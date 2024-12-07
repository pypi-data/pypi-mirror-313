import os
import matplotlib.pyplot as plt
from .imports import import_torch, import_torchvision
from .util import gridify, _create_folder, _format_image

torch = import_torch()
torchvision = import_torchvision()


@torch.no_grad()
def show_image(
    tensor: torch.Tensor,
    columns: int | None = None,
    rescale: bool = False,
    clamp_range: tuple[float] = (0.0, 1.0),
    colorbar: bool = False,
    max_width: int | None = None,
    padding: int = 3,
    pad_value: float = 0.0,
) -> None:
    """
    Shows tensor of shape **(\\*,C,H,W)** as an image using pyplot.
    Any extra dimensions are treated as batch dimensions, and displayed in a grid.
    By default, the image is simply clipped to the 0-1 range. Use rescale and clamp_range to modify this behaviour.

    Args:
        tensor : (H,W) or (C,H,W) or (\\*,C,H,W) tensor to display
        columns : number of columns to use for the grid of images (default 8 or less)
        rescale : whether to rescale the images to 0-1 range. Uses min-max scaling.
        clamp_range : (min,max), tuple of values to clamp the images to, before rescaling. Use None to disable clamping
        colorbar : whether to add a colorbar to the image, only works for grayscale images (default False)
        max_width : maximum width of the image
        padding : number of pixels between images in the grid
        pad_value : inter-padding value for the grid of images
    """
    tensor = _format_image(
        tensor,
        columns=columns,
        rescale=rescale,
        clamp_range=clamp_range,
        max_width=max_width,
        padding=padding,
        pad_value=pad_value,
    )  # (C,H',W') ready to show
    C, H, W = tensor.shape
    plt.figure(figsize=(W / 50, H / 50), dpi=50)
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Remove margins

    plt.imshow(tensor.permute((1, 2, 0)))
    plt.axis("off")
    if tensor.shape[0] == 1 and colorbar:
        plt.colorbar()
    plt.show()


@torch.no_grad()
def save_image(
    tensor: torch.Tensor,
    folder: str,
    name: str = "imagetensor",
    columns: int | None = None,
    rescale: bool = False,
    clamp_range: tuple[float] = (0.0, 1.0),
    colorbar: bool = False,
    max_width: int | None = None,
    padding: int = 3,
    pad_value: float = 0.0,
    create_folder: bool = True,
) -> None:
    """
    Saves tensor of shape **(\\*,C,H,W)** as an image using pyplot.
    Any extra dimensions are treated as batch dimensions, and displayed in a grid.
    By default, the image is simply clipped to the 0-1 range. Use rescale and clamp_range to modify this behaviour.

    Args:
        tensor : (H,W) or (C,H,W) or (\\*,C,H,W) tensor to display
        folder : relative path of folder where to save the image
        name : name of the image (do not include extension)
        columns : number of columns to use for the grid of images (default 8 or less)
        rescale : whether to rescale the images to 0-1 range
        clamp_range : (min,max), tuple of values to clamp the images to, before rescaling. Use None to disable clamping
        colorbar : whether to add a colorbar to the image, only works for grayscale images (default False)
        max_width : maximum width of the image
        padding : number of pixels between images in the grid
        pad_value : inter-padding value for the grid of images
        create_folder : whether to create the folder if it does not exist (default True)
    """
    _create_folder(folder, create_folder)

    tensor = _format_image(
        tensor,
        columns=columns,
        rescale=rescale,
        clamp_range=clamp_range,
        max_width=max_width,
        padding=padding,
        pad_value=pad_value,
    )  # (C,H',W') ready to save
    H, W = tensor.shape[1], tensor.shape[2]
    plt.figure(figsize=(W / 50, H / 50), dpi=50)
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Remove margins

    plt.imshow(tensor.permute((1, 2, 0)), extent=[0, W, 0, H])
    plt.axis("off")
    if tensor.shape[0] == 1 and colorbar:
        plt.colorbar()

    plt.savefig(os.path.join(folder, f"{name}.png"), dpi=50, bbox_inches="tight", pad_inches=0)
    plt.close()
