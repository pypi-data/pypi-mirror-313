def import_torch():
    """
    Lazily import torch, giving helpful error message if not installed.
    """
    try:
        import torch

        return torch
    except ImportError:
        raise ImportError(
            "PyTorch is not installed. ShowTens requires PyTorch. "
            "Please install it with one of the following commands:\n\n"
            "- For CPU only: pip install torch\n"
            "- For CUDA support: Visit https://pytorch.org for installation instructions "
            "specific to your system and CUDA version."
        )


def import_torchvision():
    """
    Lazily import torchvision.transforms, giving helpful error message if not installed.
    """
    try:
        import torchvision

        return torchvision
    except ImportError:
        raise ImportError(
            "torchvision is not installed. ShowTens requires torchvision. "
            "Please install it with the following command:\n\n"
            "pip install torchvision"
        )


# torch = import_torch()
