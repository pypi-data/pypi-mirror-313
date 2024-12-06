from __future__ import annotations
from torch.utils.data import Dataset, DataLoader
from typing import Union, Tuple, List, Dict, Callable, Sequence, Literal
from pathlib import Path
from detectools.data.data_reader.readers import (
    BaseReader,
    CocoReader,
    ANNOTATION_TYPE_DICT,
)
from detectools.preprocessing.preprocessing import build_preprocessing
from detectools.preprocessing.image import load_image, save_image
from detectools import Configuration
from detectools.formats import BaseFormat, BatchedFormat
from detectools.utils import visualization
from torch import Tensor
from torchvision.transforms.v2 import Transform
from detectools.data.augmentation_class import Augmentation
import torchvision.transforms.v2 as T
import torch
import copy
from random import shuffle
import detectools.data.errors as er
from tqdm import tqdm
import json


class DetectDataset(Dataset):
    """Detection dataset class for detectools : load and return image, annotation, image name.

    Args:
        dataset_path (Union[str, Path]): path to dataset folder.
        reader (BaseReader, optional): Class to read data from dataset folder. Defaults to CocoReader.
        preprocessing (Callable, optional): Preprocessing images (normalization). Defaults to build_preprocessing().
        augmentation (List[Transform], optional): Augmentation to apply to images / annotations. Must be from torchvision.transforms.v2.Transform Defaults to None.
        label_converter (Dict[int, int], optional): Convert labels to another value. For e.g : {0: 2, 1: 5} etc. Defaults to None.

    Example:
    ----------

    .. highlight:: python
    .. code-block:: python

        >>> from detectools import DetectDataset
        >>> data_path = \"path/to/data\"
        >>> dataset = DetectDataset(data_path)
        >>> image, target, image_name = dataset[1]
        >>> print(type(image), type(target), type(image_name))
        <class 'torch.Tensor' >, <class 'BboxFormat' >, <class 'str'>
        >>> print(image.shape, target.size, image_name)
        torch.Size([3,512,512]), 5, 'img_01.png'


    Attributes
    ----------

    Attributes:
        - dataset_path (``Path``): path to dataset folder.
        - reader (``BaseReader``): Class to read data from dataset folder. Defaults to CocoReader.
        - preprocessing (``Callable``): Preprocessing images (normalization). Defaults to build_preprocessing().
        - augmentation (``List[Transform]``): Augmentation to apply to images / annotations. Must be from torchvision.transforms.v2.Transform Defaults to None.
        - category_ids (``Dict[int, str]``): Dict that associate a name to a category label index. Defaults is equal to self.reader.category_ids
        - label_converter (``Dict[int, int]``): Convert labels to another value. For e.g : {0: 2, 1: 5} etc. Defaults to None.


    **Methods**:
    """

    def __init__(
        self,
        dataset_path: Union[str, Path],
        reader: BaseReader = CocoReader,
        preprocessing: Callable = build_preprocessing(),
        augmentation: List[Transform] = None,
        label_converter: Dict[int, int] = None,
    ):

        self.dataset_path = (
            dataset_path if isinstance(dataset_path, Path) else Path(dataset_path)
        )
        self.reader: BaseReader = reader(dataset_path)
        self.preprocessing = preprocessing
        self.augmentation = augmentation
        self.category_ids = self.reader.category_ids
        self.label_converter = label_converter
        self._img_dir = self.dataset_path / "images"
        self._device = Configuration().device
        # The following is to handle splitting
        self._indexes = list(range(len(self.reader)))

    def __getitem__(self, idx: int):
        elem = self.reader[self._indexes[idx]]
        img_name: str = elem[0]
        target: BaseFormat = elem[1]
        # Rename / regroup categories if wanted
        if self.label_converter != None:
            new_labels = [self.label_converter[l] for l in target.labels]
            target = type(target)(target.data, new_labels)

        image = load_image(self._img_dir / img_name)
        image = image.to(self._device)
        target.device = self._device

        if self.augmentation != None:
            augment = Augmentation(self.augmentation)
            image, target = augment(image, target)

        if self.preprocessing != None:
            image = self.preprocessing(image)

        target, _ = target.sanitize()
        return image, target, img_name

    def __len__(self) -> int:
        return len(self._indexes)

    def __iter__(self):
        for x in range(len(self)):
            yield self[x]

    def split(
        self, sequence: Sequence[float, float, float]
    ) -> Tuple[DetectDataset, DetectDataset, DetectDataset]:
        """split dataset in 3 new datasets according to proportions

        Args:
            sequence (Sequence[float, float, float]): proportions to split the dataset into. Sum must be 1.

        Example:
        ----------
        .. highlight:: python
        .. code-block:: python

            >>> dataset = DetectDataset("path/to/dataset")
            >>> train_dataset, valid_dataset, test_dataset = dataset.split((0.6, 0.2, 0.2))
        """
        seq_sum = sum(sequence)
        assert round(seq_sum, 3) == 1, "sequence sum is not equal to 1."
        idx = copy.copy(self._indexes)
        shuffle(idx)
        stop1 = int(sequence[0] * len(idx))
        stop2 = int(sum(sequence[0:2]) * len(idx))
        stop3 = int(seq_sum * len(idx))
        if stop2 > len(idx):
            stop2 -= len(idx) - stop2
        dataset1 = copy.deepcopy(self)
        dataset1._indexes = idx[0:stop1]
        dataset2 = copy.deepcopy(self)
        dataset2._indexes = idx[stop1:stop2]
        dataset3 = copy.deepcopy(self)
        if len(idx[stop2:]) == 0:
            dataset3 = None
        else:
            dataset3._indexes = idx[stop2:]
        return dataset1, dataset2, dataset3

    def keep_indexes(self, indexes: Union[list, slice, Tensor]):
        """Filter dataset by keeping only indices given in arg.

        Args:
            indexes (``Union[list, slice, Tensor]``): can be slice, Tensor or list. To use slice please use : slice(i, j) with i, j desired slice indexes in arg.
        """
        if isinstance(indexes, Tensor):
            assert (
                indexes.dim() == 1
            ), f"Must use Tensor of dim 1 for indexes, got {indexes.shape}"
            indexes = indexes.tolist()
        indx = torch.tensor(self._indexes)[indexes].tolist()
        self._indexes = indx

    def export_dataset(
        self,
        destination_folder: Union[str, Path],
        number_visu: Union[Literal["all"], int] = "all",
        file_extension: str = "",
    ):
        """Export dataset accordingly to BaseReader class. For example CocoReader will export in following structure:
        Dataset Name -> Image_dir, coco_annotations.json

        Args:
            destination_folder (Union[str, Path]): Path to new dataset folder.
            number_visu (Union[Literal[&quot;all&quot;], int], optional): number of visualization to create. If "all" will derive all of them. Defaults to "all".
            file_extension (str, optional): if requires a specific file extension. If "" will use BaseReader's. Defaults to "".
        """
        if file_extension == "":
            file_extension = self.reader.annotation_file_type
        destination_folder = (
            destination_folder
            if isinstance(destination_folder, Path)
            else Path(destination_folder)
        )
        number_visu = len(self) if number_visu == "all" else number_visu
        img_folder = destination_folder / "images"
        annot_folder = destination_folder / "annotations"
        visu_folder = destination_folder / "visualizations"
        if number_visu > 0:
            visu_folder.mkdir(parents=True, exist_ok=True)
        img_folder.mkdir(parents=True, exist_ok=True)
        annot_folder.mkdir(parents=True, exist_ok=True)
        for img, target, img_name in tqdm(
            self, total=len(self), desc="Exporting dataset : "
        ):
            visu_saved = 0
            if visu_saved < number_visu:
                visu_path = visu_folder / f"visu__{img_name}"
                visualization(img, target, self.category_ids, save_path=visu_path)
            save_image(img, img_folder / img_name)
            _, export_target = self.reader.export_annotation(
                img_name, img, target, self.category_ids
            )
            annot_file_path = annot_folder / f"annotation__{img_name}.{file_extension}"
            if ANNOTATION_TYPE_DICT[file_extension] == "file":
                with open(annot_file_path, "w") as f:
                    if isinstance(export_target, dict):
                        json.dump(export_target, f)
                    else:
                        f.write(export_target)
            elif ANNOTATION_TYPE_DICT[file_extension] == "image":
                save_image(annot_file_path)
        if file_extension == "json":
            self.reader.group_export(
                annot_folder,
                destination_folder / "coco_annotations.json",
                self.category_ids,
            )


class DetectLoader(DataLoader):
    """Child class of ``DataLoader`` that batchify images and BaseFormats. DetectionLoader support any features from torch Dataloaders (Sampler, etc..).

    Args:
        *args
        *kwargs

    Example:
    ----------
    .. highlight:: python
    .. code-block:: python

        >>> from detectools import DetectLoader
        >>> loader = DetectLoader(dataset, batch_size=2)
        >>> for batch in loader:
        >>>     img, target, img_name = batch


    **Methods**:
    """

    def __init__(self, *args, **kwargs):
        super().__init__(collate_fn=self.collate_fn, *args, **kwargs)

    def collate_fn(
        self, batch: List[Tuple[str, Tensor, BaseFormat]]
    ) -> Tuple[Tensor, BaseFormat]:
        """
        Args:
            batch (``List[Tuple[Tensor, BaseFormat]]``): List of pairs image/target.

        Returns:
            ``Tuple[Tensor, BatchedFormats]``:
                - Batch images (N, 3, H, W).
                - BaseFormats wrapped into BatchedFormats class.
        """
        images = [triplet[0] for triplet in batch]
        targets = [triplet[1] for triplet in batch]
        names = {i: triplet[2] for i, triplet in enumerate(batch)}
        images, targets = self.pad_to_larger(images, targets)
        er.check_images_targets_size(images, targets)
        batch_images = torch.stack(images).to(Configuration().device)
        batch_targets = BatchedFormat(targets)

        return batch_images, batch_targets, names

    def pad_to_larger(
        self, images: List[Tensor], targets: List[BaseFormat]
    ) -> Tuple[List[Tensor], List[BaseFormat]]:
        """Pad images and targets to larger image size.

        Args:
            images (``List[Tensor]``): Images.
            targets (``List[BaseFormat]``): Targets.
        """
        # get max borders sizes
        larger_width = max([image.shape[-1] for image in images])
        larger_height = max([image.shape[-2] for image in images])
        padded_images, padded_targets = [], []

        # for each image pad image & target
        for i, image in enumerate(images):
            t = int((larger_height - image.shape[-2]) / 2)
            l = int((larger_width - image.shape[-1]) / 2)
            r = int((larger_width - image.shape[-1]) - l)
            b = int((larger_height - image.shape[-2]) - t)
            # Order of t, l, b, r changes again in torchvision
            padder = T.Pad((l, t, r, b))
            padded_images.append(padder(image))
            padded_targets.append(targets[i].pad_to((larger_height, larger_width))[0])

        return padded_images, padded_targets
