import torch
from torch import Tensor


@torch.jit.script
def mask_iou(
    mask1: Tensor,
    mask2: Tensor,
) -> Tensor:
    """Computes iou between 2 sets of masks of dim (N, H, W), (M, H, W). N and M denote one hot encoded masks per object.

    Args:
        mask1 (``Tensor``)
        mask2 (``Tensor``)

    Returns: Tensor

    """

    N, H, W = mask1.shape
    M, H, W = mask2.shape

    mask1 = mask1.view(N, H * W)
    mask2 = mask2.view(M, H * W)

    intersection = torch.matmul(mask1, mask2.t())

    area1 = mask1.sum(dim=1).view(1, -1)
    area2 = mask2.sum(dim=1).view(1, -1)

    union = (area1.t() + area2) - intersection

    ret = torch.where(
        union == 0,
        torch.tensor(0.0, device=mask1.device),
        intersection / union,
    )

    return ret
