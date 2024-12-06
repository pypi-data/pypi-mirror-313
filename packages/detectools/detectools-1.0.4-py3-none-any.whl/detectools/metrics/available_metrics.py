from typing import Dict

import detectools.metrics.func as F
from detectools.formats import BaseFormat, BboxFormat
from detectools.metrics.base_metric import (
    DetectMetric,
    ClassWiseDetectMetric,
    ClassifMetric,
    SemanticSegmentationMetric,
)
from torch import Tensor
from torchmetrics.detection import MeanAveragePrecision
from detectools.formats import BatchedFormat


class DetectF1score(DetectMetric):
    """F1 score for detection task."""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.f1score, name="DetectF1score", *args, **kwargs)


class ClassWiseDetectF1score(ClassWiseDetectMetric):
    """Similar as DetectF1score but with multiclass detail. Samplewise is not provided in that case.
    Multiclass is handled by removing all other classes objects than the considered one in target and prediction for tp, fp, tn, fn computation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            func=F.f1score,
            name="classwise_DetectF1score",
            *args,
            **kwargs,
        )


class DetectPrecision(DetectMetric):
    """Precision for detection task."""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.precision, name="DetectPrecision", *args, **kwargs)


class ClassWiseDetectPrecision(ClassWiseDetectMetric):
    """Similar as DetectPrecision but with multiclass detail. Samplewise is not provided in that case.
    Multiclass is handled by removing all other classes objects than the considered one in target and prediction for tp, fp, tn, fn computation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            func=F.precision,
            name="classwise_DetectPrecision",
            *args,
            **kwargs,
        )


class DetectRecall(DetectMetric):
    """Recall for detection task."""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.recall, name="DetectRecall", *args, **kwargs)


class ClassWiseDetectRecall(ClassWiseDetectMetric):
    """Similar as DetectRecall but with multiclass detail. Samplewise is not provided in that case.
    Multiclass is handled by removing all other classes objects than the considered one in target and prediction for tp, fp, tn, fn computation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            func=F.recall,
            name="classwise_DetectRecall",
            *args,
            **kwargs,
        )


class DetectAccuracy(DetectMetric):
    """Accuracy for detection task. In case of detection, tn is none : -> 0 for computation"""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.accuracy, name="DetectAccuracy", *args, **kwargs)


class ClassWiseDetectAccuracy(ClassWiseDetectMetric):
    """Similar as DetectAccuracy but with multiclass detail. Samplewise is not provided in that case.
    Multiclass is handled by removing all other classes objects than the considered one in target and prediction for tp, fp, tn, fn computation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            func=F.accuracy,
            name="classwise_DetectAccuracy",
            *args,
            **kwargs,
        )


class ClassifAccuracy(ClassifMetric):
    """Classification accuracy score"""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.accuracy, name="ClassifAccuracy", *args, **kwargs)


class ClassifF1score(ClassifMetric):
    """Classification F1 score"""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.f1score, name="ClassifF1score", *args, **kwargs)


class ClassifRecall(ClassifMetric):
    """Classification recall score"""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.recall, name="ClassifRecall", *args, **kwargs)


class ClassifAccuracy(ClassifMetric):
    """Classification precision score"""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.precision, name="ClassifPrecision", *args, **kwargs)


class SemanticIoU(SemanticSegmentationMetric):
    """Semantic iou score"""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.iou, name="SemanticIoU", *args, **kwargs)


class SemanticF1score(SemanticSegmentationMetric):
    """Semantic F1 score"""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.f1score, name="SemanticF1score", *args, **kwargs)


class SemanticAccuracy(SemanticSegmentationMetric):
    """Semantic accuracy score"""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.accuracy, name="Semanticaccuracy", *args, **kwargs)


class SemanticPrecision(SemanticSegmentationMetric):
    """Semantic precision score"""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.precision, name="SemanticPrecision", *args, **kwargs)


class SemanticRecall(SemanticSegmentationMetric):
    """Semantic recall score"""

    def __init__(self, *args, **kwargs):
        super().__init__(func=F.recall, name="SemanticRecall", *args, **kwargs)


class MeanAP(MeanAveragePrecision):
    """Compute Mean Average Precision (from torchmetrics MAP_ ).

    .. _MAP:
        https://lightning.ai/docs/torchmetrics/stable/detection/mean_average_precision.html

        Note : this metric neads pycocotools
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "MeanAP"

    def prepare_input(self, input: BaseFormat) -> Dict[str, Tensor]:
        """Transform BaseFormat into MAp inputs type.

        Args:
            input (``BaseFormat``): BaseFormat to convert.

        Returns:
            ``Dict[str, Tensor]``:
                - Dict of values for MAP computation.
        """
        boxes = (
            input.data.value
            if isinstance(input, BboxFormat)
            else BboxFormat.from_instance_mask(input).data.value
        )
        labels = input.labels
        prepared = {"boxes": boxes, "labels": labels}
        if input.scores != None:
            prepared.update({"scores": input.scores})
        return [prepared]

    def update(self, prediction: BaseFormat, target: BaseFormat):
        """Prepare inputs and call MAP.

        Args:
            prediction (``BaseFormat``): Predictions.
            target (``BaseFormat``): Targets.
        """
        prediction = (
            BatchedFormat([prediction])
            if not isinstance(prediction, BatchedFormat)
            else prediction
        )
        target = (
            BatchedFormat([target]) if not isinstance(target, BatchedFormat) else target
        )
        for pred, targ in zip(prediction, target):
            pred = self.prepare_input(pred)
            targ = self.prepare_input(targ)
            super().update(pred, targ)
