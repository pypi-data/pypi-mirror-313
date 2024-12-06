from ultralytics.cfg import get_cfg
from ultralytics.nn.tasks import attempt_load_one_weight, DetectionModel
from ultralytics.utils import DEFAULT_CFG
from detectools.models.basemodel import BaseModel
from typing import Literal
from detectools import Configuration
import detectools.models.yolov8.errors as er
import detectools.models.yolov8.utils as ut
from detectools.formats import (
    BatchedFormat,
    BboxData,
    InstanceMaskFormat,
    BboxFormat,
)
import torch
from typing import Dict, Tuple, Union, List
from torch import Tensor
import torchvision.transforms.v2.functional as F


class Yolov8(DetectionModel, BaseModel):
    """Yolov8 detection model. data_type must be either bbox or instance_mask to use this model.

    Args:
        architecture (``Literal[&quot;yolov8n&quot;, &quot;yolov8m&quot;, &quot;yolov8l&quot;, &quot;yolov8x&quot;]``, **optional**): Yolov8 model size. You can add "-p2" or "-p6" to load the p2 or p6 variants. Defaults to "yolov8n".
        pretrained (``bool``, **optional**): Use pretrained weights. Defaults to True.
        reg_max (``int``, **optional**): reg_max argument of yolov8 models (impacts object size detection). See ultralytics for more information. Defaults to 16.

    Attributes
    ----------

    Attributes:
        - criterion (``v8DetectionLoss``): Yolo loss from ultralytics.
        - args (``Any``) : ultralytics Yolo's configuration params.
        - pad_requirements (``int``) : pad requirements as per yolo (image shape multiple of 32 is the basic, but depends for p2 or p6). Note that is set automatically.

    Attributes
    ----------

    Properties:
        - device (``Literal["cuda", "cpu"]``): model's device


    **Methods**
    """

    def __init__(
        self,
        architecture: Literal[
            "yolov8n",
            "yolov8m",
            "yolov8l",
            "yolov8x",
            "yolov8n-p6",
            "yolov8m-p6",
            "yolov8l-p6",
            "yolov8x-p6",
            "yolov8n-p2",
            "yolov8m-p2",
            "yolov8l-p2",
            "yolov8x-p2",
        ] = "yolov8n",
        pretrained: bool = True,
        reg_max=16,
        *args,
        **kwargs,
    ):

        er.check_config(architecture, pretrained)
        config = Configuration()
        super().__init__(f"{architecture}.yaml", nc=config.num_classes, *args, **kwargs)
        self.args = get_cfg(DEFAULT_CFG)
        if pretrained:
            architecture = attempt_load_one_weight(
                f"{architecture}.pt",
            )
            self.load(architecture[0])
        self.criterion = self.init_criterion()
        self.device = config.device
        self.model[-1].reg_max = reg_max
        if "p6" in architecture:
            self.pad_requirements = 64
        elif "p2" in architecture:
            self.pad_requirements = 16
        else:
            self.pad_requirements = 32

    # overwrite
    @property
    def device(self):
        return self._device

    # overwrite
    @device.setter
    def device(self, val):
        self.to(val)
        self.criterion = self.init_criterion()

    def prepare_target(
        self, targets: BatchedFormat, img_size: Tuple[int, int]
    ) -> Dict[str, Tensor]:
        """Return target from BatchedFormat to ultralytics yolo format.

        Args:
            targets (BatchedFormat)
            img_size (Tuple[int, int])

        Returns:
            Dict[str, Tensor]: target as per ultralytics Yolo format.
        """
        # Convert to BboxFormat if there are InstanceMasks
        if any([isinstance(targ, InstanceMaskFormat) for targ in targets.formats]):
            forms = [
                (
                    BboxFormat.from_instance_mask(targ)
                    if isinstance(targ, InstanceMaskFormat)
                    else targ
                )
                for targ in targets
            ]
            targets = BatchedFormat(forms)
        targets.set_bboxes_format("CXCYWH")
        boxes = torch.cat([targ.data.value for targ in targets])
        boxes = ut.normalize_boxes(boxes, img_size)
        labels = torch.cat([targ.labels for targ in targets])[..., None]
        batch_idx = torch.cat(
            [torch.ones(targ.nb_object) * i for i, targ in enumerate(targets)]
        )[..., None]
        batch_idx = batch_idx.to(Configuration().device)
        return {"batch_idx": batch_idx, "cls": labels, "bboxes": boxes}

    def prepare(
        self, images: Tensor, targets: Union[BatchedFormat, None] = None
    ) -> Union[Tuple[Tensor, Dict], Tensor]:
        """Pad image / targets to fit yolo divisibility by 32 criterium and move targets to yolo format.
        If no targets passed simply returns images

        Args:
            images (``Tensor``): batched images [N, 3, H, W]
            targets (``Union[BatchedFormat, None]``)

        Returns:
            ``Union[Tuple[Tensor, Dict], Tensor]``:
                - Either : images_padded, yolo_targets OR images_padded
        """
        h, w = images.shape[-2], images.shape[-1]
        (t, l, r, b) = ut.yolo_pad_requirements(h, w, required=self.pad_requirements)
        # Note the inversion for torchvision pad coord ordinates : t <-> l
        images = F.pad(images, list((l, t, r, b)))
        if targets != None:
            targets = BatchedFormat([targ.pad(t, l, b, r)[0] for targ in targets])
            targets = self.prepare_target(targets, (h, w))
            return images, targets
        else:
            return images

    def build_results(
        self, raw_outputs: List[Tensor], prebuild_outputs: Tensor
    ) -> BatchedFormat:
        """Transform model outputs into Batch BboxFormat for results.

        Args:
            raw_outputs (``List[Tensor]``): Model outputs.
            prebuild_outputs (``Tensor``): Extracted boxes from outputs in eval mode.

        Returns:
            ``BatchedFormats``:
                - Batched predictions.
        """

        prebuild_outputs = prebuild_outputs.unbind()
        h, w = self.retrieve_spatial_size(raw_outputs)
        results = []
        # for each prediction
        for prediction in prebuild_outputs:
            # send pred in good pshape
            prediction = prediction.permute(1, 0)
            # get best class and corresponding score
            best_class = torch.argmax(prediction[:, 4:], dim=1)
            confidence, _ = torch.max(prediction[:, 4:], dim=1)
            # gather box cxcywh coordinates
            boxes = BboxData(prediction[:, :4], "CXCYWH", (h, w))
            # build result
            result = BboxFormat(boxes, best_class, scores=confidence)
            # objects selections
            result = ut.confidence_filter(result)
            result = ut.box_nms_filter(result)
            result, _ = result[: Configuration().model_max_detection]
            # stack batch results
            results.append(result)

        if len(results) == 0:
            results = []

        results = BatchedFormat(results)
        return results

    def compute_loss(
        self, raw_outputs: Tensor, targets: Dict[str, Tensor]
    ) -> Dict[str, Tensor]:
        """Compute loss with predictions & targets.

        Args:
            raw_outputs (``Any``): Raw output of model.
            targets (``DetectionFormat``): Targets in YOLO format.

        Returns:
            ``Dict[str, Tensor]``:
                - Loss dict with total loss (key: "loss") & sublosses.
        """
        loss, loss_detail = self.criterion(raw_outputs, targets)
        loss_dict = {
            "loss": loss,
            "loss_box": loss_detail[0],
            "loss_cls": loss_detail[1],
            "loss_dfl": loss_detail[2],
        }
        return loss_dict

    def run_forward(
        self,
        images: Tensor,
        targets: BatchedFormat,
    ) -> Union[Dict[str, Tensor], Tuple[Dict[str, Tensor], BatchedFormat]]:
        """Compute loss from images and if target passed, compute loss & return both loss dict
        and results.

        Args:
            images (``Tensor``): Batch RGB images.
            targets (``BatchedFormat``): Batch targets.

        Returns:
            ``Union[Dict[str, Tensor], Tuple[Dict[str, Tensor], BatchedFormat]]``:
                - Loss dict.
                - If predict: predictions.
        """
        # prepare inputs
        prepared_images, prepared_targets = self.prepare(images, targets=targets)
        # run forward pass
        if self.training:
            raw_outputs = self(prepared_images)
        else:
            prebuild_output, raw_outputs = self(prepared_images)
        # compute loss
        loss_dict = self.compute_loss(raw_outputs, prepared_targets)
        # return predictions if needed
        if not (self.training):
            predictions = self.build_results(raw_outputs, prebuild_output)
            # retrieve the padding from original img
            t, l, _, _ = ut.yolo_pad_requirements(
                images.shape[-2], images.shape[-1], required=self.pad_requirements
            )
            h, w = images.shape[-2:]
            # crop to original size
            predictions = BatchedFormat(
                [targ.crop(t, l, h, w)[0] for targ in predictions]
            )
            return loss_dict, predictions
        else:
            return loss_dict

    def get_predictions(self, images: Tensor) -> BatchedFormat:
        """Prepare images, Apply YOLO forward pass and build results.

        Args:
            images (``Tensor``): RGB images Tensor.

        Returns:
            ``BatchedFormats``:
                - Predictions for images as BatchedFormats.
        """
        self.eval()
        # get original spatial size
        ori_h, ori_w = images.shape[-2:]
        # pad coord to return back to non yolo required / 32 criterium afterward
        top, left, _, _ = ut.yolo_pad_requirements(
            ori_h, ori_w, required=self.pad_requirements
        )
        # pad images
        images = self.prepare(images)
        # predict
        prebuild_output, raw_outputs = self(images)
        results = self.build_results(raw_outputs, prebuild_output)
        # crop to back at original spatial size
        results = BatchedFormat(
            [pred.crop(top, left, ori_h, ori_w)[0] for pred in results]
        )
        return results

    def retrieve_spatial_size(self, raw_outputs: List[Tensor]) -> Tuple[int]:
        """Retrieve image shape from raw_outputs and stride values.

        Args:
            raw_outputs (``List[Tensor]``): Raw ouptuts from YOLO model.

        Returns:
            ``Tuple[int]``:
                - Size of input image (H, W).
        """
        h = int(raw_outputs[0].shape[-2] * self.stride[0])
        w = int(raw_outputs[0].shape[-1] * self.stride[0])
        return (h, w)
