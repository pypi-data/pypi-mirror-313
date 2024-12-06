from typing import Union, Tuple, Dict, List, Any
from pathlib import Path
from abc import ABC, abstractmethod
from detectools.formats import BaseFormat, BboxFormat, InstanceMaskFormat
from detectools.formats.base_data import InstanceMaskData, BboxData
from detectools import Configuration
import torch
import numpy as np
from torch import Tensor
import json
import cv2
from tqdm import tqdm

ANNOTATION_TYPE_DICT = {
    "json": "file",
    "png": "image",
    "tif": "images",
    "tiff": "image",
    "jpg": "image",
    "jpeg": "image",
}


class BaseReader(ABC):
    """Base class for readers. __len__ and __getitem__ methods must be implemented in concrete class.
    Your concrete class must implement concrete category_id property that returns Dict[int, str] where int is label and str category name.
    Your concrete class must have a class attribute describing annotation file type ("json" for json file, "png" for image etc.)
    You must implement export_annotation and group_export methods in concrete classes
    See CocoReader class for concrete implementation
    """

    @property
    def annotation_file_type(cls):
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, index: int) -> Tuple[str, BaseFormat]:
        """From a given index ([0, N-1] where N is the number of images) returns image name, Format

        Args:
            index (``int``): Index of image from 0 to N-1

        Returns:
            ``Tuple[str, Format]``:
                - returns image name (ex: something.jpg), target as Format
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def export_annotation(self, image: Tensor, annotation: BaseFormat):
        pass

    @abstractmethod
    def group_export(self, sub_anns_dir: Union[str, Path], cats: Dict[Any, Any]):
        pass

    @property
    @abstractmethod
    def category_ids(self) -> Dict[int, str]:
        pass

    @category_ids.setter
    @abstractmethod
    def category_ids(self, val):
        pass


DEFAULT_COCO_ANNOT = "coco_annotations.json"


class CocoReader(BaseReader):
    """Child class of BaseReader. Coco format reader class. Handles dataset with structure:

    Dataset Name -> Image_dir, coco_annotations.json

    Note : bboxes must be in XYWH format

    Args:
        annotation_path (Union[str, Path]): path to json file or to dataset directory.

    Attributes
    ----------

    Attributes:
        - annot_dict (``Dict[Any, Any]``): coco dict loaded.

    Attributes
    ----------

    Properties:
        - category_ids Dict[int, str]: label / category correspondance


    **Methods**
    """

    annotation_file_type = "json"

    def __init__(self, annotation_path: Union[str, Path]) -> None:

        annotation_path = (
            annotation_path
            if isinstance(annotation_path, Path)
            else Path(annotation_path)
        )
        if annotation_path.is_dir():
            annotation_path = annotation_path / DEFAULT_COCO_ANNOT
        with open(annotation_path) as f:
            self.annot_dict = json.load(f)
        # if items of annot_dict are dict convert them to lists
        if isinstance(self.annot_dict["categories"], dict):
            self.annot_dict["categories"] = [v for v in self.annot_dict["categories"]]
        if isinstance(self.annot_dict["images"], dict):
            self.annot_dict["images"] = [v for v in self.annot_dict["images"]]
        if isinstance(self.annot_dict["annotations"], dict):
            self.annot_dict["annotations"] = [v for v in self.annot_dict["annotations"]]
        # compute reindexer dict for imgs
        self._imgs_reindex_dict = {
            i: im["id"] for i, im in enumerate(self.annot_dict["images"])
        }
        # compute reindexer dict for labels / categories
        ordered_keys = [cat["name"] for cat in self.annot_dict["categories"]]
        ordered_keys.sort()
        self._category_converter = {}
        for i, name in enumerate(ordered_keys):
            for cat in self.annot_dict["categories"]:
                if name == cat["name"]:
                    self._category_converter.update({i: cat})
        self._label_converter = {
            k["id"]: i for i, k in self._category_converter.items()
        }
        # generate a correspondance between new labels and cat name
        self.category_ids = {i: k["name"] for i, k in self._category_converter.items()}

    @property
    def category_ids(self):
        return self._category_ids

    @category_ids.setter
    def category_ids(self, val: Dict[int, str]):
        self._category_ids = val

    def get_img_anns(self, index: int) -> Tuple[str, Tuple[int, int], List[dict]]:
        """return from index image as img name, spatial size as Tuple[int, int] (h, w) and all annotations for given image index

        Args:
            index (int)
        Returns:
            Tuple[str, Tuple[int, int], List[dict]]: img_name, spatial_size, list of coco anns
        """
        image = [
            img
            for img in self.annot_dict["images"]
            if img["id"] == self._imgs_reindex_dict[index]
        ]
        spatial_size = (image[0]["height"], image[0]["width"])
        image = image[0]["file_name"]
        anns = [
            ann
            for ann in self.annot_dict["annotations"]
            if ann["image_id"] == self._imgs_reindex_dict[index]
        ]
        return image, spatial_size, anns

    def __getitem__(self, index: int) -> Tuple[str, BaseFormat]:
        """From a given index ([0, N-1] where N is the number of images) returns image name, Format

        Args:
            index (``int``): Index of image from 0 to N-1

        Returns:
            ``Tuple[str, Format]``:
                - returns image name (ex: something.jpg), target as Format
        """
        image_name, spatial_size, anns = self.get_img_anns(index)

        # handle empty anns
        if anns == []:
            if Configuration().data_type == "bbox":
                format = BboxFormat.empty(spatial_size)
            if Configuration().data_type == "instance_mask":
                format = InstanceMaskFormat.empty(spatial_size)
        elif Configuration().data_type == "bbox":
            labels = torch.tensor(
                [
                    self._label_converter[ann["category_id"]]
                    for ann in anns
                    if "bbox" in ann.keys()
                ]
            )
            bboxes = [ann["bbox"] for ann in anns if "bbox" in ann.keys()]
            # handle empty
            if bboxes == []:
                format = BboxFormat.empty(spatial_size)
            else:
                bboxes = [torch.tensor(box)[None, :] for box in bboxes]
                bboxes = BboxData(
                    torch.cat(bboxes), format="XYWH", canvas_size=spatial_size
                )
                format = BboxFormat(bboxes, labels)
        elif Configuration().data_type == "instance_mask":
            labels = torch.tensor(
                [
                    self._label_converter[ann["category_id"]]
                    for ann in anns
                    if "segmentation" in ann.keys()
                ]
            )
            if labels == []:
                format = InstanceMaskFormat.empty(spatial_size)
            else:
                object_masks = [
                    self.segment2mask(ann, spatial_size)
                    for ann in anns
                    if "segmentation" in ann.keys()
                ]
                # reindex objects and stack them with id in [1 ... N_obj] range
                object_masks = [m * (i + 1) for i, m in enumerate(object_masks)]
                mask = np.max(np.stack(object_masks, axis=0), axis=0)
                mask = torch.tensor(mask).long()
                format = InstanceMaskFormat(InstanceMaskData(mask), labels)
        return image_name, format

    def segment2mask(
        self, ann: Dict[Any, Any], spatial_size: Tuple[int, int]
    ) -> np.ndarray:
        """Convert segment to object mask.

        Args:
            ann (Dict[Any, Any]): coco format annotation dict
            spatial_size (Tuple[int, int]): size of image as (h, w)

        Returns:
            np.ndarray: mask
        """
        segments = ann["segmentation"]
        # handle RLE coding
        if isinstance(segments, dict):
            assert (
                "counts" in segments.keys()
            ), f"Segmentation {segments} is dict but not RLE encoded."
            mask: np.ndarray = self.rleToMask(segments, spatial_size)
        else:
            mask = np.zeros((spatial_size[0], spatial_size[1], 3))
            segments = [
                np.array(seg, dtype=np.int32).reshape(-1, 2)
                for seg in segments
                if len(seg) > 4
            ]

            assert segments != [], "Empty annotation after filtering segment length"
            for poly in segments:
                cv2.drawContours(mask, [poly], -1, color=(1), thickness=-1)
            mask = mask[:, :, 0]
        mask: np.ndarray = mask.astype(np.uint64)
        return mask

    def rleToMask(self, rle: str, shape: Tuple[int, int]) -> np.ndarray:
        """convert rle encoding to binary mask

        Args:
            rle (str)
            shape (Tuple[int, int])

        Returns:
            np.ndarray: mask
        """
        rle = rle["counts"]
        # force even number of elem
        if not len(rle) % 2 == 0:
            rle.append(0)
        width, height = shape[:2]

        mask = np.zeros(width * height).astype(np.uint64)

        array = np.asarray(rle)
        starts = array[0::2]
        lengths = array[1::2]

        current_position = 0
        for i, start in enumerate(starts):
            current_position += start
            mask[current_position : int(current_position + lengths[i])] = 1
            current_position += lengths[i]

        return mask.reshape(height, width).T

    def __len__(self) -> int:
        return len(self.annot_dict["images"])

    def export_annotation(
        self,
        image_name: str,
        image: Tensor,
        format: BaseFormat,
        categories: Dict[int, str],
    ) -> Tuple[str, Dict[Any, Any]]:
        """from image, image name, categories and target (as BaseFormat) returns a writeable coco dict.

        Args:
            image_name (str)
            image (Tensor)
            format (BaseFormat)
            categories (Dict[int, str]): Dict of label / category name correspondance

        Returns:
            Tuple[str, Dict[Any, Any]]: image_name, coco dict
        """
        format.device = "cpu"
        images = [
            {
                "file_name": image_name,
                "height": image.shape[-2],
                "width": image.shape[-1],
                "id": 0,
            }
        ]
        categories = [{"name": k, "id": v} for v, k in categories.items()]
        anns = []
        for i in range(format.nb_object):
            obj, _ = format[i]
            # if no object, stop loop
            if obj.nb_object == 0:
                break
            # retrieve mask/box and label
            label = obj.labels.item()
            obj.device = "cpu"
            ann_dict = {"id": 0, "image_id": 0, "category_id": label}
            if isinstance(obj, InstanceMaskFormat):
                bboxes: BboxData = BboxData.from_mask(obj.data)
                bboxes.format = "XYWH"
                bboxes.device = "cpu"
                bboxes: Tensor = bboxes.value
                bboxes_coco = bboxes.numpy()[0]
                bboxes_coco = [int(b) for b in bboxes_coco]
                contours, _ = cv2.findContours(
                    obj.data.value.numpy().astype(np.uint8),
                    cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_NONE,
                )
                contours = [c.reshape(-1).tolist() for c in contours]
                ann_dict.update({"bbox": bboxes_coco, "segmentation": contours})
            elif isinstance(obj, BboxFormat):
                obj.data.format = "XYWH"
                bboxes = obj.data.value
                bboxes_coco = bboxes.numpy()[0]
                bboxes_coco = [int(b) for b in bboxes_coco]
                ann_dict.update({"bbox": bboxes_coco})
            anns.append(ann_dict)
        coco_dict = {"categories": categories, "images": images, "annotations": anns}
        return image_name, coco_dict

    def group_export(
        self,
        sub_anns_dir: Union[str, Path],
        destination: Union[str, Path],
        categories: Dict[int, str],
    ):
        """Final layer of export dataset function. Here looks at all individual json files and merge them to coco_annotations.json

        Args:
            sub_anns_dir (Union[str, Path])
            destination (Union[str, Path])
            categories (Dict[int, str])
        """
        categories = [{"name": k, "id": v} for v, k in categories.items()]
        grouped_dict = {"categories": categories, "images": [], "annotations": []}
        jsons_list = sub_anns_dir.glob("*.json")
        jsons_list = [json.as_posix() for json in jsons_list]
        img_idx = 0
        ann_idx = 0
        for j_file in tqdm(jsons_list, desc="Grouping jsons : "):
            with open(j_file) as f:
                d = json.load(f)
            d["images"][0]["id"] = img_idx
            grouped_dict["images"].append(d["images"][0])
            for i in range(len(d["annotations"])):
                d["annotations"][i]["id"] = ann_idx
                d["annotations"][i]["image_id"] = img_idx
                grouped_dict["annotations"].append(d["annotations"][i])
                ann_idx += 1
            img_idx += 1
        with open(destination, "w") as f:
            json.dump(grouped_dict, f)
