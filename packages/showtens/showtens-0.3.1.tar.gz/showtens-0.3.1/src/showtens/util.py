from .imports import import_torch, import_torchvision
import os

torch = import_torch()


@torch.no_grad()
def gridify(
    tensor: torch.Tensor,
    max_width: int | None = None,
    columns: int | None = None,
    padding: int = 3,
    pad_value: float = 0.0,
) -> torch.Tensor:
    """
    Makes a grid of images/videos from a batch of images.
    Like torchvision's make_grid, but more flexible.
    Accepts (B,\\*,H,W)

    Args:
        tensor : (B,\\*,H,W) tensor
        max_width : max width of the output grid. Resizes images to fit the width
        columns : number of columns of the grid. If None, uses 8 or less
        padding : padding to add to the images
        pad_value : color of the padding

    Returns:
        (\\*,H',W') tensor, representing the grid of images/videos
    """
    transf = import_torchvision().transforms

    B, H, W = tensor.shape[0], tensor.shape[-2], tensor.shape[-1]
    device = tensor.device
    if columns is not None:
        numCol = columns
    else:
        numCol = min(8, B)

    black_cols = (-B) % numCol
    tensor = torch.cat(
        [tensor, torch.zeros(black_cols, *tensor.shape[1:], device=device)], dim=0
    )  # (B',*,H,W)
    tensor = transf.Pad(padding, fill=pad_value)(tensor)  # (B',*,H+padding*2,W+padding*2)

    B, H, W = tensor.shape[0], tensor.shape[-2], tensor.shape[-1]
    rest_dim = tensor.shape[1:-2]

    rest_dim_prod = 1
    for dim in rest_dim:
        rest_dim_prod *= dim

    if max_width is not None:
        resize_ratio = max_width / (W * numCol)
        if resize_ratio < 1:
            indiv_tens_size = int(H * resize_ratio), int(W * resize_ratio)
            tensor = tensor.reshape((B, rest_dim_prod, H, W))
            tensor = transf.Resize(indiv_tens_size, antialias=True)(tensor)  # (B',rest_dim_prod,H',W')

    B, H, W = tensor.shape[0], tensor.shape[-2], tensor.shape[-1]
    assert B % numCol == 0

    numRows = B // numCol

    tensor = tensor.reshape((numRows, numCol, rest_dim_prod, H, W))  # (numRows,numCol,rest_dim_prod,H',W')
    tensor = torch.einsum("nmrhw->rnhmw", tensor)  # (rest_prod,numRows,H',numCol,W')
    tensor = tensor.reshape((rest_dim_prod, numRows * H, numCol * W))  # (rest_prod,numRows*H,numCol*W)
    tensor = tensor.reshape((*rest_dim, numRows * H, numCol * W))  # (*,numRows*H,numCol*W)

    return tensor


@torch.no_grad()
def _create_folder(folder: str, create_folder: bool = True):
    if create_folder:
        os.makedirs(folder, exist_ok=True)
    else:
        if not (os.path.exists(folder)):
            raise FileNotFoundError(f"Folder {folder} does not exist !")


@torch.no_grad()
def _format_image(
    tensor: torch.Tensor,
    columns: int = None,
    rescale: bool = False,
    clamp_range: tuple[float] = (0.0, 1.0),
    max_width: int = None,
    padding: int = 3,
    pad_value: float = 0.0,
):
    """
    Shows tensor as an image using pyplot.
    Any extra dimensions **(\\*,C,H,W)** are treated as batch dimensions.

    Args:
        tensor : (H,W) or (C,H,W) or (\\*,C,H,W) tensor to display
        columns : number of columns to use for the grid of images (default 8 or less)
        max_width : maximum width of the image
        padding : number of pixels between images in the grid
        pad_value : inter-padding value for the grid of images
    """
    tensor = tensor.detach().cpu()

    extra_params = dict(
        columns=columns,
        max_width=max_width,
        pad_value=pad_value,
        padding=padding,
        rescale=rescale,
        clamp_range=clamp_range,
    )
    if len(tensor.shape) == 2:
        # Add batch and channel dimensions
        return _format_image(tensor[None, :, :], **extra_params)
    elif len(tensor.shape) == 3:
        # Reached (C,H,W)
        tensor = _rescale_images(tensor, rescale=rescale, clamp_range=clamp_range)
        return tensor
    elif len(tensor.shape) == 4:
        # Gridify assuming (B,C,H,W)
        B = tensor.shape[0]
        if columns is not None:
            numCol = columns
        else:
            numCol = min(8, B)

        tensor = _rescale_images(tensor, rescale=rescale, clamp_range=clamp_range)  # (B,C,H,W), rescaled
        tensor = gridify(
            tensor, columns=numCol, max_width=max_width, pad_value=pad_value, padding=padding
        )  # (C,H',W')

        return tensor
    elif len(tensor.shape) > 4:
        # Collapse extra dimension to batch
        tensor = tensor.reshape(
            (-1, tensor.shape[-3], tensor.shape[-2], tensor.shape[-1])
        )  # assume all batch dimensions
        print("Assuming extra dimension are all batch dimensions, newshape : ", tensor.shape)
        return _format_image(tensor, **extra_params)
    else:
        raise Exception(f"Tensor shape should be (H,W), (C,H,W) or (*,C,H,W), but got : {tensor.shape} !")


@torch.no_grad()
def _rescale_images(tensor: torch.Tensor, rescale: bool, clamp_range: tuple[float] = None):
    """
    Clamp to clamp_range if not None, then rescale the images to 0-1 range.
    The rescaling is dynamic with min and max values for each image channel.

    Args:
        tensor : (B,C,H,W) or (C,H,W) tensors to display
        rescale : whether to rescale the images to 0-1 range
        clamp_range : (min,max), tuple of values to clamp the images to, before rescaling
    """
    if clamp_range is not None:
        tensor = tensor.clamp(min=clamp_range[0], max=clamp_range[1])

    wasthree = False
    if len(tensor.shape) == 3:
        tensor = tensor[None, :, :, :]
        wasthree = True

    B, C, H, W = tensor.shape
    tensor = tensor.reshape(B, C, H * W)
    if rescale:
        maxes, _ = torch.max(tensor, dim=2, keepdim=True)  # (B,C,1) Max value for each image channel
        mins, _ = torch.min(tensor, dim=2, keepdim=True)
        tensor = (tensor - mins) / (torch.maximum(maxes - mins, torch.tensor(1e-5)))  # rescale
    tensor = tensor.reshape(B, C, H, W)
    if wasthree:
        tensor = tensor[0]
    return tensor
