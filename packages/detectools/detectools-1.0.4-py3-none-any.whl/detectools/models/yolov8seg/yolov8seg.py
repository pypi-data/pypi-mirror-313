from ultralytics.cfg import get_cfg
from ultralytics.nn.tasks import SegmentationModel, attempt_load_one_weight
from ultralytics.utils import DEFAULT_CFG
from detectools.models.basemodel import BaseModel
from typing import Literal
from detectools import Configuration
import detectools.models.yolov8seg.errors as er
import detectools.models.yolov8seg.utils as ut
from detectools.formats import (
    BatchedFormat,
    BboxData,
    BboxFormat,
    InstanceMaskFormat,
    InstanceMaskData,
)
import torch
from typing import Dict, Tuple, Union, List
from torch import Tensor
import torchvision.transforms.v2.functional as F


class Yolov8Seg(SegmentationModel, BaseModel):
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
        - pad_requirements (``int``) : pad requirements for yolov8seg (basic is image shape must be multiple of 32)
        - mask_logit_threshold (``int``) : mask logit threshold to consider if pixel is class or background. Default is 0.5 but can be changed.

    Attributes
    ----------

    Properties:
        - device (``Literal["cuda", "cpu"]``): model's device


    **Methods**
    """

    def __init__(
        self,
        architecture: Literal[
            "yolov8n-seg",
            "yolov8m-seg",
            "yolov8l-seg",
            "yolov8x-seg",
        ] = "yolov8n-seg",
        pretrained: bool = True,
        reg_max=16,
        *args,
        **kwargs,
    ):
        er.check_config()
        assert (
            "-seg" in architecture
        ), f"architecture must be one of [yolov8n-seg, yolov8m-seg, yolov8l-seg, yolov8x-seg] to use Yolov8Seg. Got {architecture} (probably forgot the -seg)"
        config = Configuration()
        super().__init__(f"{architecture}.yaml", nc=config.num_classes, *args, **kwargs)
        self.args = get_cfg(DEFAULT_CFG)
        self.model[-1].reg_max = reg_max
        if pretrained:
            architecture = attempt_load_one_weight(
                f"{architecture}.pt",
            )
            self.load(architecture[0])
        self.criterion = self.init_criterion()
        self.device = config.device
        self.pad_requirements = 32
        self.mask_logit_threshold = 0.5

    # overwrite
    @property
    def device(self):
        return self._device

    # overwrite
    @device.setter
    def device(self, val):
        self.to(val)
        self.criterion = self.init_criterion()

    def prepare_target(self, targets: BatchedFormat) -> Dict[str, Tensor]:
        """Transform SegmentationFormat targets into yolo-seg targets format.

        Args:
            targets (``BatchedFormats``): Batch targets.

        Returns:
            ``Dict[str, Tensor]``:
                - Targets in YOLO format.
        """
        # Create batched stacked mask : (N_batch, H, W)
        targets = BatchedFormat([t.sanitize()[0] for t in targets])
        masks = torch.stack([t.data.value for t in targets])
        # masks = ut.mask2yolo(masks)
        # Create bboxes
        boxes_batched = BatchedFormat(
            [BboxFormat.from_instance_mask(t) for t in targets]
        )
        boxes_batched.set_bboxes_format("CXCYWH")
        # normalize boxes
        boxes = torch.cat(
            [ut.normalize_boxes(b.data.value, masks.shape[-2:]) for b in boxes_batched]
        )
        # extract labels
        labels = torch.cat([t.labels.long() for t in targets])
        images_indices = torch.cat(
            [torch.full((t.nb_object,), i) for i, t in enumerate(targets)]
        )
        images_indices = images_indices.to(targets.device)
        # check if all values are compatible
        N_box = boxes.shape[0]
        N_instances = sum([torch.max(m) for m in masks])
        N_labels = labels.shape[0]
        assert (N_box == N_instances) and (
            N_box == N_labels
        ), "Error in preparing target : one or multiple of (N_boxes, N_instances, N_labels) is different."

        # put labels and batch_idx in yolo dormat : Tensor (N, 1)
        batch_idx = images_indices[:, None]
        classes = labels[:, None]
        yolotarget = {
            "masks": masks,
            "bboxes": boxes,
            "cls": classes,
            "batch_idx": batch_idx,
        }
        return yolotarget

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
            targets = self.prepare_target(targets)
            return images, targets
        else:
            return images

    def prebuild_output(self, raw_outputs: Tuple[Tensor, ...]) -> Tuple[Tensor, ...]:
        """Unpack Yolov8-seg (eval mode) raw results.

        Args:
            raw_output (``Tuple[Tensor, ...]``): Yolov8 raw eval mode results.

        Returns:
            ``Tuple[Tensor, ...]``:
                - boxes (N_batch, N_obj, cxcywh).
                - cls_scores (N_batch, N_cls).
                - mask_weights (N_batch, N_obj, 32).
                - protos (N_batch, protos).
        """
        output0, output1 = raw_outputs
        output0 = output0.permute(0, 2, 1)  # permute in N_batch, N_obj, obj_length
        boxes = output0[:, :, 0:4]
        cls_indx = 4 + Configuration().num_classes
        cls_scores = output0[:, :, 4:cls_indx]
        mask_weights = output0[:, :, -32:]
        protos = output1[2]
        return boxes, cls_scores, mask_weights, protos

    def build_results(
        self, raw_outputs: Tuple[Tensor, ...], get_logit: bool = False
    ) -> BatchedFormat:
        """Transform model outputs into Batch InstanceMaskFormat for results.

        Args:
            raw_outputs (``List[Tensor]``): Model outputs.

        Returns:
            ``BatchedFormats``:
                - Batched predictions.
        """
        # extract info from raw results
        boxes, cls_scores, mask_weights, protos = self.prebuild_output(raw_outputs)
        spatial_size = self.retrieve_spatial_size(raw_outputs)
        results = []
        for i, image_boxes in enumerate(boxes):
            # get image values
            image_boxes = boxes[i]
            image_cls_scores = cls_scores[i]
            image_mask_weights = mask_weights[i]
            image_protos = protos[i]
            # get best class and corresponding score
            image_cls_scores, best_class = torch.max(image_cls_scores, dim=1)
            # filter by confidence thr
            conf_filter = ut.confidence_filter(
                image_cls_scores, Configuration().model_confidence_threshold
            )
            image_cls_scores = image_cls_scores[conf_filter]
            image_labels = best_class[conf_filter]
            image_boxes = image_boxes[conf_filter]
            image_mask_weights = image_mask_weights[conf_filter]
            # if no objects with good confidence move to next image
            if image_labels.nelement() == 0:
                results.append(InstanceMaskFormat.empty(spatial_size))
                continue
            # Apply nms from boxes on other objects
            boxes_ = BboxData(image_boxes, "CXCYWH", spatial_size)
            nms_indexes = ut.box_nms_filter(boxes_, image_cls_scores)
            # apply nms to all values
            image_boxes = image_boxes[nms_indexes]
            image_cls_scores = image_cls_scores[nms_indexes]
            image_mask_weights = image_mask_weights[nms_indexes]
            image_labels = image_labels[nms_indexes]
            # Keep only model_max_detection elements
            model_max_detection = Configuration().model_max_detection
            if image_boxes.nelement() > model_max_detection:
                indexes = torch.argsort(image_cls_scores)
                image_boxes = image_boxes[indexes][-model_max_detection:]
                image_cls_scores = image_cls_scores[indexes][-model_max_detection:]
                image_mask_weights = image_mask_weights[indexes][-model_max_detection:]
                image_labels = image_labels[indexes][-model_max_detection:]
            # compute binary masks per remaining obj
            _boxes = BboxData(image_boxes, "CXCYWH", spatial_size)  # change box format
            _boxes.format = "XYXY"
            image_masks = ut.proto2mask(
                image_protos, image_mask_weights, _boxes.value, spatial_size
            )
            # apply "logits" thresholding to mask (logit > 0.5 belong to object)
            image_masks = image_masks.gt_(self.mask_logit_threshold)
            logit_filter = torch.tensor([torch.max(m) != 0 for m in image_masks]).to(
                image_masks.device
            )  # Filter non kept masks
            image_cls_scores = image_cls_scores[logit_filter]
            image_labels = image_labels[logit_filter]
            image_masks = image_masks[logit_filter]
            image_instance_mask = InstanceMaskData.from_binary_masks(image_masks)
            if image_instance_mask.nb_object != image_labels.shape[0]:
                pass
            mask_format = InstanceMaskFormat(
                image_instance_mask, image_labels, image_cls_scores
            )
            mask_format, _ = (
                mask_format.sanitize()
            )  # Sanitize will reindex objects thus removing empty masks
            results.append(mask_format)
        if len(results) == 0:
            results = [InstanceMaskFormat.empty(spatial_size)]
        return BatchedFormat(results)

    def compute_loss(self, predictions: Tuple, target: Dict) -> Dict[str, Tensor]:
        """Compute loss with predictions & targets.

        Args:
            predictions (``Any``): Raw output of model.
            target (``Dict[Any, Any]``): Targets in YOLO format.

        Returns:
            ``Dict[str, Tensor]``:
                - Loss dict with total loss (key: "loss") & sublosses.
        """
        loss, loss_detail = self.criterion(predictions, target)
        loss_dict = {
            "loss": loss,
            "loss_box": loss_detail[0],
            "loss_seg": loss_detail[1],
            "loss_cls": loss_detail[2],
            "loss_dfl": loss_detail[3],
        }
        return loss_dict

    def retrieve_spatial_size(self, raw_outputs: List[Tensor]) -> Tuple[int, int]:
        """Retrieve image shape from raw_outputs and stride values.

        Args:
            raw_outputs (``List[Tensor]``): Raw ouptuts from YOLO model.

        Returns:
            ``Tuple[int]``:
                - Size of input image (H, W).
        """
        if self.training:
            h = int(raw_outputs[0][0].shape[-2] * self.stride[0])
            w = int(raw_outputs[0][0].shape[-1] * self.stride[0])
        else:
            h = int(raw_outputs[1][0][0].shape[-2] * self.stride[0])
            w = int(raw_outputs[1][0][0].shape[-1] * self.stride[0])
        return (h, w)

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
        raw_outputs = self(prepared_images)
        # compute loss
        loss_dict = self.compute_loss(raw_outputs, prepared_targets)
        # return predictions if needed
        if not (self.training):
            predictions = self.build_results(raw_outputs)
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
        raw_outputs = self(images)
        results = self.build_results(raw_outputs)
        # crop to back at original spatial size
        results = BatchedFormat(
            [pred.crop(top, left, ori_h, ori_w)[0] for pred in results]
        )
        return results
