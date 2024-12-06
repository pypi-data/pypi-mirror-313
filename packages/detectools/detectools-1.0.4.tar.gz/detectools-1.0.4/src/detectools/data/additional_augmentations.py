import torch
import torchvision.transforms.v2 as T
from torchvision.transforms.v2 import Transform
from typing import Sequence, Union
from typing import Tuple
import random as rd


class RandomCropAndResize(Transform):
    """
    With a given probability, apply RandomCrop and Resize from torchvision.transforms.v2.
    NB : here we resize only and systematically if cropped.

    Args:
        crop (``Union[int, Sequence[int]]``): Size to crop
        resize (``Union[int, Sequence[int]]``): Size to resize
        p (``float``, **optional**): probability. Defaults to 0.5.


    **Methods**:
    """

    def __init__(
        self,
        crop: Union[int, Sequence[int]],
        resize: Union[int, Sequence[int]],
        p=0.5,
        **kwargs,
    ):

        super().__init__(**kwargs)
        self.p = p
        self.crop = T.RandomCrop(crop)
        self.resize = T.Resize(resize)

    def forward(self, *inputs):
        if torch.rand(1) >= self.p:
            pass
        else:
            inputs = self.crop.forward(inputs)
            inputs = self.resize.forward(inputs)
        return inputs


class RandomCenterCropAndResize(Transform):
    """
    With a given probability, apply CenterCrop and Resize from torchvision.transforms.v2.
    NB : here we resize only and systematically if cropped.

        Args:
            crop (``Union[int, Sequence[int]]``): Size to crop
            resize (``Union[int, Sequence[int]]``): Size to resize
            p (``float``, **optional**): probability. Defaults to 0.5.
    """

    def __init__(self, crop: Sequence[int], resize: Sequence[int], p=0.5, **kwargs):
        super().__init__(**kwargs)
        self.p = p
        self.crop = T.CenterCrop(crop)
        self.resize = T.Resize(resize)

    def forward(self, *inputs):
        if torch.rand(1) >= self.p:
            pass
        else:
            inputs = self.crop.forward(inputs)
            inputs = self.resize.forward(inputs)
        return inputs


class RandomPadAndResize(Transform):
    """
    With a given probability, apply Pad and Resize from torchvision.transforms.v2. This looks like a zoom out effect by decreasing spatial resolution.
    NB : here we resize only and systematically if Padded.

        Args:
            MaxPad (``Union[int, Sequence[int]]``): maximum padding bounds can be int for common padding bound for all borders or sequence of 4 ints for (t, l, b, r)
            resize (``Union[int, Sequence[int]]``): Size to resize
            p (``float``, **optional**): probability to apply transformation. Defaults to 0.5.
    """

    def __init__(
        self,
        maxpad: Sequence[int],
        resize: Sequence[int],
        p=0.5,
        **kwargs,
    ):

        super().__init__(**kwargs)
        self.p = p
        self.max_pad = (maxpad,) * 4 if isinstance(maxpad, int) else maxpad
        self.resize = T.Resize(resize)

    def forward(self, *inputs):
        if torch.rand(1) >= self.p:
            pass
        else:
            t = rd.randrange(0, self.max_pad[0])
            l = rd.randrange(0, self.max_pad[1])
            r = rd.randrange(0, self.max_pad[2])
            b = rd.randrange(0, self.max_pad[3])
            padder = T.Pad([t, l, b, r])
            inputs = padder.forward(inputs)
            inputs = self.resize.forward(inputs)
        return inputs
