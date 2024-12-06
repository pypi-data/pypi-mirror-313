from __future__ import annotations
from typing import List, Tuple, Literal, Dict, Union, Any
from detectools.models.basemodel import BaseModel
from detectools import Configuration
from detectools.formats import InstanceMaskFormat, BatchedFormat, InstanceMaskData
from detectools import Configuration
from transformers import (
    Mask2FormerConfig,
    Mask2FormerForUniversalSegmentation,
    Mask2FormerImageProcessor,
)
from operator import itemgetter
from transformers.models.mask2former.modeling_mask2former import (
    Mask2FormerForUniversalSegmentationOutput,
)
import torch
from torch import Tensor

# TODO solve résolution issues (create modulable feature map, check if possible to adapt to large images in inference mode. Have a look at prediction head ;) ). Use property


class Mask2Former(Mask2FormerForUniversalSegmentation, BaseModel):
    """Mask2Former class, child class of Mask2FormerForUniversalSegmentation from hugging face. To use, data_type must be set to instance_mask.

    Args:
        pretrain (Literal[&quot;large&quot;, &quot;medium&quot;, &quot;small&quot;, &quot;tiny&quot;, &quot;&quot;], optional): Pretrained architecture. Defaults to "tiny".
        overlap_mask_thr (float, optional): Defaults to 0.8.

    Attributes
    ----------

    Attributes:
        processor (``Mask2FormerImageProcessor``)
        overlap_mask_thr (``float``)


    Attributes
    ----------

    Properties:
        queries (``torch.nn.Embedding``) : number of queries / dim for embedding. To use setter please provide int or Tuple[int, int]. In case only a int is provided dimensional embedding is 256, otherwise Tuple is query number, dim.

    Notes: When used for large image inference, Mask2Former is less performant if trained on smaller patches. One way out is to increase the query number. Please check property description. Future amelioration on this matter is under developpment.


    **Methods**
    """

    size_configs = {
        "large": "facebook/mask2former-swin-large-coco-instance",
        "medium": "facebook/mask2former-swin-base-coco-instance",
        "small": "facebook/mask2former-swin-small-coco-instance",
        "tiny": "facebook/mask2former-swin-tiny-coco-instance",
    }

    def __init__(
        self,
        pretrain: Literal["large", "medium", "small", "tiny", ""] = "tiny",
        overlap_mask_thr: float = 0.8,
    ):

        # assert Task mode is "instance_mask"
        assert (
            Configuration().data_type == "instance_mask"
        ), f"Configuration().data_type should be 'instance_mask' to construct Mask2Former object, got {Configuration().data_type}"

        if pretrain:
            pretrain_config = Mask2Former.size_configs[pretrain]
            pretrain_model = Mask2FormerForUniversalSegmentation.from_pretrained(
                pretrain_config,
                num_labels=Configuration().num_classes
                + 1,  # mask2former redefine labels including background.
                ignore_mismatched_sizes=True,
            )
            self.__dict__ = pretrain_model.__dict__
        else:
            super().__init__(Mask2FormerConfig(Configuration().num_classes))

        # define mask2former input processor
        self.processor = Mask2FormerImageProcessor(
            do_resize=False, do_normalize=False, do_rescale=False, ignore_index=255
        )

        self.overlap_mask_thr = overlap_mask_thr
        # original queries in model (can be changed with queries property)
        self._queries = self.model.transformer_module.queries_embedder

    @property
    def queries(self):
        return self._queries

    @queries.setter
    def queries(self, embedding: Union[int, Tuple]):
        if isinstance(embedding, int):
            nb, dim = embedding, 256
        else:
            nb, dim = embedding
        self.model.transformer_module.queries_embedder = torch.nn.Embedding(nb, dim)
        self.model.transformer_module.queries_features = torch.nn.Embedding(nb, dim)
        self._queries = torch.nn.Embedding(nb, dim)

    def prepare_target(
        self, target: InstanceMaskFormat
    ) -> Tuple[Tensor, Dict[int, int]]:
        """Prepare target in Mask2Former format"""
        labels = target.labels
        labels = torch.cat([torch.tensor([0]).to(self.device), labels + 1])
        instance_labels_dict = dict(
            zip(range(0, target.nb_object + 1), labels.tolist())
        )
        masks = target.data.value
        return masks, instance_labels_dict

    def prepare(
        self, images: Tensor, targets: Union[BatchedFormat, None] = None
    ) -> Dict[str, Union[Tensor, Dict[Any, Any]]]:
        """Transform images and targets into Mask2Former specific format for prediction & loss computation.

        Args:
            images (``Tensor``): Batch images.
            targets (``BatchedFormats``, **optional**): Batched targets from DetectionDataset.

        Returns:
            ``Union[Any, Tuple[Any]]``:
                - Images data prepared for Mask2Former.
                - If targets: images + targets prepared for Mask2Former.
        """

        if targets != None:
            instance_labels = []
            segmentation_maps = []
            for target in targets:
                assert isinstance(
                    target, InstanceMaskFormat
                ), "Target should be instance mask format for Mask2former"
                target_masks, target_dict = self.prepare_target(target)
                instance_labels.append(target_dict)
                segmentation_maps.append(target_masks)

            model_input = self.processor(
                images=list(images.unbind()),
                segmentation_maps=segmentation_maps,
                instance_id_to_semantic_id=instance_labels,
                return_tensors="pt",
            )
        else:
            model_input = self.processor(
                images=list(images.unbind()),
                return_tensors="pt",
            )

        return model_input

    # override
    def build_results(
        self,
        raw_outputs: Mask2FormerForUniversalSegmentationOutput,
        spatial_size: Tuple[int, int],
    ) -> BatchedFormat:
        """Transform model outputs into BatchedFormat for results.

        Args:
            raw_outputs (``Mask2FormerForUniversalSegmentationOutput``): Mask2Former output.
            spatial_size (``Tuple[int, int]``): Size of original image (H, W).

        Returns:
            ``BatchedFormats``:
                - Model output as BatchedFormat.
        """
        # Process raw output wtih Mask2Former processor.
        batch_size = raw_outputs.masks_queries_logits.shape[0]
        predictions = self.processor.post_process_instance_segmentation(
            raw_outputs,
            overlap_mask_area_threshold=self.overlap_mask_thr,
            threshold=Configuration().model_confidence_threshold,
            target_sizes=[spatial_size] * batch_size,
        )
        results = []
        # iter on predictions
        for prediction in predictions:
            spatial_size = prediction["segmentation"].shape[-2:]
            # remove empty segmentation objects (objects with no mask pixels)
            mask: Tensor = prediction[
                "segmentation"
            ].long()  # Here -1 = non segmented, then 0 - N objects includes background
            segments = prediction["segments_info"]
            # retrieve labels, scores
            labels = torch.tensor([i["label_id"] for i in segments])
            scores = torch.tensor([i["score"] for i in segments])
            # remove non existing objects
            empty_objs_filt = torch.tensor(
                [torch.count_nonzero(mask == l) != 0 for l in range(labels.shape[0])]
            )
            labels = labels[empty_objs_filt]
            scores = scores[empty_objs_filt]
            # move mask non predicted (label = -1) and background (label=0) together
            if mask.unique()[0] == -1:
                if torch.any(labels == 0).item():
                    mask[mask == mask.unique()[1:][labels == 0].item()] = -1
            else:
                mask[mask == mask.unique()[labels == 0].item()] = -1
            # Reindex labels and scores to remove background ( -1 in labels and in mask)
            labels -= 1
            filtering = labels != -1
            labels = labels[filtering]
            scores = scores[filtering]
            labels = labels.to(self.device)
            scores = scores.to(self.device)
            # create InstanceMaskData instance and handle empty detection
            mask += 1
            mask, _ = InstanceMaskData(mask)._reindex()
            if mask.nb_object != 0:
                result = InstanceMaskFormat(mask, labels=labels, scores=scores)
                result, _ = result.sanitize()
                results.append(result)
            else:
                results.append(InstanceMaskFormat.empty(spatial_size))
        if len(results) == 0:
            results.append(InstanceMaskFormat.empty(spatial_size))
        results = BatchedFormat(results)
        return results

    def inputs_to_device(self, input: Any, device: Literal["cpu", "cuda"]):
        """Send Mask2Former inputs to device."""
        for k, v in input.items():
            if isinstance(v, list):
                input[k] = [t.to(device) for t in v]
            elif isinstance(v, Tensor):
                input[k] = v.to(device)
        return input

    def run_forward(
        self, images: Tensor, targets: BatchedFormat
    ) -> Dict[str, Tensor] | Tuple[Dict[str, Tensor] | BatchedFormat]:
        """Compute loss from images and if target passed, compute loss & return both loss dict
        and results.

        Args:
            images (``Tensor``): Batch RGB images.
            targets (``BatchedFormat``): Batch targets.

        Returns:
            ``Union[Dict[str, Tensor], Tuple[Dict[str, Tensor], BatchedFormat]]``:
                - Loss dict and prediction if model in eval mode.
        """
        # prepare inputs
        spatial_size = images.shape[-2:]
        model_input = self.prepare(images, targets=targets)
        model_input = self.inputs_to_device(model_input, self.device)
        # run forward pass
        output: Mask2FormerForUniversalSegmentationOutput = self(
            pixel_values=model_input["pixel_values"],
            mask_labels=model_input["mask_labels"],
            class_labels=model_input["class_labels"],
        )
        # compute loss
        loss_dict = {"loss": output.loss}
        # return predictions if needed
        if not self.training:
            predictions = self.build_results(output, spatial_size)
            return loss_dict, predictions
        else:
            return loss_dict

    def get_predictions(self, images: Tensor) -> BatchedFormat:
        """Prepare images, Apply model forward pass and build results.

        Args:
            images (``Tensor``): RGB images Tensor.

        Returns:
            ``BatchedFormat``:
                - Predictions for images as BatchedFormat.
        """
        self.eval()
        spatial_size = images.shape[-2:]
        model_input = self.prepare(images)
        model_input = self.inputs_to_device(model_input, self.device)
        # predict
        output: Mask2FormerForUniversalSegmentationOutput = self(
            pixel_values=model_input["pixel_values"]
        )
        results = self.build_results(output, spatial_size=spatial_size)

        return results
