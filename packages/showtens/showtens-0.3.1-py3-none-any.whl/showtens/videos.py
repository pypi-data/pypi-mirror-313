import os
from .util import gridify, import_torch, _create_folder
import cv2, numpy as np

torch = import_torch()


@torch.no_grad()
def show_video(
    tensor: torch.Tensor,
    fps: int = 30,
    columns: int | None = None,
    max_width: int | None = None,
    padding: int = 3,
    pad_value: float = 0.0,
) -> None:
    """
    Shows tensor as a video. Accepts both **(T,H,W)**, **(T,3,H,W)** and **(\\*,T,3,H,W)** tensors.
    Tensor should be a float tensor with values in [0,1]. Clips the values otherwise.

    NOT IMPLEMENTED YET

    Args:
        tensor : (T,H,W) or (T,3,H,W) or (\\*,T,3,H,W) float tensor
        columns : number of columns to use for the grid of videos (default 8 or less)
        fps : fps of the video (default 30)
        out_size : Height of output video (height adapts to not deform videos) (default 800)
    """
    return NotImplementedError("showVideo not implemented yet, use saveVideo instead")


@torch.no_grad()
def save_video(
    tensor: torch.Tensor,
    folder: str,
    name: str = "videotensor",
    fps: int = 30,
    columns: int | None = None,
    max_width: int | None = None,
    padding: int = 3,
    pad_value: float = 0.0,
    create_folder: bool = True,
) -> None:
    """
    Shows tensor as a video. Accepts both **(T,H,W)**, **(T,3,H,W)** and **(\\*,T,3,H,W)** tensors.
    Tensor should be a float tensor with values in [0,1]. Clips the values otherwise.

    Args:
        tensor : (T,H,W) or (T,3,H,W) or (\\*,T,3,H,W) float tensor
        folder : path to save the video
        name : name of the video
        fps : fps of the video (default 30)
        columns : number of columns to use for the grid of videos (default 8 or less)
        max_width : maximum width of the image
        padding : number of pixels between images in the grid
        pad_value : inter-padding value for the grid of images
    """
    _create_folder(folder, create_folder)

    tensor = _format_video(
        tensor, columns=columns, fps=fps, max_width=max_width, padding=padding, pad_value=pad_value
    )  # (T,3,H',W') ready to save
    T, C, H, W = tensor.shape
    output_file = os.path.join(folder, f"{name}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_file, fourcc, fps, (W, H))

    to_save = (255 * tensor.permute(0, 2, 3, 1).cpu().numpy()).astype(np.uint8)

    for t in range(T):
        frame = to_save[t]
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        video.write(frame)

    video.release()


def _format_video(tensor, columns=None, fps=30, max_width=None, padding=3, pad_value=0.0):
    """
    Formats tensor as a video. Accepts both (T,H,W), (T,3,H,W) and (\\*,T,3,H,W) float tensors.
    Assumes that the tensor value are in [0,1], clips them otherwise.

    Args:
        tensor : (T,H,W) or (T,3,H,W) or (\\*,T,3,H,W) float tensor
        columns : number of columns to use for the grid of videos (default 8 or less)
        fps : fps of the video (default 30)
        max_width : maximum width of the image
        padding : number of pixels between images in the grid
        pad_value : inter-padding value for the grid of images
    """
    tensor = tensor.detach().cpu()
    extra_params = dict(columns=columns, fps=fps, max_width=max_width, pad_value=pad_value, padding=padding)

    if len(tensor.shape) == 3:
        # add channel dimension
        tensor = tensor[:, None, :, :].expand(-1, 3, -1, -1)  # (T,3,H,W)
        return _format_video(tensor, **extra_params)
    elif len(tensor.shape) == 4:
        if tensor.shape[1] == 1:
            print("Assuming gray-scale video")
            tensor = tensor.expand(-1, 3, -1, -1)  # (T,3,H,W)
        assert tensor.shape[1] == 3, f"Tensor shape should be (T,H,W), (T,3,H,W) or (*,T,3,H,W) !"
        # A single video
        return tensor
    elif len(tensor.shape) == 5:
        tensor = gridify(tensor, max_width=max_width, columns=columns, padding=padding, pad_value=pad_value)
        return _format_video(tensor, **extra_params)
    elif len(tensor.shape) > 5:
        tensor = tensor.reshape((-1, *tensor.shape[-4:]))
        return _format_video(tensor, **extra_params)
    else:
        raise ValueError(f"Tensor shape should be (T,H,W), (T,3,H,W) or (*,T,3,H,W), but got : {tensor.shape} !")
