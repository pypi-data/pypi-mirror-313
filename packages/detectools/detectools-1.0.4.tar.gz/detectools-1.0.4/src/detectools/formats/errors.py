from torch import Tensor
from torchvision.tv_tensors import BoundingBoxes, Mask
from typing import Union, Tuple, List
from detectools import Configuration


# ============= Exceptions

# Format


class FormatTypeMismatchException(Exception):
    def __init__(self, obj, required_type) -> None:
        message = f"Required type is {required_type}, got {type(obj)}."
        super().__init__(message)


class MismatchCanvasSizeException(Exception):
    def __init__(self, obj1, obj2) -> None:
        message = f"Mismatch canvas_size : {type(obj1)} has {obj1.canvas_size} and {type(obj2)} has {obj2.canvas_size}."
        super().__init__(message)


class MismatchObjectNumberException(Exception):
    def __init__(self, obj1, obj2) -> None:
        message = f"Mismatch nb_object : {type(obj1)} has {obj1.nb_object} and {type(obj2)} has {obj2.nb_object}."
        super().__init__(message)


class MismatchDeviceException(Exception):
    def __init__(self, obj1, obj2) -> None:
        message = f"Mismatch device : {type(obj1)} has {obj1.device} and {type(obj2)} has {obj2.device}."
        super().__init__(message)


class NoObjectException(Exception):
    def __init__(self) -> None:
        message = f"Neither bounding box nor mask provided, please use Format.empty(canvas_size) to create empty object"
        super().__init__(message)


class NumberObjectException(Exception):
    def __init__(self, obj):
        message = f"Number of objects differents between labels and data, got {obj.nb_object} and {obj.data.nb_object}"
        super().__init__(message)


# Boxes


class BboxFormatException(Exception):
    def __init__(self, bbox, format, canvas_size):
        message = f"bbox must be a BoundingBoxes torchvision instance OR torch Tensor while specifying canvas_size and format, got : bbox = {bbox}, format = {format}, canvas_size = {canvas_size}"
        super().__init__(message)


class BboxShapeException(Exception):
    def __init__(self, bbox):
        message = f"bbox shape must be [N, 4] got {bbox.shape}"
        super().__init__(message)


class BboxConsistencyException(Exception):
    def __init__(self, bbox) -> None:
        message = f"Something went wrong with bbox. Please check format, size, canvas_size, values : bbox = {bbox.value}, format = {bbox.format}, canvas_size = {bbox.canvas_size}, nb_objects = {bbox.nb_objects}"
        super.__init__(message)


# Masks


class MaskShapeException(Exception):
    def __init__(self, mask):
        message = f"mask dim must be 2 (i.e. (H, W) ) got mask shape = {mask.shape}"
        super().__init__(message)


# others


class ProtectedAttributeException(Exception):
    def __init__(self):
        super().__init__(
            "Can't modify this protected attribute, would lead to inconsistency"
        )


class CropCoordinatesException(Exception):
    def __init__(self, obj, left, top, height, width):
        message = f"Crop coordinates larger than canvas_size of BboxData, got : top: {top}, left: {left}, height: {height}, width: {width}, canvas_size: {obj.canvas_size}"
        super().__init__(message)


class NoFormatException:
    def __init__(self) -> None:
        message = "No data format has been set (nor mask or boxes)"
        super().__init__(message)


# ============== Tests

# Tests are used for sanity checks. They return False if there is a problem, True if the object is correct


def check_canvas_size(canvas_size: Tuple[int, int]):
    assert (
        len(canvas_size) == 2
    ), f"Incorrect canvas_size, must be a 2-tuple, got {canvas_size}"
    pass


def check_bbox_dim(bbox: Union[Tensor, BoundingBoxes]):
    """Check that bbox is [N, 4]"""
    if bbox.dim() != 2 or bbox.shape[-1] != 4:
        raise BboxShapeException(bbox)
    pass


def check_mask_dim(mask: Union[Tensor, Mask]):
    if mask.dim() != 2:
        raise MaskShapeException(mask)
    pass


def check_crop_coords(obj, t, l, h, w):
    if not ((t + h <= obj.canvas_size[0]) and (l + w <= obj.canvas_size[1])):
        raise CropCoordinatesException(obj, t, l, h, w)
    pass


def check_format_init(obj_key, obj, required_type):
    assert (
        getattr(obj, obj_key) != None
    ), f"As per configuration, {obj_key} must be passed as argument of Format. No {obj_key} in here."
    if not (isinstance(getattr(obj, obj_key), required_type)):
        raise FormatTypeMismatchException(getattr(obj, obj_key), required_type)


def check_bbox_assertion_with_boxfrommask():
    assert not (
        Configuration().box_from_masks
    ), "Cannot set bboxes attributes if box_from_masks enabled in Configuration(). Please, consider setting mask instead and boxes will be computed accordingly or disable box_from_mask."
    pass


def check_batched_canvas_size(obj_list: List[object]):
    l = [obj.canvas_size for obj in obj_list]
    if len(l) == 0:
        pass
    else:
        test = [l[0] == it for it in l]
        test = all(test)
        assert (
            test
        ), f"All canvas_size in Format list for BatchedFormat aren't equal, got: {l}"
    pass


def check_labels_size(obj):
    if obj.nb_object != obj.data.nb_object:
        raise NumberObjectException(obj)
