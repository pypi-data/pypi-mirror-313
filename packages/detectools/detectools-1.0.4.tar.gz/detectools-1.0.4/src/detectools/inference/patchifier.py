from typing import Tuple, List
from torch import Tensor
from math import ceil
import torch
from torchvision.transforms.v2 import Pad
from itertools import product
from detectools.formats import BatchedFormat, BaseFormat, BboxFormat, InstanceMaskFormat
import copy
from torchvision.ops import nms


class Patchifier:
    """Handle patchification and unpatchification

    Args:
        patch_size (``Tuple[int, int]``): size of patches to create
        overlap (``float``): overlap between patches
        border_penalty (``float``, **optional**): penalty to apply on patch border objects before nms. Defaults to 0.5.
        nms_iou_threshold (``float``, **optional**): nms threshold. Defaults to 0.45.
        final_score_threshold (``float``, **optional**): final score (after penalty) threshold. Defaults to 0.4.

    Attributes
    ----------

    Attributes:
        patch_size (``Tuple[int, int]``)
        overlap (``float``): overlap between patches
        border_penalty (``float``)
        postprocess (```PostProcesser```)


    **Methods**
    """

    def __init__(
        self,
        patch_size: Tuple[int, int],
        overlap: float,
        border_penalty: float = 0.5,
        nms_iou_threshold: float = 0.45,
        final_score_threshold: float = 0.4,
    ):
        self.patch_size = patch_size
        self.overlap = overlap
        self.border_effect_penality = border_penalty
        self.postprocess = PostProcesser(nms_iou_threshold, final_score_threshold)

    def pad_to(
        self, image: Tensor, new_size: Tuple[int, int]
    ) -> Tuple[Tensor, Tuple[int, int, int, int]]:
        """Pad image to given size
        Args:
            image (Tensor).
            new_size (Tuple[int, int]).

        Returns:
            Tuple[Tensor, Tuple[int, int, int, int]]: padded image, (t, l, r, b)
        """
        t = int((new_size[0] - image.shape[-2]) / 2)
        l = int((new_size[1] - image.shape[-1]) / 2)
        b = int((new_size[0] - image.shape[-2]) - t)
        r = int((new_size[1] - image.shape[-1]) - l)
        padder = Pad((l, t, r, b))
        pad_coord = (t, l, r, b)
        return padder(image), pad_coord

    def patchify(
        self, image: Tensor
    ) -> Tuple[Tensor, List[Tuple[int, int]], Tensor, Tuple[int, int, int, int]]:
        """Create patches for image prediction : 1) Pad image to fit all patches, 2) create patches

        Args:
            image (``Tensor``)

        Returns:
            ``Tuple[ Tensor, List[Tuple[int, int]], Tuple[int, int], Tensor, Tuple[int, int]]``:
                - patches stacked (N_patch, c, h, w), List of (top, left) pad coordinates, padded image, image pad coordinates
        """
        h, w = image.shape[-2:]
        assert (
            self.patch_size[0] < h and self.patch_size[1] < w
        ), f"Can't patchify image of shape {(h, w)} with patch size {self.patch_size}."
        c, h, w = image.shape[-3:]
        h_patch, w_patch = self.patch_size
        # compute strides values
        stride_h = h_patch - round(h_patch * self.overlap)
        stride_w = w_patch - round(w_patch * self.overlap)
        # get number of pacthes on axis
        nb_h_patches = ceil(h / stride_h)
        nb_w_patches = ceil(w / stride_w)
        # padded image shape (H,W)
        h_padded = (nb_h_patches - 1) * stride_h + h_patch
        w_padded = (nb_w_patches - 1) * stride_w + w_patch
        # pad image
        padded_image, pad_coord = self.pad_to(image, (h_padded, w_padded))
        # get coordinates
        top_corners = range(0, nb_h_patches * stride_h, stride_h)
        left_corners = range(0, nb_w_patches * stride_w, stride_w)
        origins = list(product(top_corners, left_corners))
        # Create patches tensors
        patches = torch.zeros(
            (nb_h_patches * nb_w_patches, c, h_patch, w_patch), device=image.device
        ).to(image.device)
        #  Fill the patches tensors
        for idx, (y, x) in enumerate(origins):
            patches[idx] = padded_image[:, y : y + h_patch, x : x + w_patch]

        return patches, origins, padded_image, pad_coord

    def _merge_prediction_patches(
        self,
        pred_patches: BatchedFormat,
        origins: List[Tuple[int, int]],
        image_padded_size: Tuple[int, int],
    ) -> BaseFormat:
        """combine the patchs predictions together"""
        # add patch to full sized format
        full_pred: BaseFormat = type(pred_patches.formats[0]).empty(
            canvas_size=image_padded_size
        )
        scores = torch.tensor([]).to(pred_patches.device)
        for pred, ori in zip(pred_patches.formats, origins):
            r_pad = image_padded_size[1] - ori[1] - pred.canvas_size[1]
            b_pad = image_padded_size[0] - ori[0] - pred.canvas_size[0]
            full_pred += pred.pad(ori[0], ori[1], r_pad, b_pad)[0]
            if pred.scores != None:
                scores = torch.cat([scores, pred.scores])
        assert (
            scores.nelement() == full_pred.nb_object
        ), "Inconsistency between scores and object number."
        full_pred._scores = scores
        return full_pred

    def unpatchify(
        self,
        pred_patches: BatchedFormat,
        origins: List[Tuple[int, int]],
        image_padded_size: Tuple[int, int],
        padded_image_coords: Tuple[int, int, int, int],
        original_image_size: Tuple[int, int],
    ):
        """merge patchs predictions together while applying penalty, postprocess etc.
        Note that since InstanceMasks do not handle overlapping objects, you need to treat directly the patches in the postprocess.
        To do so you derive boxes, then use boxes to filter the masks."""
        # apply penalty
        pred_patches = BatchedFormat(
            [self._scores_penalty(pred) for pred in pred_patches]
        )
        # if instance_masks, need to filter patchs objects before merging (otherwise will override objects ...)
        if isinstance(pred_patches[0][0], InstanceMaskFormat):
            box_patches = [
                BboxFormat.from_instance_mask(patch) for patch in pred_patches
            ]
            associated_boxes = self._merge_prediction_patches(
                BatchedFormat(box_patches), origins, image_padded_size
            )
            pred_patches = self.postprocess.handle_patches_mask(
                pred_patches, associated_boxes
            )
            preds = self._merge_prediction_patches(
                pred_patches, origins, image_padded_size
            )
        else:
            # merge patchs
            preds = self._merge_prediction_patches(
                pred_patches, origins, image_padded_size
            )
            # Duplicates handling
            preds = self.postprocess.handle_box_duplicates(preds)
        # crop to original image
        t, l, _, _ = padded_image_coords
        h = original_image_size[0]
        w = original_image_size[1]
        preds, _ = preds.crop(t, l, h, w)
        return preds

    def _scores_penalty(self, patch: BaseFormat) -> BaseFormat:
        """apply score penalty on border. Method is linear"""
        if isinstance(patch, BboxFormat):
            return self._box_penalty(patch)
        elif isinstance(patch, InstanceMaskFormat):
            # if InstanceMaskFormat create boxes, apply penalty on objects boxes scores, return InstanceMaskFormat with replaced scores
            boxes = BboxFormat.from_instance_mask(patch)
            new_scores = self._box_penalty(boxes)
            new_patch = InstanceMaskFormat(
                data=patch.data, labels=patch.labels, scores=new_scores.scores
            )
            return new_patch

    def _box_penalty(self, patch: BaseFormat) -> BaseFormat:
        """Apply box scores penalty to reduce border effect. Helps patchification multiple objects removal.

        Args:
            patch (``BaseFormat``)

        Returns:
            ``BaseFormat``:
                - patch with reduced scores on border.
        """
        if patch.nb_object == 0:
            return patch
        assert (
            patch.scores != None
        ), "Can't apply penalty on scores since scores = None."
        patch: BaseFormat = copy.copy(patch)
        patch.format = "XYXY"
        patch_xcenter = patch.canvas_size[0] / 2
        patch_ycenter = patch.canvas_size[1] / 2
        max_devs = []
        for box in patch.data.value:
            centro_x = int((box[0] + box[2]) / 2)
            centro_y = int((box[1] + box[3]) / 2)
            relative_xdeviation = abs(centro_x - patch_xcenter) / patch.canvas_size[1]
            relative_ydeviation = abs(centro_y - patch_ycenter) / patch.canvas_size[0]
            # max and *2 because relative_dev in [0, 0.5] range (but we want in [0, 1])
            max_devs.append(max(2 * relative_xdeviation, 2 * relative_ydeviation))
        # Apply linear penalty
        relu = torch.nn.ReLU(inplace=True)
        penalty = relu(1 - self.border_effect_penality * torch.tensor(max_devs)).to(
            patch.device
        )
        new_scores = patch.scores * penalty
        patch._scores = new_scores
        return patch


class PostProcesser:
    """Handles postprocessing

    Args:
        nms_iou_th (``float``): nms threshold
        final_score_threshold (``float``): final score thresholding
    """

    def __init__(self, nms_iou_th: float, final_score_threshold: float):
        self.nms_iou_th = nms_iou_th
        self.final_score_threshold = final_score_threshold

    def handle_patches_mask(
        self, pred_batch: BatchedFormat, associated_boxes: BboxFormat
    ):
        # nms suppression
        nms_filter = self._box_nms_suppress(associated_boxes)
        pred_batch, nms_bool_filter = self._apply_index(pred_batch, nms_filter)
        associated_boxes, _ = associated_boxes[nms_bool_filter]
        pred_batch = BatchedFormat(
            [pred[pred.scores > self.final_score_threshold][0] for pred in pred_batch]
        )
        pred_batch.sanitize()
        return pred_batch

    def _apply_index(self, pred_batch: BatchedFormat, index: Tensor):
        index_slicer = [patch.nb_object for patch in pred_batch]
        # convert index to bool tensor with shape [N_objs]
        if not index.dtype == torch.bool:
            idx = range(sum(index_slicer))
            index = torch.tensor([i in index for i in idx])
        # create index parser for batch
        index_slicer.insert(0, 0)
        slicer = []
        s = 0
        for i in index_slicer:
            s += i
            slicer.append(s)
        # filter patches
        patch_list = []
        for i, patch in enumerate(pred_batch):
            patch_list.append(patch[index[slicer[i] : slicer[i + 1]]][0])
        return BatchedFormat(patch_list), index

    def handle_box_duplicates(self, pred: BaseFormat) -> BaseFormat:
        """Main function that call further function depending on handling mode

        Args:
            pred (``BaseFormat``): data to handle duplicates

        Returns:
            ``BaseFormat``:
                - handled duplicate new data
        """
        # nms suppression
        nms_filter = self._box_nms_suppress(pred)
        new_pred, _ = pred[nms_filter]
        new_pred, _ = new_pred.sanitize()
        new_pred, _ = new_pred[new_pred.scores > self.final_score_threshold]
        return new_pred

    def _box_nms_suppress(self, to_handle: BboxFormat) -> Tensor:
        """return a filter tensor of objects to keep after nms"""
        indexes_filter = nms(to_handle.data.value, to_handle.scores, self.nms_iou_th)
        return indexes_filter
