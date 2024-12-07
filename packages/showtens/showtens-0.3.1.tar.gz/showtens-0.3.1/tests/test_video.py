import sys, pathlib, os

sys.path.append(pathlib.Path(__file__).parent.parent.as_posix())

from src.showtens.util import import_torch, import_torchvision

# None implemented yet
from src.showtens.videos import save_video

curpath = pathlib.Path(__file__).parent


def test_video():
    """
    Unfortunately I see no way to write automatic unit tests for this function.
    """
    read_video = import_torchvision().io.read_video
    transf = import_torchvision().transforms
    torch = import_torch()

    randAug = transf.RandomResizedCrop(224)

    video, _, _ = read_video(
        os.path.join(curpath, "test_folder/test_vid.mp4"), output_format="TCHW", pts_unit="sec"
    )

    video = video.to(torch.float32) / 255.0
    video = video[::2]

    video_tile = torch.stack([randAug(video) for _ in range(3)], dim=0)  # (10,T,3,H,W)
    save_video(
        video_tile,
        folder="test_folder",
        name="see_same",
        fps=30,
        columns=2,
        max_width=None,
        padding=3,
        pad_value=1.0,
        create_folder=True,
    )
