from torch.nn import Module
from typing import Union, Any, Tuple, Dict
from torch import Tensor
from detectools.formats import BatchedFormat
from abc import ABC, abstractmethod


class BaseModel(Module, ABC):
    """Base Class for detectools models.

    Attributes
    ----------

    Attributes:
        - confidence_thr (``float``): Confidence score threshold to consider object as true prediction.
        - model_max_detection (``int``): Maximum number of object to predict on one image.
        - model_nms_threshold (``float``): IoU threshold to consider 2 boxes as overlapping for Non Max Suppression algorithm.
        - num_classes (``int``): Number of classes.


    **Methods**:
    """

    @property
    def device(self):
        """Send model to device.

        Args:
            device (``Literal['cpu', 'cuda']``): Device to send model on.
        """
        return self._device

    @device.setter
    def device(self, val):
        self.to(val)
        self._device = val

    @abstractmethod
    def prepare(
        self, images: Tensor, targets: BatchedFormat = None
    ) -> Union[Any, Tuple[Any]]:
        """Transform images and targets into model specific format for prediction & loss computation.

        Args:
            images (``Tensor``): Batch images.
            targets (``BatchedFormats``, **optional**): Batched targets from DetectionDataset.

        Returns:
            ``Union[Any, Tuple[Any]]``:
                - Images data prepared for model.
                - If targets: images + targets prepared for model.
        """

    @abstractmethod
    def build_results(self, raw_outputs: Any) -> BatchedFormat:
        """Transform model outputs into BaseFormat for results.
        This function also apply instances selection on results according to args:

        - confidence_thr
        - model_max_detection
        - model_nms_threshold

        Args:
            raw_outputs (``Any``): Model outputs.

        Returns:
            ``BatchedFormats``:
                - Model output for batch.
        """

    @abstractmethod
    def get_predictions(self, images: Tensor) -> BatchedFormat:
        """Prepare images, Apply model forward pass and build results.

        Args:
            images (``Tensor``): RGB images Tensor.

        Returns:
            ``BatchedFormats``:
                - Predictions for images as BatchedFormats.
        """

    @abstractmethod
    def run_forward(
        self, images: Tensor, targets: BatchedFormat
    ) -> Union[Dict[str, Tensor], Tuple[Dict[str, Tensor], BatchedFormat]]:
        """Compute loss from images and if target passed, compute loss & return both loss dict
        and results.

        Args:
            images (``Tensor``): Batch RGB images.
            targets (``BatchedFormats``): Batch targets.
            predict (``bool``, **optional**): To return predictions or not. Defaults to False.

        Returns:
            ``Union[Dict[str, Tensor], Tuple[Dict[str, Tensor], BatchedFormats]]``:
                - Loss dict.
                - If predict: Predictions.
        """
