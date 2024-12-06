from typing import List
from detectools.formats import (
    BaseFormat,
    BboxFormat,
    BboxData,
    InstanceMaskData,
    InstanceMaskFormat,
)
import torchvision.transforms.v2 as T
from torch import Tensor
from torchvision.tv_tensors import Image
import torch
import detectools.data.errors as er

# Tested : Mask : Ok : RandomResize, RandomCrop, RandomZoomOut, ScaleJitter, RandomHorizontalFlip / Vertical, RandomRotation, RandomAffine, RandomPerspective
#           Errors : RandomCropIou if you have masks only -> needs boxes
#           boxes : Ok : same as mask but careful with crop / rotation : can lead to slightly off new boxes as per rotation / crops don't preserve structural information of boxes by nature

# TODO check augmentation rotation with boxes : got an error of different input shape / canvas size between image and boxes


class Augmentation:
    """Class that handles augmentation in dataset. Call on different Formats (data_type) specific methods
    Args:
        augmentations (List[T.Transform]): List of torchvision.transforms.v2 Transform classes (or from detectools.data.additional_augmentations)
    """

    def __init__(self, augmentations: List[T.Transform]) -> None:
        self.transform = T.Compose(augmentations)

    def __call__(self, image: Tensor, target: BaseFormat):
        """Augment depending on format type"""
        image = Image(image)
        transformed_target, _, transformed_img = target.apply_augmentation(
            image, self.transform
        )
        return transformed_img, transformed_target
