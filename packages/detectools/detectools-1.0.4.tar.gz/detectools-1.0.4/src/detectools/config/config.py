from typing import Literal, Union
import detectools.config.errors as er
import numpy as np
import torch
import random as rd


class _SingletonConfig(type):
    """Metaclass for Config class Singleton design pattern"""

    _instance = None

    def __call__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Configuration(metaclass=_SingletonConfig):
    """Configuration class for detectools (Singleton -> can be instancied once and then point to same object). Store all configuration information about the library configuration.
    If you wish to changes parameters later on, you can simply modify the corresponding attributes.


    Args:
        device (``Literal[&quot;cpu&quot;, &quot;cuda&quot;]``, **optional**): Device to be used by default when creating objects, running models etc. Defaults to "cpu".
        data_type (``Literal[&quot;instance_mask&quot;, &quot;bbox&quot;, &quot;keypoint&quot;]``, **optional**): Default format to use in dataset, models, prediction etc. Defaults to "bbox".
        num_classes (``int``, **optional**): Number of classes in model. Defaults to 1.
        mask_min_size (``int``, **optional**): Minimal size of mask to be considered : below this threshold annotation will be ignored. Defaults to 15.
        splitted_mask_handling (``bool``, **optional**): If set to True redefine masks that are splitted (after cropping for example) so they belong to independant objects. Defaults to False.
        model_nms_threshold (``float``, **optional**): Default nms iou threshold used in models. Defaults to 0.45.
        model_confidence_threshold (``float``, **optional**): Default model confidence threshold to consider it a valid object prediction. Defaults to 0.5.
        model_max_detection (``int``, **optional**): Maximum number of objects outputed by a model (useful for some models such as yolo type models). Defaults to 300.
        metrics_matcher_type (``Literal[&quot;bbox&quot;, &quot;instance_mask&quot;]``, **optional**): Object matcher data type used in metrics (note that instance_mask is slower because needs transition to cpu to save gpu memory). If data_type is instance mask and matcher type is bbox will convert it to bbox for matching in metrics. Defaults to "bbox".
        metrics_match_iou_threshold (``float``, **optional**): Metrics matcher iou threshold. Defaults to 0.45.
        patchifier_mode (``Literal[&quot;bbox&quot;, &quot;instance_mask&quot;]``, **optional**): Patchifier data type used for nms and duplicate supresser. If data_type is mask and patchifier to bbox will convert for according operations. Defaults to "bbox".
        seed (``Union[False, int]``, **optional**): use a manual seed to enforce reproducibility (you probably want to also switch deterministic to True in that case). If False it ends reproducibility. Defaults to False.
        deterministic (``bool``, **optional**): Use deterministic algorithms. Helps further reproducibility (see also seeds). Be careful : some models can't be deterministic so sometimes you need to switch it to False even if you are manually seeding. Defaults to False.


    Example:
    ----------

    .. highlight:: python
    .. code-block:: python

        >>> from detectools import Configuration()
        >>> config = Configuration(data_type = "instance_mask") # can instantiate with given parameter
        >>> config.device = "cuda"  # can modify parameters by modifying attributes / properties


    Attributes
    ----------

    Attributes:
        - data_type (``Literal[&quot;instance_mask&quot;, &quot;bbox&quot;, &quot;keypoint&quot;]``, **optional**): Default format to use in dataset, models, prediction etc. Defaults to "bbox".
        - num_classes (``int``): Number of classes in model. Defaults to 1.
        - mask_min_size (``int``): Minimal size of mask to be considered : below this threshold annotation will be ignored. Defaults to 15.
        - splitted_mask_handling (``bool``): If set to True redefine masks that are splitted (after cropping for example) so they belong to independant objects. Defaults to False.
        - model_nms_threshold (``float``): Default nms iou threshold used in models. Defaults to 0.45.
        - model_confidence_threshold (``float``): Default model confidence threshold to consider it a valid object prediction. Defaults to 0.5.
        - model_max_detection (``int``): Maximum number of objects outputed by a model (useful for some models such as yolo type models). Defaults to 300.
        - metrics_matcher_type (``Literal[&quot;bbox&quot;, &quot;instance_mask&quot;]``): Object matcher data type used in metrics. If data_type is instance mask and matcher type is bbox will convert it to bbox for matching in metrics. Defaults to "bbox".
        - metrics_match_iou_threshold (``float``): Metrics matcher iou threshold. Defaults to 0.45.
        - patchifier_mode (``Literal[&quot;bbox&quot;, &quot;instance_mask&quot;]``): Patchifier data type used for nms and duplicate supresser. If data_type is mask and patchifier to bbox will convert for according operations. Defaults to "bbox".


    Attributes
    ----------

    Properties:
        - device (``Literal[&quot;cpu&quot;, &quot;cuda&quot;]``): Device to be used by default when creating objects, running models etc. Defaults to "cpu".
        - seed (``Union[False, int]``, **optional**): use a manual seed to enforce reproducibility (you probably want to also switch deterministic to True in that case). If False it ends reproducibility. Defaults to False.
        - deterministic (``bool``, **optional**): Use deterministic algorithms. Helps further reproducibility (see also seeds). Be careful : some models can't be deterministic so sometimes you need to switch it to False even if you are manually seeding. Defaults to False.



    Notes:
        1) If you use instance_mask, bbox will included when needed from the masks.
        2) you can change model_nms_threshold and model_confidence_threshold for the entire lib by modifying the attributes
        3) In instance mode, by default the target ``Format`` remove small objects in case their masks contains less than min_mask_threshold (default 5 pixels).
        Change the attribute to modify this behaviour.
        4) The option splitted_mask_handling is by default False.
        If you set to True, when performing transformation on object mask that split it into discontinuous sub-masks the library creates new objects for every sub-masks.
        Otherwise they will still be describing the same unique object

    """

    def __init__(
        self,
        device: Literal["cpu", "cuda"] = "cpu",
        data_type: Literal["instance_mask", "bbox", "keypoint"] = "bbox",
        num_classes: int = 1,
        mask_min_size: int = 15,
        splitted_mask_handling: bool = False,
        model_nms_threshold: float = 0.45,
        model_confidence_threshold: float = 0.5,
        model_max_detection: int = 300,
        metrics_matcher_type: Literal["bbox", "instance_mask"] = "bbox",
        metrics_match_iou_threshold: float = 0.45,
        patchifier_mode: Literal["bbox", "instance_mask"] = "bbox",
        seed: Union[False, int] = False,
        deterministic: bool = False,
    ):

        # generic
        self.data_type = data_type
        self.device: str = device
        self.num_classes: int = num_classes
        # Format specific parameters
        self.mask_min_size = mask_min_size
        self.splitted_mask_handling = splitted_mask_handling
        # Model build_results parameters
        self.model_nms_threshold = model_nms_threshold
        self.model_confidence_threshold = model_confidence_threshold
        self.model_max_detection = model_max_detection
        # metrics params
        self.metrics_matcher_type = metrics_matcher_type
        self.metrics_match_iou_threshold = metrics_match_iou_threshold
        # patchifier setup
        self.patchifier_mode = patchifier_mode
        # reproducibility
        self.seed = seed
        self.deterministic = deterministic

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, val: Literal["cpu", "cuda"]):
        er.check_device_availability(val)
        self._device = val

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, val: Union[False, int]):
        assert val == False or isinstance(
            val, int
        ), f"seed must be a int or False. Got {val}"
        if val:
            rd.seed(val)
            np.random.seed(val)
            torch.manual_seed(val)
        else:
            rd.seed()
            np.random.seed()
            torch.seed()
        self._seed = val

    @property
    def deterministic(self):
        return self.deterministic

    @deterministic.setter
    def deterministic(self, val: bool):
        assert isinstance(val, bool), f"deterministic must be a bool, got {val}"
        if val:
            torch.use_deterministic_algorithms(True)
            # disable convolutions benchmark
            if torch.cuda.is_available():
                torch.backends.cudnn.benchmark = False
        else:
            torch.use_deterministic_algorithms(False)
            # disable convolutions benchmark
            if torch.cuda.is_available():
                torch.backends.cudnn.benchmark = True
        self._deterministic = val
