import torch


def check_device_availability(device):
    assert (
        device == "cpu" or device == "cuda"
    ), f"{device} is not a valid device, must be: cuda or: cpu"
    if device != "cpu":
        assert (
            torch.cuda.is_available()
        ), "CUDA seems unavailable. Please run torch.cuda.is_available() to verify"
    pass
