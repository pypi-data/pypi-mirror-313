from typing import List, Tuple, Union
import torch
from torch import Tensor
import torchvision.transforms.v2 as T
from torchvision.io import read_image
from pathlib import Path


def build_preprocessing(
    mean: List[float] = [0.485, 0.456, 0.406], std: List[float] = [0.229, 0.224, 0.225]
) -> T.Compose:
    """Build preprocessing to scale RGB tensor image values between 0 & 1 and normalize according to
    mean and std. Defaults values are from Imagenet.

    Args:
        mean (List[float], optional): mean values for each channels Defaults to [0.485, 0.456, 0.406].
        std (List[float], optional): std values for each channels. Defaults to [0.229, 0.224, 0.225].

    Returns:
        T.Compose:
    """
    # build the Compose
    preprocessing = T.Compose(
        [
            T.ConvertImageDtype(
                dtype=torch.float32
            ),  # torch.float32 is universal for DL
            T.Normalize(mean=mean, std=std),
        ]
    )

    return preprocessing


def get_channels_statistics(image_folder: Union[str, Path]) -> Tuple[Tensor]:
    """Iterate over image folder and output mean and std for each channels for the dataset of images.

    Args:
        image_folder (str): path to folder of images

    Returns:
        Tuple[List[float]]: values for mean and std
    """
    if not isinstance(image_folder, Path):
        image_folder = Path(image_folder)
    # build Compose to scale image values
    scaler = T.Compose([T.ConvertImageDtype(dtype=torch.float32)])
    # initialization of dataset variables
    channels_sum, channels_squared_sum = 0, 0
    n_images = 0
    # iterate over folder
    for img_path in image_folder.iterdir():
        # load image as tensor and scale values
        image = read_image(img_path.as_posix())
        image = scaler(image)
        # sum channels values
        channels_sum += torch.mean(image, dim=[1, 2])
        channels_squared_sum += torch.mean(image**2, dim=[1, 2])
        # increment total of image
        n_images += 1

    # compute dataset mean & std
    mean = channels_sum / n_images
    std = (channels_squared_sum / n_images - mean**2) ** 0.5

    return mean, std
