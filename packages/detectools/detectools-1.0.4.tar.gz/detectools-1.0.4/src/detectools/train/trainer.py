from detectools.models.basemodel import BaseModel
from torch.optim import Optimizer
from detectools import Configuration
from typing import Literal, Dict, Tuple, List, Union
from torch import Tensor
from detectools.formats import BatchedFormat
from detectools.data import DetectLoader
from tqdm import tqdm
import torch
from torchmetrics import Metric
from detectools.metrics.base_metric import (
    DetectMetric,
    ClassWiseDetectMetric,
    SemanticSegmentationMetric,
    ClassifMetric,
)
from torch.utils.tensorboard import SummaryWriter
from pathlib import Path
import shutil


class Trainer:
    """Class that handles training in detectools. Handles train / valid epochs, monitoring (via tensorboard) and metrics computation.

    Args:
        model (``BaseModel``): detectools model.
        optimizer (``Optimizer``): torch optimizer (Ex: Adam())
        metrics (``List[Union[DetectMetric, ClassWiseDetectMetric, SemanticSegmentationMetric, ClassifMetric]]``, **optional**): List of detectools metrics. Check available metrics in detectools.metrics.available_metrics Defaults to [].
        log_dir (``str``, **optional**): tensorboard output directory. If "" no monitoring is provided. Defaults to "".


    Example:
    ----------

    .. highlight:: python
    .. code-block:: python
        >>> from detectools import DetectDataset, DetectLoader, Trainer
        >>> from torch.optim import Adam
        >>> model = Yolov8()
        >>> optim = Adam(model.parameters(), 1e-4)
        >>> train_set, valid_set, _ = DetectDataset(dataset_path=data_path).split((0.8, 0.2, 0))
        >>> trainer = Trainer(model, optim, metrics=[DetectF1score()], log_dir="test_dir")
        >>> train_loader = DetectLoader(train_set, batch_size=6)
        >>> valid_loader = DetectLoader(valid_set, batch_size=6)
        >>> for e in range(N_epoch):
        >>>     trainer.train_epoch(train_loader, e)
        >>>     trainer.valid_epoch(valid_loader, e)


    Attributes
    ----------

    Attributes:
        - model (``BaseModel``): detectools model.
        - optimizer (``Optimizer``): torch optimizer (Ex: Adam())
        - metrics (``List[Union[DetectMetric, ClassWiseDetectMetric, SemanticSegmentationMetric, ClassifMetric]]``, **optional**): List of detectools metrics. Check available metrics in detectools.metrics.available_metrics Defaults to [].
        - board (``SummaryWriter``): tensorboard output directory.

    Attributes
    ----------

    Properties:
        - device (``Literal[&quot;cpu&quot;, &quot;cuda&quot;]``) : the setter move evrything that's needed to desired device.


    **Methods**

    """

    def __init__(
        self,
        model: BaseModel,
        optimizer: Optimizer,
        metrics: List[
            Union[
                DetectMetric,
                ClassWiseDetectMetric,
                SemanticSegmentationMetric,
                ClassifMetric,
            ]
        ] = [],
        log_dir="",
    ):

        self.model = model
        self.optimizer = optimizer
        self.log_dir = log_dir
        self.device = Configuration().device
        self.metrics: List[
            Union[
                DetectMetric,
                ClassWiseDetectMetric,
                SemanticSegmentationMetric,
                ClassifMetric,
            ]
        ] = [m.to(self.device) for m in metrics]
        # create log dir and board for tensorboard
        if log_dir:
            # if log dir exist remove it
            if Path(log_dir).exists():
                shutil.rmtree(log_dir)

            Path(log_dir).mkdir(parents=True)
            self.board = SummaryWriter(log_dir)
        else:
            self.board = False

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, val: Literal["cpu", "cuda"]):
        self.model.device = val
        self._device = val

    def train_step(self, images: Tensor, targets: BatchedFormat) -> Dict[str, Tensor]:
        """Run forward pass, loss computation and backward pass.

        Args:
            images (``Tensor``): Batch images
            targets (``BatchedFormat``): Batch targets.

        Returns:
            ``Dict[str, Tensor]``:
                - Dict of losses containing (total loss at key 'loss').
        """
        assert self.model.training, "model is not in train mode for train_step"
        loss_dict = self.model.run_forward(images, targets)
        loss = loss_dict["loss"]
        loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad()
        return loss_dict

    def valid_step(
        self, images: Tensor, targets: BatchedFormat
    ) -> Tuple[Dict[str, Tensor], Dict[str, Dict[str, Tensor]]]:
        """Run forward, compute metrics, return loss dict and metrics.

        Args:
            images (``Tensor``): Batch images.
            targets (``BatchedFormat``): Targets.

        Returns:
            ``Tuple[Dict[str, Tensor], Dict[str, Dict[str, Tensor]]]``:
                - Losses and metrics values.
        """
        assert not (self.model.training), "model is not in valid mode for valid_step"
        loss_dict, predictions = self.model.run_forward(images, targets)
        metrics = self.compute_metrics(predictions, targets)
        return loss_dict, metrics

    def epoch(
        self,
        loader: DetectLoader,
        ep_number: int,
        tag: str = "",
    ) -> Dict[str, Tensor]:
        """Run trainning epoch.

        Args:
            loader (``DetectLoader``): DetectLoader.
            ep_number (``int``): Epoch number.
            tag (``str``, **optional**): Tag to link to epoch. Defaults to "".

        Returns:
            ``Dict[str, Tensor]``:
                - Epochs values (Losses & metrics).
        """
        # create aggregator for loss averged accros samples
        loss_aggregator = Aggregator()
        iterator = tqdm(loader, total=len(loader), desc=f"Epoch {ep_number}/{tag}")
        # iterate over batches
        for images, targets, _ in iterator:
            batch_size = images.shape[0]
            # send to device
            images = images.to(self.device)
            targets: BatchedFormat
            # gather loss & metrics (if valid)
            if self.model.training:
                loss_dict = self.train_step(images, targets)
                loss_aggregator(loss_dict, batch_size)
                epoch_dict = loss_aggregator.compute()
            else:
                loss_dict, metric_dict = self.valid_step(images, targets)
                loss_aggregator(loss_dict, batch_size)
                epoch_dict = loss_aggregator.compute()
                epoch_dict.update(metric_dict)
            # extract str from log to display in terminal
            log_str = self.log_string(epoch_dict)
            iterator.set_postfix_str(f"{log_str}")
        for metric in self.metrics:
            metric.reset()
        if self.log_dir:
            for key, value in epoch_dict.items():
                if isinstance(value, dict):
                    self.board.add_scalars(key, value, ep_number)
                else:
                    self.board.add_scalars(key, {tag: value}, ep_number)

        return epoch_dict

    def train_epoch(
        self, loader: DetectLoader, ep_number: int, tag: str = "Train"
    ) -> Dict[str, Tensor]:
        """Run train epoch.

        Args:
            loader (``DetectionLoader``): DetectionLoader.
            ep_number (``int``): Epoch number.
            tag (``str``, **optional**): Tag to link to epoch. Defaults to "Train".

        Returns:
            ``Dict[str, Tensor]``:
                - Epochs values (Losses).
        """
        self.model.train()
        epoch_dict = self.epoch(loader, ep_number, tag=tag)
        return epoch_dict

    def valid_epoch(
        self, loader: DetectLoader, ep_number: int, tag: str = "Valid"
    ) -> Dict[str, Tensor]:
        """Run train epoch.

        Args:
            loader (``DetectionLoader``): DetectionLoader.
            ep_number (``int``): Epoch number.
            tag (``str``, **optional**): Tag to link to epoch. Defaults to "Valid".

        Returns:
            ``Dict[str, Tensor]``:
                - Epochs values (Losses & metrics).
        """
        self.model.eval()
        with torch.no_grad():
            epoch_dict = self.epoch(loader, ep_number, tag=tag)
        return epoch_dict

    def log_string(self, epoch_dict: Dict[str, Tensor]) -> str:
        """Transform epoch dict in string.

        Args:
            epoch_dict (``Dict[str, Tensor]``): Dict of epoch values to display.

        Returns:
            ``str``:
                - String to print with epoch values.
        """
        flattened_dict = epoch_dict.copy()
        for key, value in flattened_dict.items():
            if isinstance(value, dict):
                flattened_dict[key] = value[list(value.keys())[0]]

        log = ""
        for key, value in flattened_dict.items():
            log += f"{key} : {str(round(value.item(), 3))} "

        return log

    def compute_metrics(self, predictions: BatchedFormat, targets: BatchedFormat):
        for metric in self.metrics:
            metric.update(predictions, targets)
        # after all updates recompute to get averaged values of metric
        metric_dict = {}
        for metric in self.metrics:
            results = metric.compute()
            metric_dict.update({metric.name: results})

        return metric_dict


class Aggregator:
    """Aggregator aggregate losses across batchs.

    Attributes:
    -----------

    Attributes:
        iterations (``int``): Number of iterations.
        losses (``Dict[str, Tensor]``): Dictionnary of epoch losses (over iterations).

    Methods:
    ----------
    """

    iterations: int
    losses: dict

    def __init__(self):
        self.iterations = 0
        self.losses: dict = None

    def update(self, batch_losses: Dict[str, Tensor]):
        """Update internal loss dict with new losses.

        Args:
            batch_losses (``Dict[str, Tensor]``): Dict of losses.
        """

        for key, value in self.losses.items():
            self.losses[key] = value + batch_losses[key]

    def __call__(self, batch_losses: Dict[str, Tensor], batch_size: int):
        """Update internal loss dict.

        Args:
            batch_losses (``Dict[str, Tensor]``): Dict of losses.
            batch_size (``int``): Batch size.
        """

        if self.losses:
            self.update(batch_losses)
        else:
            self.losses = batch_losses

        self.iterations += 1 * batch_size

    def compute(self) -> Dict[str, Tensor]:
        """Return loss dict with values divided by iterations (Mean accross samples).

        Returns:
            ``Dict[str, Tensor]``:
                - Losses over iterations.
        """

        out_dict = {
            key: (value / self.iterations) for key, value in self.losses.items()
        }
        return out_dict
