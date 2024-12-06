from typing import Any, Callable, Dict, List, Tuple, Union
from detectools.formats import BatchedFormat, BaseFormat, InstanceMaskFormat
import torch
from torch import Tensor
from torchmetrics import Metric
from detectools.metrics.matcher import Matcher
from detectools import Configuration
from torchmetrics.classification import StatScores


class DetectMetric(Metric):
    """Base class for custom detection metric with torchmetrics engine

    Args:
        func (Callable): function to apply to tp, fp, tn, fn
        name (str, optional): metric's name (useful for tensorboard monitoring). Defaults to "DetectionMetric".
    """

    is_differentiable = None
    higher_is_better = True
    full_state_update: bool = False

    def __init__(
        self,
        func: Callable,
        name: str = "DetectionMetric",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.add_state("tp", default=torch.tensor(0), dist_reduce_fx="sum")
        self.add_state("fp", default=torch.tensor(0), dist_reduce_fx="sum")
        self.add_state("fn", default=torch.tensor(0), dist_reduce_fx="sum")
        self.add_state("samplewise", default=[], dist_reduce_fx="cat")
        self.func = func
        self.name = name

    def update(
        self,
        prediction: Union[BaseFormat, BatchedFormat],
        target: Union[BaseFormat, BatchedFormat],
    ):
        """Update metric's internal state with prediction target comparison (tp, fp, tn, fn)

        Args:
            prediction (Union[BaseFormat, BatchedFormat])
            target (Union[BaseFormat, BatchedFormat])
        """

        # if no objects in prediction or target: stats are neutral (0)
        # else compute match box and stats

        # Cast pred and target to batched format if not already batched format
        prediction: BatchedFormat = (
            prediction
            if isinstance(prediction, BatchedFormat)
            else BatchedFormat([prediction])
        )
        target: BatchedFormat = (
            target if isinstance(target, BatchedFormat) else BatchedFormat([target])
        )
        # update metric
        matcher = Matcher()
        for pred, targ in zip(prediction, target):
            if pred.nb_object != 0 and targ.nb_object != 0:
                tp, fp, fn, _ = matcher.match_pred_target(pred, targ)
            elif pred.nb_object != 0 and targ.nb_object == 0:
                tp, fp, fn, _ = 0, pred.nb_object, 0, None
            elif prediction.size == 0 and target.size != 0:
                tp, fp, fn, _ = 0, 0, targ.nb_object, None
            else:
                return

            self.tp += tp
            self.fp += fp
            self.fn += fn
            # None because of no tn in detection
            self.samplewise.append(self.func(tp, fp, None, fn))

    def compute(self) -> Dict[str, Tensor]:
        """Return metric computed with internal state.

        Returns:
             Dict[str, Tensor]: dictionnary with aggregation_method: value
        """
        global_value = self.func(self.tp, self.fp, None, self.fn)
        samplewise_value = torch.nanmean(torch.tensor(self.samplewise))
        metric_dict = {"global": global_value, "samplewise": samplewise_value}

        return metric_dict


class ClassWiseDetectMetric(Metric):
    """Base class that agregates n_classes DetectMetric(s) to obtain class dependant performances.
    Note that samplewise scores are not performed here.

    Args:
        func (Callable): function to apply to tp, fp, tn, fn
        name (str, optional): metric's name (useful for tensorboard monitoring). Defaults to "ClassWiseDetectionMetric".

    Attributes
    ----------

    Attributes:
        - classmetrics (``List[DetectMetric]``): list of detectmetrics specialized in each classes.
    """

    def __init__(
        self,
        func: Callable,
        name: str = "ClassWiseDetectionMetric",
        **kwargs,
    ):
        num_classes = Configuration().num_classes
        assert (
            num_classes >= 2
        ), f"{num_classes} is an invalid number of classes for ClassWiseMetric (must be >= 2). If you have one class please use DetectMetric instead of ClasswiseMetric"

        super().__init__(**kwargs)
        self.name = name

        # create instances of DetectMetrics : 1 for global and 1 for each class
        self.classmetrics = [DetectMetric(func, name=f"{name}/global").to(self.device)]
        self.classmetrics += [
            DetectMetric(func, name=f"{name}/cls_{i}").to(self.device)
            for i in range(num_classes)
        ]

    def update(
        self,
        prediction: Union[BaseFormat, BatchedFormat],
        target: Union[BaseFormat, BatchedFormat],
    ):
        """Update all DetectMetrics in self.classmetrics according to prediction / target.

        Args:
            prediction (Union[BaseFormat, BatchedFormat])
            target (Union[BaseFormat, BatchedFormat])
        """
        prediction = (
            prediction
            if isinstance(prediction, BatchedFormat)
            else BatchedFormat([prediction])
        )
        target = (
            target if isinstance(target, BatchedFormat) else BatchedFormat([target])
        )
        for i, met in enumerate(self.classmetrics):
            filtered_pred = self._filter_classes(prediction, i)
            filtered_targ = self._filter_classes(target, i)
            if i == 0:
                met.update(prediction, target)
            else:
                met.update(filtered_pred, filtered_targ)

    def _filter_classes(self, batchedformat: BatchedFormat, cls: int):
        new_formats = []
        for form in batchedformat:
            new_form, _ = form[form.labels == cls]
            new_formats.append(new_form)
        return BatchedFormat(new_formats)

    def compute(self):
        """Return metrics values.

        Returns:
             Dict[str, Tensor]: dictionnary with all "global" DetectMetric in self.classmetrics
        """
        classwisedict = {met.name: met.compute()["global"] for met in self.classmetrics}
        return classwisedict

    # override
    def reset(self):
        """Reset all metrics in self.classmetrics. Override from torchmetrics Metric"""
        [met.reset() for met in self.classmetrics]

    # override
    def to(self, device: Any):
        """Move all metrics in self.classmetrics to device. Override from torchmetrics Metric

        Args:
            device (Any)
        """
        self.classmetrics = [metric.to(device) for metric in self.classmetrics]
        return self


class ClassifMetric(Metric):
    """Child class of torchmetrics metrics for classification.
    Allow to take Format as inputs and return dict of metric."""

    def __init__(
        self,
        func: Callable,  # metric functionnal
        name: str = "ClassifMetric",
        **kwargs: Any,
    ):

        super().__init__(**kwargs)
        num_classes = Configuration().num_classes
        self.func = func
        self.task = "binary" if num_classes == 1 else "multiclass"
        self.nc = num_classes
        # use tm engine to get statistics (tp,tn,fp,fn,sup)
        self.stat_score = StatScores(
            task=self.task,
            multidim_average="samplewise",
            average="none",
            num_classes=num_classes,
        )
        self.add_state("stats", default=[], dist_reduce_fx="cat")
        self.name = name

    def update(
        self,
        prediction: Union[BaseFormat, BatchedFormat],
        target: Union[BaseFormat, BatchedFormat],
    ):
        """Update internal states."""
        # if no predictions or target, no classification evaluation
        prediction = (
            BatchedFormat([prediction])
            if not isinstance(prediction, BatchedFormat)
            else prediction
        )
        target = (
            BatchedFormat([target]) if not isinstance(target, BatchedFormat) else target
        )
        for pred, targ in zip(prediction, target):
            if pred.nb_object == 0 or targ.nb_object == 0:
                return
            target_labels = targ.labels
            # match objects
            matcher = Matcher()
            _, _, _, (pred_idxs, target_idxs) = matcher.match_pred_target(pred, targ)
            pred_idxs = pred_idxs.to(pred.device)
            target_idxs = target_idxs.to(targ.device)
            pred, _ = pred[pred_idxs]
            targ, _ = targ[target_idxs]
            # if no box match, add all targets in fn
            if pred.nb_object == 0:
                class_stats = torch.zeros((self.nc, 5)).to(pred.device)
                values = torch.tensor(
                    [torch.sum(target_labels == i) for i in range(self.nc)]
                )
                class_stats[:, 4] = values
                self.stats.append(class_stats[None, ...])
                return
            # get labels
            pred_labels = pred.labels
            target_labels = targ.labels
            # if binary pass label 0 to 1
            if self.task == "binary":
                pred_labels += 1
                target_labels += 1
            # compute stats
            stats = self.stat_score(
                pred_labels[None, ...], target_labels[None, ...]
            ).view(1, self.nc, 5)
            self.stats.append(stats)

    def global_micro_compute(self) -> Tensor:
        """Compute metric with global/micro averagging."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5)
        # sum stats accross samples
        samples_stack = samples_stack.sum(dim=0)  # (NC, 5)
        # sum stats accross classes
        micro_stack = torch.sum(samples_stack, dim=0)  # (5,)
        # compute metric
        tp, fp, tn, fn, _ = micro_stack.unbind(0)
        return self.func(tp, fp, tn, fn)

    def global_macro_compute(self) -> Tuple[Tensor, Tensor]:
        """Compute metric with global/macro averraging.
        Return also metric/class tensor."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5)
        # sum stats accross samples
        samples_stack = samples_stack.sum(dim=0)  # (NC, 5)
        # compute metric/class
        tp, fp, tn, fn, _ = samples_stack.unbind(1)
        class_metrics = self.func(tp, fp, tn, fn)  # (NC,)
        return torch.nanmean(class_metrics), class_metrics

    def samplewise_micro(self) -> Tensor:
        """Compute metric with samplewise/micro averagging."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5))
        # sum stat accross classes
        samples_stack = samples_stack.sum(dim=1)  # (NC, 5)
        # compute metric/sample
        tp, fp, tn, fn, _ = samples_stack.unbind(dim=1)
        samples_metrics = self.func(tp, fp, tn, fn)
        # mean accross samples
        return torch.nanmean(samples_metrics)

    def samplewise_macro(self) -> Tensor:
        """Compute metric with samplewise/macro averagging."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5)
        # compute metric/class/sample
        tp, fp, tn, fn, _ = samples_stack.unbind(2)
        class_metrics = self.func(tp, fp, tn, fn)  # (N,NC)
        # mean accross classes
        macro = torch.nanmean(class_metrics, dim=1)  # (N,)
        # mean accross samples
        macro_samplewise = torch.nanmean(macro, dim=0)

        return macro_samplewise

    def compute(self):
        """Comput metric with all averag strategy and return a dict with all values."""
        if not self.stats:
            return {self.name: torch.tensor(torch.nan)}
        # if binary no need for macro aggregation
        metric_dict = {}
        if self.task == "multiclass":
            # global micro
            global_micro = self.global_micro_compute()
            metric_dict.update({"_global_micro": global_micro})
            # global macro
            global_macro, class_metrics = self.global_macro_compute()
            classes_dict = {
                f"/cls_{i}": class_metrics[i] for i in range(class_metrics.nelement())
            }
            metric_dict.update({"_global_macro": global_macro})
            metric_dict.update(classes_dict)
            # samplewise micro
            samplewise_micro = self.samplewise_micro()
            metric_dict.update({"_samplewise_micro": samplewise_micro})
            # samplewise macro
            samplewise_macro = self.samplewise_macro()
            metric_dict.update({"_samplewise_macro": samplewise_macro})
        else:
            # global micro
            global_micro = self.global_micro_compute()
            metric_dict.update({"_global": global_micro})
            # samplewise micro
            samplewise_micro = self.samplewise_micro()
            metric_dict.update({"_samplewise": samplewise_micro})
            return metric_dict

        return metric_dict


# TODO adapt to semantic basedata object once implemented (when merging segmentools and detectools)


class SemanticSegmentationMetric(ClassifMetric):
    """Child class of ClassifMetric. Move from instance to semantic segmentation paradigm to provide stats based on classes masks (instead of objects)."""

    def __init__(
        self,
        func: Callable,  # metric functionnal
        name: str = "SegmentationMetric",
        **kwargs: Any,
    ):
        assert (
            Configuration().data_type == "instance_mask"
        ), f"Configuration().data_type must be instance_mask to use SemanticSegmentationMetrics. Got {Configuration().data_type}"
        # init from ClassifMetric and
        # redefine stat score num_classes for multiclass detection to include background as a class (+1 class)
        # Note that background is later removed in update (background is meaningless regarding instance segmentation) but important for stats calculations
        num_classes = Configuration().num_classes
        super().__init__(func, name=name, **kwargs)
        if num_classes > 1:
            self.stat_score.num_classes = num_classes + 1

    # override
    def update(
        self,
        prediction: Union[BaseFormat, BatchedFormat],
        target: Union[BaseFormat, BatchedFormat],
    ):
        """Convert target & prediction to semantic mask to compute stats in semantic segmentation paradigm. Update internal state."""
        prediction = (
            BatchedFormat([prediction])
            if not isinstance(prediction, BatchedFormat)
            else prediction
        )
        target = (
            BatchedFormat([target]) if not isinstance(target, BatchedFormat) else target
        )
        assert isinstance(prediction[0][0], InstanceMaskFormat) and isinstance(
            target[0][0], InstanceMaskFormat
        ), f"To use SemanticSegmentationMetrics format of model prediction and target must be InstanceMaskFormat. Got {type(prediction[0])} and {target[0]}"
        for pred, targ in zip(prediction, target):
            # handling empty target
            if targ.nb_object == 0:
                semantic_target_mask = torch.zeros(targ.canvas_size).to(self.device)
            else:
                semantic_target_mask = targ.export_semantic_mask()
            # handling empty prediction
            if pred.nb_object == 0:
                semantic_prediction_mask = torch.zeros(pred.canvas_size).to(self.device)
            else:
                semantic_prediction_mask = pred.export_semantic_mask()
            # flatten and add dummy dim for stat score
            flatpred = semantic_prediction_mask.flatten()[None, :]
            flattarget = semantic_target_mask.flatten()[None, :]
            if self.task == "binary":
                self.stats.append(self.stat_score(flatpred, flattarget))
            else:
                # for multiclass will remove the background scores to avoid crazy high scores
                self.stats.append(self.stat_score(flatpred, flattarget)[:, 1:, :])
