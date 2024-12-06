from __future__ import annotations
from abc import ABC, abstractmethod
from torch import Tensor
from typing import Union, Literal, Tuple
from torchvision.tv_tensors import BoundingBoxes, Mask, BoundingBoxFormat
from torchvision.transforms.v2 import ConvertBoundingBoxFormat
import detectools.formats.errors as er
from detectools import Configuration
from torchvision.transforms.v2.functional import (
    crop_bounding_boxes,
    pad_bounding_boxes,
    pad_mask,
    crop_mask,
)
import torch
import copy
import detectools.formats.utils as ut
from torchvision.transforms.v2 import Transform


class BaseData(ABC):
    """Abstract class for base data."""

    # abstract class method

    @classmethod
    def empty(cls, canvas_size) -> BaseData:
        pass

    # abstract method

    @abstractmethod
    def crop(self, t: int, l: int, h: int, w: int) -> Tuple[BaseData, Tensor]:
        pass

    @abstractmethod
    def pad(self, t: int, l: int, r: int, b: int) -> Tuple[BaseData, Tensor]:
        pass

    @abstractmethod
    def __getitem__(
        self, indexes: Union[int, Tensor, slice]
    ) -> Tuple[BaseData, Tensor]:
        pass

    @abstractmethod
    def sanitize(self) -> Tuple[BaseData, Tensor]:
        pass

    @abstractmethod
    def __add__(self, obj2: BaseData) -> BaseData:
        pass

    @abstractmethod
    def apply_augmentation(
        self, image: Tensor, transform: Transform
    ) -> Tuple[BaseData, Tensor, Tensor]:
        """Need to be defined in concrete class : apply augmentation on it

        Args:
            image (``Tensor``): image to augment
            transform (``Transform``) : torchvision transform v2 augmentation

        Returns:
            ``Tuple[BaseData, Tensor, Tensor]``:
                - transformed BaseData, present tensor, transformed image
        """
        pass

    # concrete property

    @property
    def value(self):
        return self._value

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, val):
        assert val in ["cpu", "cuda"], f"device is not one of cuda nor cpu, got {val}"
        self._device = val
        self._value = self._value.to(val)

    @property
    def nb_object(self):
        return self._nb_objects

    @nb_object.setter
    def nb_object(self, v):
        raise er.ProtectedAttributeException()

    @property
    def canvas_size(self):
        return self._canvas_size

    @canvas_size.setter
    def canvas_size(self, v):
        raise er.ProtectedAttributeException()

    # abstract property

    @value.setter
    @abstractmethod
    def value(self, val):
        pass


class BboxData(BaseData):
    """Bounding box data class (child of BaseData)

    Args:
        bbox (Union[BoundingBoxes, Tensor]): tensor value of bounding box. Shape must be [N, 4]
        format (Literal[&quot;XYXY&quot;, &quot;XYWH&quot;, &quot;CXCYWH&quot;], optional): format of created BoundingBox. Defaults to "XYXY".
        canvas_size (Tuple[int, int], optional): Size of associated image [h, w]. Defaults to None.

    Attributes
    ----------

    Properties:
        - device (``Literal[&quot;cpu&quot;, &quot;cuda&quot;]``)
        - value (``BoundingBoxes``): Tensor value of bounding box
        - format (Literal[&quot;XYXY&quot;, &quot;XYWH&quot;, &quot;CXCYWH&quot;]): if changed directly will automatically re-derive value
        - nb_objects (``int``): number of objects contained.
        - canvas_size (Tuple[int, int])


    **Methods**:
    """

    @classmethod
    def from_mask(cls, mask: Union[InstanceMaskData, Tensor]) -> BboxData:
        """Generate BboxData object from mask

        Args:
            mask (``Union[InstanceMaskData, Tensor]``)

        Returns:
            ``BboxData``

        """
        assert isinstance(mask, Tensor) or (
            mask,
            InstanceMaskData,
        ), f"Invalid mask type, must be InstanceMaskData or Tensor got : {type(mask)}"
        mask = InstanceMaskData(mask) if isinstance(mask, Tensor) else mask
        # verify if object present in mask, if not -> empty BboxData
        if mask.nb_object == 0:
            return BboxData.empty(mask.canvas_size)
        # create one hot for masks_to_boxes and ignore 0 encoding (background)
        boxes = ut.mask2boxes(mask.value)
        bbox = BboxData(boxes, format="XYXY", canvas_size=mask.canvas_size)
        bbox.device = Configuration().device
        return bbox

    @classmethod
    def empty(cls, canvas_size: Tuple[int, int]) -> BboxData:
        """Return an empty BboxData with value = Tensor of shape [0, 4]

        Args:
            canvas_size (Tuple[int, int]): size of associated image.

        Returns:
            BboxData: empty BboxData
        """
        er.check_canvas_size(canvas_size)
        bbox = BoundingBoxes(
            torch.empty((0, 4)), canvas_size=canvas_size, format="XYXY"
        )
        return BboxData(bbox)

    @classmethod
    def _create_bbox(
        cls,
        bbox: Union[BoundingBoxes, Tensor],
        format: Literal["XYXY", "XYWH", "CXCYWH"] = None,
        canvas_size: Tuple[int, int] = None,
    ) -> BoundingBoxes:
        """Check sanity and create bbox object in __init__

        Args:
            bbox (``Union[BoundingBoxes, Tensor]``): torchvision BoundingBoxes object or Tensor. Shape must be [N, 4]
            format (``Literal[&quot;XYXY&quot;, &quot;XYWH&quot;, &quot;CXCXWH&quot;]``, **optional**):  Defaults to None.
            canvas_size (``Tuple[int, int]``, **optional**): Defaults to None.

        Returns:
            ``BoundingBoxes``:
                - A sane BoundingBoxes object
        """

        if not (
            isinstance(bbox, BoundingBoxes) or (canvas_size != None and format != None)
        ):
            raise er.BboxFormatException(bbox, format, canvas_size)

        er.check_bbox_dim(bbox)

        if not (isinstance(bbox, BoundingBoxes)):
            bbox = BoundingBoxes(bbox, format=format, canvas_size=canvas_size)
        if bbox.format != format:
            converter = ConvertBoundingBoxFormat(format)
            bbox = converter(bbox)
        return bbox

    def __init__(
        self,
        bbox: Union[BoundingBoxes, Tensor],
        format: Literal["XYXY", "XYWH", "CXCYWH"] = "XYXY",
        canvas_size: Tuple[int, int] = None,
    ):
        bbox.to(torch.uint8)
        bbox = BboxData._create_bbox(bbox, format, canvas_size)
        self._format = bbox.format
        self._canvas_size = bbox.canvas_size
        self._value = bbox
        self._nb_objects = self.value.shape[0]
        self.device = Configuration().device

    def __getitem__(self, indexes: int | Tensor | slice) -> Tuple[BboxData, Tensor]:
        # Handles empty self and empty Tensor indices (empty slice not handled):
        # - indexes is empty -> return empty BboxData, self is empty return copy of self whatever indexes
        if self.nb_object == 0:
            return self, torch.tensor([])
        indexes = torch.arange(self.nb_object).to(self.device)[indexes]
        if indexes.nelement() == 0:
            new_bbox = BboxData.empty(self.canvas_size)
            new_bbox.format = self.format
        else:
            new_bbox = BoundingBoxes(
                self.value[indexes],
                canvas_size=self.canvas_size,
                format=self.format,
            )
            new_bbox = BboxData(new_bbox)
        new_bbox, present = new_bbox.sanitize()
        present = present.to(self.device)
        indexes = indexes.view(1) if indexes.dim() == 0 else indexes
        present = present if present.nelement() == 0 else indexes[present]
        return new_bbox, present

    @BaseData.value.setter
    def value(self, val: Union[Tensor, BoundingBoxes]):
        """When changing bounding box value : if BoundingBoxes -> change all adequate params (format, canvas_size, nb_objects etc.) otherwise replace Tensor value but preserve formats"""
        er.check_bbox_dim(val)
        bbox = val.to(self.device)
        if isinstance(bbox, BoundingBoxes):
            self._format = bbox.format
            self._canvas_size = bbox.canvas_size
            self._nb_objects = bbox.shape[0]
            self._value = bbox
        elif isinstance(bbox, Tensor):
            self._value = BoundingBoxes(
                bbox, format=self._format, canvas_size=self._canvas_size
            )
            self._nb_objects = bbox.shape[0]
        else:
            raise er.BboxFormatException(bbox, None, None)

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, f: Union[str, BoundingBoxFormat]):
        f = f if isinstance(f, BoundingBoxFormat) else BoundingBoxFormat(f)
        self._format = f
        convert = ConvertBoundingBoxFormat(f)
        self.value = convert(self.value)

    def crop(self, t: int, l: int, h: int, w: int) -> Tuple[BboxData, Tensor]:
        """Crop the BboxData object and update values, canvas etc.
        Note : forcing XYXY format to be compatible with torchvision func but restore format after.

        Args:
            t (``int``): top coordinate of crop
            l (``int``): left coordinate of crop
            h (``int``): height value of crop
            w (``int``): width value of crop
        """
        er.check_crop_coords(self, t, l, h, w)

        old_format = self.format
        # change format to be compatible with torch vision
        self.format = "XYXY"
        new_bbox, new_canvas = crop_bounding_boxes(
            self.value, self.format, top=t, left=l, height=h, width=w
        )
        # restore format
        self.format = old_format
        # create output BboxData
        cropped_bbox = BoundingBoxes(new_bbox, format="XYXY", canvas_size=new_canvas)
        cropped_bbox = BboxData(cropped_bbox)
        cropped_bbox.device = self.device
        cropped_bbox.format = self.format
        cropped_bbox, present = cropped_bbox.sanitize()
        return cropped_bbox, present

    def pad(self, t: int, l: int, r: int, b: int) -> Tuple[BboxData, Tensor]:
        """Pad the ``BboxData`` object and update values, canvas etc.
        Note : forcing XYXY format to be compatible with torchvision func but restore format after.

        Args:
            t (``int``): top value of crop
            l (``int``): left value of crop
            r(``int``): right value of crop
            b (``int``): bottom value of crop
        """

        old_format = self.format
        self.format = "XYXY"
        # Ordering top, left inversed in torchvision crop vs pad in torchvision
        new_bbox, new_canvas = pad_bounding_boxes(
            self.value, self.format, self.canvas_size, list((l, t, r, b))
        )
        # restore format
        self.format = old_format
        # create output BboxData
        padded_bbox = BoundingBoxes(new_bbox, format="XYXY", canvas_size=new_canvas)
        padded_bbox = BboxData(padded_bbox)
        padded_bbox.device = self.device
        padded_bbox.format = self.format
        padded_bbox, present = padded_bbox.sanitize()
        return padded_bbox, present

    def sanitize(self) -> Tuple[BboxData | Tensor]:
        """remove boxes with width or height = 0
        returns as well a tensor of kept objects (useful for labels handling in BaseFormat)
        """
        boxes = copy.deepcopy(self)
        boxes.format = "XYWH"
        test_h_w_zero = boxes.value[:, 2:] == 0
        to_keep = torch.tensor(
            [torch.logical_not(torch.any(test)) for test in test_h_w_zero]
        )
        # infer from it indexes of removed objs
        present = torch.arange(to_keep.shape[0]).to(self.device)
        if present.nelement() != 0 and to_keep.nelement() != 0:
            present = present[to_keep]
        else:
            present = torch.tensor([])
        if present.nelement() != 0:
            boxes.value = boxes.value[to_keep]
            boxes.format = self.format
            return boxes, present
        else:
            return BboxData.empty(boxes.canvas_size), present

    def __add__(self, obj2: BboxData) -> BboxData:
        assert isinstance(
            obj2, BboxData
        ), f"Can't add object of type {type(obj2)} to object BboxData."
        assert (
            self.canvas_size == obj2.canvas_size
        ), "Bbox data do not have same canvas_size, can't add them."
        if self.format != obj2.format:
            self.format = "XYXY"
            obj2.format = "XYXY"
        new_boxes = torch.cat([self.value, obj2.value], dim=0)
        return BboxData(new_boxes, self.format, self.canvas_size)

    def apply_augmentation(
        self, image: Tensor, transform: Transform
    ) -> Tuple[BboxData, Tensor, Tensor]:
        """Apply transform on self and associated image

        Args:
            image (``Tensor``)
            transform (``Transform``)

        Returns:
            ``Tuple[BboxData, Tensor, Tensor]``:
                - augmented data, present Tensor, image
        """
        old_format = self.format
        self.format = "XYXY"
        augmented_img, augmented_value = transform(image, self.value)
        augmented_data, present = BboxData(augmented_value).sanitize()
        self.format = old_format
        return augmented_data, present, augmented_img


class InstanceMaskData(BaseData):
    """Instance segmentation data class (Child class of BaseData)

    Args:
        mask (Union[Mask, Tensor]): Stacked mask (Tensor) of shape [H, W]. Each object is indexed in [1...N] range.

    Attributes
    ----------

    Properties:
        - device (``Literal[&quot;cpu&quot;, &quot;cuda&quot;]``)
        - value (``BoundingBoxes``): Tensor value of stacked instance mask
        - nb_objects (``int``): number of objects contained.
        - canvas_size (Tuple[int, int]): dim of mask (h, w)


    **Methods**:
    """

    @classmethod
    def empty(cls, canvas_size):
        """generate empty instance mask (full of 0) with given canvas_size"""
        er.check_canvas_size(canvas_size)
        mask = torch.zeros(canvas_size)
        return InstanceMaskData(mask)

    @classmethod
    def from_binary_masks(cls, mask: Tensor) -> InstanceMaskData:
        """Generate InstanceMaskData from one_hot (binary) mask of shape [N, H, W] where N = number of objects. Note that background must not be included.

        Args:
            mask (Tensor): one hot mask of shape [N, H, W]

        Returns:
            InstanceMaskData: Stacked InstanceMaskData
        """
        assert (
            mask.dim() == 3
        ), f"Mask is not in (N_obj, h, w) format. Got shape {mask.shape}"
        stacked = torch.zeros(mask.shape[-2:]).to(mask.device)
        for i, m in enumerate(mask):
            stacked, _ = torch.max(torch.stack([m * (i + 1), stacked]), dim=0)
        return InstanceMaskData(stacked)

    def __init__(
        self,
        mask: Union[Mask, Tensor],
    ):
        er.check_mask_dim(mask)
        mask = mask.long()
        self._value = mask if isinstance(mask, Mask) else Mask(mask)
        self._canvas_size = (self._value.shape[0], self._value.shape[1])
        self._nb_objects = torch.max(self.value).item()
        self.device = Configuration().device

    @BaseData.value.setter
    def value(self, val: Union[Tensor, Mask]):
        er.check_mask_dim(val)
        self._mask = val if isinstance(val, Mask) else Mask(val)
        self._canvas_size = (val.shape[0], val.shape[1])
        self._nb_objects = torch.max(val)

    def _reindex(self) -> Tuple[InstanceMaskData, Tensor]:
        """If missing object in mask reidex accordingly

        Returns:
            ``Tuple[InstanceMaskData, Tensor]``:
                - reindexed InstanceMaskData, id of objects which are present (CAREFUL : 0 is written as 1 in stacked mask, here we index per object not mask)
        """
        if self.nb_object == 0:
            return self, torch.tensor([])
        unique = torch.unique(self.value)
        should_be = range(1, self.nb_object + 1)
        # present will have values in [0, N_obj-1]
        present = torch.tensor(
            [i for i, val in enumerate(should_be) if (val in unique)]
        )
        new_mask = copy.deepcopy(self.value)
        for i, u in enumerate(unique):
            new_mask[self.value == u] = i
        # reindex from mask object id to object id
        return InstanceMaskData(new_mask), present.to(new_mask.device)

    def _remove_small_objects(self) -> Tuple[InstanceMaskData, Tensor]:
        """remove all small objects from mask. Handles splitted_mask_handling option

        Returns:
            ``Tuple[InstanceMaskData, Tensor]``:
                - new InstanceMaskData without small objects, id of objects which were kept (CAREFUL : 0 is written as 1 in stacked mask, here we index per object not mask)
        """
        if Configuration().splitted_mask_handling:
            return self.__remove_small_objs_with_splitting()
        else:
            return self.__remove_small_objs_no_splitting()

    def __remove_small_objs_no_splitting(self) -> Tuple[InstanceMaskData, Tensor]:
        """Handles cleaning of small objects in case of no mask splitting handling option

        Returns:
            Tuple[InstanceMaskData, Tensor]: cleaned_mask, indices of kept objects
        """
        msk_threshold = Configuration().mask_min_size
        new_mask = copy.deepcopy(self.value)
        for i in torch.unique(self.value):
            # replace all values that occurence are smaller than mask threshold
            new_mask[new_mask == i] = (
                0 if torch.count_nonzero(self.value == i) < msk_threshold else i
            )
        new_mask, present = InstanceMaskData(new_mask)._reindex()
        return new_mask, present

    def __remove_small_objs_with_splitting(self) -> Tuple[InstanceMaskData, Tensor]:
        """Same as __remove_small_objs_no_splitting but includes a redefinition of objects that are discontinuous as new objects.
        This leads to duplicated original object indices in the returned <present> Tensor.

        Returns:
            Tuple[InstanceMaskData, Tensor]: cleaned_mask, indices of kept objects
        """
        new_mask: Tensor = copy.deepcopy(self.value)
        new_mask, present = ut.reindex_mask_with_splitted_objects(new_mask)
        new_mask = InstanceMaskData(new_mask)
        new_mask, keep = new_mask.__remove_small_objs_no_splitting()
        if present.nelement() != 0 and keep.nelement() != 0:
            present = present[keep]
        # The minus 1 is for reidexing the objects from 0 to N-1 (while masks are from 1 to N_objs)
        return new_mask, present - 1

    def sanitize(self) -> Tuple[InstanceMaskData, Tensor]:
        """reindex and remove all small objects from mask

        Returns:
            ``Tuple[InstanceMaskData, Tensor]``:
                - new InstanceMaskData without small objects, id of objects which were removed because too small (CAREFUL : 0 is written as 1 in stacked mask, here we index per object not mask)
        """
        new_mask, _ = self._reindex()
        new_mask, present = self._remove_small_objects()
        return new_mask, present

    def __getitem__(
        self, indexes: int | Tensor | slice
    ) -> Tuple[InstanceMaskData, Tensor]:
        if self.nb_object == 0:
            return self, torch.tensor([])
        indexes = torch.arange(self.nb_object).to(self.device)[indexes]
        if indexes.nelement() == 0:
            empty = InstanceMaskData.empty(self.canvas_size)
            empty.device = self.device
            return empty, torch.tensor([]).to(self.device)
        mask = torch.zeros(self.canvas_size).to(self.value.dtype).to(self.device)
        new_objects = torch.arange(0, self.nb_object, dtype=torch.uint8).to(
            self.device
        )[indexes]
        for i in new_objects.view(-1):
            mask[self.value == i + 1] = (i + 1).to(self.value.dtype)
        newmask, present = InstanceMaskData(mask).sanitize()
        present = present.to(self.device)
        # after sanitize, objects might be removed : reindex new_objects if are in present
        present = new_objects.view(-1)[[n in present for n in new_objects.view(-1)]]
        newmask.device = self.device
        return newmask, present

    def __add__(self, obj2: InstanceMaskData) -> InstanceMaskData:
        """Return new mask from 2 InstanceMaskData object. NB : This loose overlapping mask information"""
        assert isinstance(
            obj2, InstanceMaskData
        ), f"Can't add object of type {type(obj2)} to object InstanceMaskData."
        assert (
            self.canvas_size == obj2.canvas_size
        ), "InstanceMaskData data do not have same canvas_size, can't add them."
        reindex_new_mask = obj2.value
        reindex_new_mask[reindex_new_mask != 0] += self.nb_object
        # extract max of masks. NB : this lose overlapping mask information !!
        new_mask, _ = torch.max(torch.stack([self.value, reindex_new_mask]), dim=0)
        return InstanceMaskData(new_mask)

    def pad(self, t: int, l: int, r: int, b: int) -> Tuple[InstanceMaskData, Tensor]:
        """Pad InstanceMaskData to desired coordinates. Note : the order t, l, r, b is different between detectools and torchvision.

        Args:
            t (int): top padding
            l (int): left padding
            r (int): right padding
            b (int): bottom padding

        Returns:
            Tuple[InstanceMaskData, Tensor]: padded InstanceMaskData, indices of present objects
        """
        padded_mask = copy.deepcopy(self.value)
        # Ordering top, left inversed in torchvision crop vs pad in torchvision
        new_mask_data = InstanceMaskData(pad_mask(padded_mask, (l, t, r, b)))
        new_mask_data.device = self.device
        new_mask_data, present = new_mask_data.sanitize()
        return new_mask_data, present

    def crop(self, t: int, l: int, h: int, w: int) -> Tuple[InstanceMaskData, Tensor]:
        """Crop InstanceMaskData to desired coordinates.

        Args:
            t (int): top crop coord
            l (int): left crop coord
            h (int): height of crop
            w (int): width of crop

        Returns:
            Tuple[InstanceMaskData, Tensor]: padded InstanceMaskData, indices of present objects
        """
        cropped_mask = copy.deepcopy(self.value)
        new_mask_data = InstanceMaskData(crop_mask(cropped_mask, t, l, h, w))
        new_mask_data.device = self.device
        new_mask_data, present = new_mask_data.sanitize()
        return new_mask_data, present

    def apply_augmentation(
        self, image: Tensor, transform: Transform
    ) -> Tuple[InstanceMaskData, Tensor, Tensor]:
        """Apply transform on self and associated image

        Args:
            image (``Tensor``)
            transform (``Transform``)

        Returns:
            ``Tuple[InstanceMaskData, Tensor, Tensor]``:
                - augmented data, present Tensor, image
        """
        augmented_img, augmented_value = transform(image, self.value)
        augmented_data, present = InstanceMaskData(augmented_value).sanitize()
        return augmented_data, present, augmented_img
