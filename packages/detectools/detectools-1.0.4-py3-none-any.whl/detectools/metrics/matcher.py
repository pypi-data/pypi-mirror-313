from torchvision.ops import box_iou
from detectools.formats import BaseFormat, BboxFormat, InstanceMaskFormat
import torch
from detectools import Configuration
from typing import Literal, Tuple
from torch import Tensor
import detectools.metrics.utils as ut
from torch.nn.functional import one_hot


class Matcher:
    """Class that handles the matching of prediction and targets to get tp, fp, fn"""

    def __init__(self):

        self.iou_th = Configuration().metrics_match_iou_threshold
        self._mode: Literal["bbox", "instance_mask"] = (
            Configuration().metrics_matcher_type
        )

    def match_pred_target(
        self, pred: BaseFormat, targ: BaseFormat
    ) -> Tuple[int, int, int, Tuple[Tensor, Tensor]]:
        """Matches predictions and targets

        Args:
            pred (Format)
            targ (Format)

        Returns:
            Tuple[int, int, int, Tuple[Tensor, Tensor]]: tp, fp, fn, (matched_predictions indices, matched_targets_indices)
        """
        # compute cross ious
        if self._mode == "bbox":
            cross_ious = self.match_boxes(pred, targ)
        elif self._mode == "instance_mask":
            cross_ious = self.match_instance_masks(pred, targ)
        #### derive tp, fp, fn and matching indexes
        matched_candidates = (
            torch.max(cross_ious, dim=1)[0][..., None]
            == torch.max(cross_ious, dim=0)[0][None, ...]
        ).view(cross_ious.shape)
        # true positive if iou of max_matchs > iou threshold
        tp = torch.sum((matched_candidates > 0) & (cross_ious > self.iou_th))
        # false positive: all boxes with no match with targets
        fp = torch.sum(pred.nb_object - torch.sum(tp))
        # false negative if target has no pred box with iou > threshold
        fn = torch.sum(torch.max(cross_ious, dim=0)[0] < 0.5)
        pred_idxs, target_idxs = torch.where(
            torch.logical_and((matched_candidates > 0), (cross_ious > self.iou_th))
        )
        # extract indexes
        pred_idxs = pred_idxs.tolist() if pred_idxs.nelement() > 0 else []
        target_idxs = target_idxs.tolist() if target_idxs.nelement() > 0 else []
        match_idxs = (torch.tensor(pred_idxs).long(), torch.tensor(target_idxs).long())
        # send back box format to original format
        return tp, fp, fn, match_idxs

    def match_boxes(
        self, pred: BaseFormat, targ: BaseFormat
    ) -> Tuple[int, int, int, Tuple[Tensor, Tensor]]:
        """compute box cross ious for matching"""
        assert isinstance(pred, BboxFormat) or isinstance(
            pred, InstanceMaskFormat
        ), "Prediction must be BboxFormat or InstanceMaskFormat to use match_boxes"
        assert isinstance(targ, BboxFormat) or isinstance(
            targ, InstanceMaskFormat
        ), "target must be BboxFormat or InstanceMaskFormat to use match_boxes"
        # Convert to BboxFormat if needed
        if isinstance(pred, InstanceMaskFormat):
            pred: BboxFormat = BboxFormat.from_instance_mask(pred)
        if isinstance(targ, InstanceMaskFormat):
            targ: BboxFormat = BboxFormat.from_instance_mask(targ)
        pred.data.format = "XYXY"
        targ.data.format = "XYXY"
        cross_ious = box_iou(pred.data.value, targ.data.value)
        return cross_ious

    def match_instance_masks(self, pred: InstanceMaskFormat, targ: InstanceMaskFormat):
        """compute instance_mask cross ious for matching"""
        assert isinstance(
            pred, InstanceMaskFormat
        ), "Prediction must be InstanceMaskFormat to use match_instance_masks"
        assert isinstance(
            targ, InstanceMaskFormat
        ), "target must be InstanceMaskFormat to use match_instance_masks"
        # convert pred / target to one hots to use mask_iou func. Remove class 0 encoded and move to cpu for memory usage.
        original_pred_device = pred.device
        original_targ_device = targ.device
        pred.device = "cpu"
        targ.device = "cpu"
        one_hot_preds = one_hot(pred.data.value).permute(2, 0, 1)[1:]
        one_hot_targs = one_hot(targ.data.value).permute(2, 0, 1)[1:]
        # apply cross iou and return object to devices
        cross_ious = ut.mask_iou(one_hot_preds, one_hot_targs)
        pred.device = original_pred_device
        targ.device = original_targ_device
        cross_ious = cross_ious.to(original_pred_device)
        return cross_ious
