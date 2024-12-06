from __future__ import annotations
from typing import Tuple
from torch import Tensor
from detectools.formats.base_data import InstanceMaskData, BboxData
from detectools.formats.base_formats import BaseFormat
import torch
import detectools.formats.errors as er
from typing import Union, List, Literal
from detectools import Configuration


class InstanceMaskFormat(BaseFormat):
    """Class for Instance Segmentation Format (Child class of *BaseFormat*). contains *InstanceMaskData* value, labels and scores.

    Args:
        data (InstanceMaskData)
        labels (Tensor)
        scores (Tensor | None, optional). Defaults to None.

    Properties & attributes : cf *BaseFormat*


    **Methods**
    """

    @classmethod
    def empty(cls, canvas_size: Tuple[int, int]) -> InstanceMaskFormat:
        """Create an empty InstanceMaskFormat of dimension canvas_size

        Args:
            canvas_size (Tuple[int, int])

        Returns:
            InstanceMaskFormat
        """
        return InstanceMaskFormat(
            InstanceMaskData.empty(canvas_size), labels=torch.tensor([])
        )

    def __init__(
        self, data: InstanceMaskData, labels: Tensor, scores: Tensor | None = None
    ):

        assert isinstance(
            data, InstanceMaskData
        ), f"Expect to have InstanceMaskData data for InstanceMaskFormat, got {type(data)}."
        super().__init__(data, labels, scores)

    def export_semantic_mask(self) -> Tensor:
        """From self (data.value and labels) generate a semantic mask by replacing objects indexing by their corresponding labels.
        Note that labels are shifted by 1 as 0 is preserved for background

        Returns:
            ``Tensor``:
                - Semantic mask
        """
        inst_mask, _ = self.sanitize()
        semantic_mask = torch.zeros(self.canvas_size).to(self.device)
        semantic_mask = semantic_mask.long()
        if self.nb_object == 0:
            return semantic_mask
        for i, lab in enumerate(self.labels):
            semantic_mask[inst_mask.data.value == (i + 1)] = lab.item() + 1
        return semantic_mask


class BboxFormat(BaseFormat):
    """Class for Bounding box format (Child class of *BaseFormat*). contains *BBoxData* value, labels and scores.

    Args:
        data (BBoxData)
        labels (Tensor)
        scores (Tensor | None, optional). Defaults to None.

    Properties & attributes : cf *BaseFormat*


    **Methods**
    """

    @classmethod
    def from_instance_mask(cls, mask: InstanceMaskFormat) -> BboxFormat:
        """Create a BboxFormat from InstanceMaskFormat

        Args:
            mask (InstanceMaskFormat)

        Returns:
            BboxFormat
        """
        mask, _ = mask.sanitize()
        boxes = BboxFormat(BboxData.from_mask(mask.data), mask.labels, mask.scores)
        assert (
            mask.nb_object == boxes.nb_object
        ), "Different number of objects when creating boxes from instance masks, you may need to increase the mask_min_size parameter in Configuration()"
        return boxes

    @classmethod
    def empty(cls, canvas_size: Tuple[int]) -> BboxFormat:
        """Create an empty BboxFormat of dimension canvas_size

        Args:
            canvas_size (Tuple[int, int])

        Returns:
            BboxFormat
        """
        return BboxFormat(BboxData.empty(canvas_size), labels=torch.tensor([]))

    def __init__(self, data: BboxData, labels: Tensor, scores: Tensor | None = None):
        assert isinstance(
            data, BboxData
        ), f"Expect to have BboxData data for BboxFormat, got {type(data)}."
        super().__init__(data, labels, scores)


class BatchedFormat:
    """A class that handles a list of Formats

    Args:
        formats (``List[BaseFormat]``)

    Attributes
    ----------

    Properties:
        - device (``Literal[&quot;cpu&quot;, &quot;cuda&quot;]``): When changed, move all formats into same device.
        - formats (``List[BaseFormat]``): contains all stored formats.
        - size (``int``): number of formats


    **Methods**
    """

    def __init__(self, formats: List[BaseFormat]):

        formats_check = [isinstance(form, BaseFormat) for form in formats]
        assert all(
            formats_check
        ), f"Some targets are not Format, got {[type(form) for form in formats]}"
        self.formats: List[BaseFormat] = formats
        self.sanitize()

    def sanitize(self):
        """Apply sanitize to all formats"""
        self.formats = [form.sanitize()[0] for form in self.formats]

    @property
    def formats(self):
        return self._formats

    @formats.setter
    def formats(self, val: List[BaseFormat]):
        self._canvas_size = val[0].canvas_size if len(val) != 0 else None
        self._formats = val
        self._size = len(val)
        self.device = Configuration().device

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, val):
        for form in self.formats:
            form.device = val
        self._device = val

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        raise er.ProtectedAttributeException()

    def __getitem__(self, indexes: Union[int, slice, Tensor]) -> BatchedFormat:
        if isinstance(indexes, Tensor):
            if indexes.dtype == torch.bool:
                indexes = indexes.tolist()
            else:
                indexes = indexes.cpu().tolist()
                indexes = [i in indexes for i in range(len(indexes))]
        if isinstance(indexes, list):
            new_batch = [b for i, b in enumerate(self.formats) if indexes[i]]
        else:
            new_batch = self.formats[indexes]
        if not isinstance(new_batch, list):
            new_batch = [new_batch]
        return new_batch

    def set_bboxes_format(self, val: Literal["XYXY", "XYWH", "CXCYWH"]):
        for form in self.formats:
            assert isinstance(
                form, BboxFormat
            ), f"In BatchedFormat: can't change bbox format of object {type(form)}"
            form.data.format = val

    def __next__(self):
        _next: BaseFormat = next(self.__iter__())
        return _next

    def __iter__(self):
        return iter(self.formats)

    def __add__(self, form2: BatchedFormat):
        return BatchedFormat(self.formats + form2.formats)
