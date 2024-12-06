from detectools import Configuration


class ConfigurationException(Exception):
    def __init__(self):
        message = f"Configuration() is not properly set, yolo requires Configuration().data_type to be bbox or instance_mask got {Configuration().data_type}"
        super().__init__(message)


class P6Exception(Exception):
    def __init__(self):
        message = f"p6 or p2 yolov8 models don't have pretrained weights. Please switch pretrained to False"
        super().__init__(message)


def check_config(architecture, pretrained):
    if (
        Configuration().data_type == "bbox"
        or Configuration().data_type == "instance_mask"
    ):
        pass
    else:
        raise ConfigurationException()
    if ("-p6" in architecture or "-p2" in architecture) and pretrained:
        raise P6Exception()
