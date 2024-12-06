import geomloss
import torch
import numpy as np
from torch.nn import MSELoss

device = "cuda" if torch.cuda.is_available() else "cpu"
NONZERO_FACTOR = 1e-5


class SinkhornLoss:
    def __init__(
        self,
        cost_matrix,
        normalize_cost=True,
        spatiotemporal=False,
        blur=0.1,
        reach=0.01,
        scaling=0.1,
        mode="unbalanced",
        **sinkhorn_kwargs,
    ):
        """Initialize Sinkhorn loss to train NN with OT loss

        Args:
            cost_matrix (np.ndarray): 2-dim numpy array with pairwise costs
                between locations
            normalize_cost (bool): Whether to normalize cost matrix by dividing
                by the maximum cost.
            spatiotemporal (bool): Set to True to compute the error for spatio-
                temporal data (across space and time)
            blur (float, optional): typical scale associated to the temperature.
                Defaults to 0.1. See
                https://www.kernel-operations.io/geomloss/api/pytorch-api.html.
            reach (float, optional): specifies the typical scale associated to
                the constraint strength. Defaults to 0.01. See
                https://www.kernel-operations.io/geomloss/api/pytorch-api.html.
            scaling (float, optional): _description_. Defaults to 0.1.
                https://www.kernel-operations.io/geomloss/api/pytorch-api.html.
            mode (str, optional): How prediction and gt are normalized.
                if mode=unbalanced: pred and gt have different mass
                if mode=balancedSoftmax: pred is softmaxed, gt is normalized
                if mode=balanced: pred and gt are both normalized to sum 1
                Defaults to "unbalanced".
        """
        assert mode in ["unbalanced", "balancedSoftmax", "balanced"]
        self.mode = mode
        self.spatiotemporal = spatiotemporal
        # adapt cost matrix type and size
        if isinstance(cost_matrix, np.ndarray):
            cost_matrix = torch.from_numpy(cost_matrix)
        # normalize to values betwen 0 and 1
        if normalize_cost:
            cost_matrix = cost_matrix / torch.max(cost_matrix)
        if cost_matrix.dim() != 3:
            if cost_matrix.dim() != 2:
                raise ValueError(
                    "cost matrix cost_matrix must have 2 or 3 dimensions"
                )
            cost_matrix = cost_matrix.unsqueeze(0)

        # cost matrics and locs both need a static representation and are
        # modified later to match the batch size
        self.cost_matrix = cost_matrix.to(device)
        self.cost_matrix_original = self.cost_matrix.clone()

        # introduce dummy weights since we assume fixed locations
        self.dummy_weights_alpha = torch.tensor(
            [[[i] for i in range(cost_matrix.size()[-2])]]
        ).float()
        self.dummy_weights_beta = torch.tensor(
            [[[i] for i in range(cost_matrix.size()[-1])]]
        ).float()
        self.dummy_weights_a = self.dummy_weights_alpha.clone()
        self.dummy_weights_b = self.dummy_weights_beta.clone()

        # sinkhorn loss
        self.loss_object = geomloss.SamplesLoss(
            loss="sinkhorn",
            cost=self.get_cost,
            backend="tensorized",
            debias=True,
            blur=blur,
            reach=reach,
            scaling=scaling,
            **sinkhorn_kwargs,
        )

    def get_cost(self, a, b):
        return self.cost_matrix

    def adapt_to_batchsize(self, batch_size):
        if self.cost_matrix.size()[0] != batch_size:
            self.cost_matrix = self.cost_matrix_original.repeat(
                (batch_size, 1, 1)
            )
            self.dummy_weights_a = self.dummy_weights_alpha.repeat(
                (batch_size, 1, 1)
            )
            self.dummy_weights_b = self.dummy_weights_beta.repeat(
                (batch_size, 1, 1)
            )

    def __call__(self, a_in, b_in):
        """a_in: predictions, b_in: targets"""

        # 1) Normalize dependent on the OT mode (balanced / unbalanced)
        b_in = b_in + NONZERO_FACTOR  # to prevent that all gt are zero
        if self.mode == "balanced":
            a = a_in / torch.unsqueeze(torch.sum(a_in, dim=-1), -1)
            b = b_in / torch.unsqueeze(torch.sum(b_in, dim=-1), -1)
        elif self.mode == "balancedSoftmax":
            # this yields a spearman correlation of 0.74
            a = (a_in * 2.71828).softmax(dim=-1)
            b = b_in / torch.unsqueeze(torch.sum(b_in, dim=-1), -1)
        else:
            # TODO: Any other possibility to do relu without getting all zeros?
            a = torch.relu(a_in) + NONZERO_FACTOR
            b = b_in

        # 2) flatten one axis -> either for spatiotemporal OT or treating the
        # temporal axis as batch
        batch_size = a.size()[0]
        if self.spatiotemporal:
            # flatten space-time axes
            a = a.reshape((batch_size, -1))
            b = b.reshape((batch_size, -1))
        elif a.dim() == 3:
            # if we have to flatten at all, flatten time over the batch size
            steps_ahead = a.size()[1]
            a = a.reshape((batch_size * steps_ahead, -1))
            b = b.reshape((batch_size * steps_ahead, -1))
            batch_size = batch_size * steps_ahead

        # 3) Adapt cost matrix size to the batch size
        self.adapt_to_batchsize(batch_size)

        # 4) Normalize again if spatiotemporal (over the space-time axis)
        # such that it overall sums up to 1
        if self.spatiotemporal and self.mode != "unbalanced":
            a = a / torch.unsqueeze(torch.sum(a, dim=-1), -1)
            b = b / torch.unsqueeze(torch.sum(b, dim=-1), -1)

        loss = self.loss_object(
            a, self.dummy_weights_a, b, self.dummy_weights_b
        )
        return torch.sum(loss)


class CombinedLoss:
    def __init__(
        self, cost_matrix, mode="balancedSoftmax", spatiotemporal=False
    ) -> None:
        self.standard_mse = MSELoss()
        if spatiotemporal:
            self.sinkhorn_error = SinkhornLoss(
                cost_matrix, mode=mode, spatiotemporal=True
            )
            self.dist_weight = 100
        else:
            self.sinkhorn_error = SinkhornLoss(cost_matrix, mode=mode)
            self.dist_weight = 10

    def __call__(self, a_in, b_in):
        # compute the error between the mean of predicted and mean of gt demand
        # this is the overall demand per timestep per batch
        # total_mse = (torch.mean(a_in, dim=-1) - torch.mean(b_in, dim=-1)) ** 2
        # take the average of the demand divergence over batch & timestep
        # mse_loss = torch.mean(total_mse)
        mse_loss = self.standard_mse(a_in, b_in)
        # mse_loss = self.standard_mse(a_in, b_in)
        sink_loss = self.sinkhorn_error(a_in, b_in)
        # for checking calibration of weighting
        # print(mse_loss, self.dist_weight * sink_loss)
        return mse_loss + self.dist_weight * sink_loss


def sinkhorn_loss_from_numpy(
    a,
    b,
    cost_matrix,
    mode="unbalanced",
    sinkhorn_kwargs={},
    loss_class=SinkhornLoss,
):
    a = torch.tensor(a.tolist()).float()
    b = torch.tensor(b.tolist()).float()
    # cost_matrix = torch.tensor([cost_matrix])
    # # Testing for the case where multiple steps ahead are predicted
    # a = a.unsqueeze(1).repeat(1, 3, 1)
    # b = b.unsqueeze(1).repeat(1, 3, 1)
    # print("Before initializing", cost_matrix.shape, a.size(), b.size())
    loss = loss_class(cost_matrix, mode=mode, **sinkhorn_kwargs)
    return loss(a, b)
