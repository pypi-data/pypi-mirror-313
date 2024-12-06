from detectools.formats import BaseFormat, BboxData
from detectools import Configuration
from math import ceil, floor
from typing import Tuple
from torchvision.ops import nms
from torch import Tensor
import torch
from ultralytics.utils.ops import scale_masks


def yolo_pad_requirements(h: int, w: int, required=32) -> Tuple[int, int, int, int]:
    """Conmpute pad coordinates to ensure /32 or /64 yolo criterium on height and width

    Args:
        h (``int``): height
        w (``int``): width
    Returns:
        ``Tuple[int, int, int, int]``:
            - top, left, right, bottom
    """
    diff_h, diff_w = h % required, w % required
    pad_h = required - diff_h if diff_h > 0 else 0
    pad_w = required - diff_w if diff_w > 0 else 0
    # define padding for each border
    if pad_h or pad_w:
        half_h, half_w = pad_h / 2, pad_w / 2
        left, top, right, bottom = (
            ceil(half_w),
            ceil(half_h),
            floor(half_w),
            floor(half_h),
        )
    else:
        left, top, right, bottom = (0, 0, 0, 0)
    return (top, left, right, bottom)


def confidence_filter(scores: Tensor, conf_threshold) -> Tensor:
    """Filter Format according to confidence threshold from Configuration()

    Args:
        format (``Format``)

    Returns:
        ``Format``
    """
    if scores.nelement() == 0:
        return torch.tensor([])
    filt: Tensor = scores > conf_threshold
    return filt


def box_nms_filter(boxdata: BboxData, scores: Tensor) -> BaseFormat:
    """Filter Format according to nms threshold from Configuration()

    Args:
        format (``Format``)

    Returns:
        ``Format``
    """
    if boxdata.nb_object == 0:
        return torch.tensor([])
    boxdata.format = "XYXY"
    indexes: Tensor = nms(
        boxdata.value.float(),
        scores=scores,
        iou_threshold=Configuration().model_nms_threshold,
    )
    return indexes


def normalize_boxes(boxes: Tensor, img_size: Tuple[int, int]) -> Tensor:
    boxes = boxes.float()
    image_w = img_size[1]
    image_h = img_size[0]
    boxes[:, 0] = boxes[:, 0] / image_w
    boxes[:, 1] = boxes[:, 1] / image_h
    boxes[:, 2] = boxes[:, 2] / image_w
    boxes[:, 3] = boxes[:, 3] / image_h
    return boxes


def proto2mask(
    protos: Tensor, weights: Tensor, boxes: Tensor, shape: Tuple[int]
) -> Tensor:
    """Combine protos and weights to get masks, then crop instances from boxes (Useful in predictions).

    Args:
        protos (``Tensor``): Sub masks (32, ...).
        weights (``Tensor``): YOLO mask weights (32, ...).
        boxes (``Tensor``): Boxes (N, 4) in XYXY format.
        shape (``Tuple[int]``): Original image size (H, W).

    Returns:
        ``Tensor``:
            - YOLO segmentation mask.
    """
    c, mh, mw = protos.shape  # CHW
    masks = (weights @ protos.float().view(c, -1)).sigmoid().view(-1, mh, mw)
    masks: Tensor = scale_masks(masks[None], shape)[0]  # CHW
    for m in range(masks.shape[0]):
        xl, yl, xr, yr = boxes.int()[m]
        masks[m, 0:yl, :] = 0
        masks[m, yr:, :] = 0
        masks[m, :, 0:xl] = 0
        masks[m, :, xr:] = 0
    return masks


# def mask2yolo(mask: Tensor) -> Tensor:
#     """Convert stacked binary to yolo mask, i.e (1, h, w) with values in [0, ... , Nobjs]
#     This shape is suitable for yolov8 loss.

#     Args:
#         mask (``Tensor``): Stacked binary mask (N, H, W).

#     Returns:
#         ``Tensor``:
#             - YOLO segmentation mask.
#     """
#     if mask.ndim < 3:
#         mask = mask[None, :]
#     reidexed = torch.zeros(mask.shape[-3:]).to(mask.device)
#     reidexed = reidexed.long()
#     current_add = 0
#     for i, m in enumerate(mask):
#         if torch.max(m) == 0:
#             continue
#         m[m != 0] += current_add
#         current_add = torch.max(m)
#         reidexed[i, :] = m
#     # convert to yolomask: stacked h, w with values in [0, ..., Nobjs], 0 being absence of object
#     yolomask, _ = torch.max(reidexed, dim=0)
#     return yolomask[None, :]
