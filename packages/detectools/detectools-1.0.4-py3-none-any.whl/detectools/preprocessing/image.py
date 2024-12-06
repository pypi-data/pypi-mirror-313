from torch import Tensor
from pathlib import Path
import torch
from typing import Union
from PIL import Image
import torchvision.transforms.functional as F
from torchvision.transforms.functional import pil_to_tensor


def save_image(image: Union[Tensor, Image.Image], path: Union[str, Path]) -> Image:
    """Transform image in PIL format and save to given path."""
    if not isinstance(path, Path):
        path = Path(path)
    parent = path.parent
    Path(parent).mkdir(exist_ok=True, parents=True)
    if isinstance(image, Image.Image):
        image.save(path.as_posix())
    else:
        image = image.to(torch.uint8)
        pil_image = F.to_pil_image(image)
        pil_image.save(path.as_posix())


def load_image(image_path: Union[str, Path]) -> Tensor:
    """Load image using torchvision. Handles png, tiff, jpg, jpeg extensions.

    Args:
        image_path (str): Path to image.

    Returns:
        Tensor: image in torch Tensor [3, H, W].
    """
    if isinstance(image_path, str):
        image_path = Path(image_path)
    img = Image.open(image_path)
    img = pil_to_tensor(img)
    return img
