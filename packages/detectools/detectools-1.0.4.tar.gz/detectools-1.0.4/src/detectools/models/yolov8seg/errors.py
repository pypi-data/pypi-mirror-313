from detectools import Configuration


class ConfigurationException(Exception):
    def __init__(self):
        message = f"Configuration() is not properly set, yolo requires Configuration().data_type to be instance_mask got {Configuration().data_type}"
        super().__init__(message)


def check_config():
    if Configuration().data_type == "instance_mask":
        pass
    else:
        raise ConfigurationException()
