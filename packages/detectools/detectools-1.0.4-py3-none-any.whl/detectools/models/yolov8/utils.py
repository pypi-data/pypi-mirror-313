from detectools.formats import BaseFormat
from detectools import Configuration
from math import ceil, floor
from typing import Tuple
from torchvision.ops import nms
from torch import Tensor


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


def confidence_filter(format: BaseFormat) -> BaseFormat:
    """Filter Format according to confidence threshold from Configuration()

    Args:
        format (``Format``)

    Returns:
        ``Format``
    """
    assert format.scores != None, "Scores are not in format: cannot filter."
    new_format, _ = format[format.scores > Configuration().model_confidence_threshold]
    return new_format


def box_nms_filter(format: BaseFormat) -> BaseFormat:
    """Filter Format according to nms threshold from Configuration()

    Args:
        format (``Format``)

    Returns:
        ``Format``
    """
    if format.nb_object == 0:
        return format
    original_format = format.data.format
    format.data.format = "XYXY"
    indexes: Tensor = nms(
        format.data.value.float(),
        scores=format.scores.float(),
        iou_threshold=Configuration().model_nms_threshold,
    )
    indexes = indexes.to(Configuration().device).sort()[0]
    format.data.format = original_format
    new_format, _ = format[indexes]
    return new_format


def normalize_boxes(boxes: Tensor, img_size: Tuple[int, int]) -> Tensor:
    """Normalize boxes to 1 -> h, w -> [0, 1] according to img size

    Args:
        boxes (``Tensor``): boxes Tensor
        img_size (``Tuple[int, int]``): image size

    Returns:
        ``Tensor``:
            - normalized boxes
    """
    boxes = boxes.float()
    image_w = img_size[1]
    image_h = img_size[0]
    boxes[:, 0] = boxes[:, 0] / image_w
    boxes[:, 1] = boxes[:, 1] / image_h
    boxes[:, 2] = boxes[:, 2] / image_w
    boxes[:, 3] = boxes[:, 3] / image_h
    return boxes
