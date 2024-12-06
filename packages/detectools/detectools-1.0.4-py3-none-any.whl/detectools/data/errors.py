from typing import List
from torch import Tensor
from detectools.formats import BaseFormat


def check_images_targets_size(images: List[Tensor], targets: List[BaseFormat]):
    assert all([img.shape[-2] == images[0].shape[-2] for img in images]) and all(
        [img.shape[-1] == images[0].shape[-1] for img in images]
    ), "DataLoader : images do not have the same shape"
    assert all(
        [targ.canvas_size[0] == targets[0].canvas_size[0] for targ in targets]
    ) and all(
        [targets[0].canvas_size[1] == targ.canvas_size[1] for targ in targets]
    ), "DataLoader: Targets don't have the same canvas_size"
    assert (images[0].shape[-2] == targets[0].canvas_size[0]) and (
        images[0].shape[-1] == targets[0].canvas_size[1]
    ), "DataLoader : images and targets do not have the save shape / canvas_size. "


class UnknownFormatException(Exception):
    def __init__(self, obj, message: str) -> None:
        message = f"Unknown format {type(obj)}. {message}"
        super().__init__(message)
