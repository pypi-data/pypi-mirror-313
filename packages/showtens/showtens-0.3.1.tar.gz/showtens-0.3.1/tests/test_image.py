import sys, pathlib, os

sys.path.append(pathlib.Path(__file__).parent.parent.as_posix())

from src.showtens.util import import_torch, import_torchvision

# None implemented yet
from src.showtens import show_image, save_image

curpath = pathlib.Path(__file__).parent


def test_view():
    """
    Unfortunately I see no way to write automatic unit tests for this function.
    """
    from PIL import Image

    torch = import_torch()
    transf = import_torchvision().transforms
    image = Image.open(os.path.join(curpath, "test_folder", "whale.png"))

    whale = transf.ToTensor()(image)  # (4,H,W);
    randAug = transf.RandomResizedCrop(whale.shape[-2:])
    whale_tile = torch.stack([randAug(whale) for _ in range(7)], dim=0)  # (9,3,H,W)

    alpha_noise = torch.rand(7, 1, *whale.shape[-2:])
    whale_tile[:, 3:, :, :] = whale_tile[:, 3:, :, :] * (alpha_noise)  # (9,4,H,W)
    num, _, H, W = whale_tile.shape
    print("first, expected shape : ", (H * 2, W * 4))
    show_image(whale_tile, columns=4, colorbar=False, max_width=None, padding=0, pad_value=1.0)
    print("Second, expected max_width : 500, figure shape : ", (H * 2, W * 4))
    show_image(whale_tile[:, 2:3], columns=None, colorbar=True, max_width=500, padding=3, pad_value=0.0)


def test_save():
    """
    Unfortunately I see no way to write automatic unit tests for this function.
    """
    from PIL import Image

    torch = import_torch()
    transf = import_torchvision().transforms
    image = Image.open(os.path.join(curpath, "test_folder", "whale.png"))

    whale = transf.ToTensor()(image)  # (4,H,W);
    randAug = transf.RandomResizedCrop(whale.shape[-2:])
    whale_tile = torch.stack([randAug(whale) for _ in range(9)], dim=0)  # (9,4,H,W)

    _, _, H, W = whale_tile.shape

    print("Expected shape : ", (H * 2, W * 5))
    save_image(
        whale_tile,
        folder="test_folder",
        name="whale_list",
        columns=5,
        colorbar=False,
        max_width=None,
        padding=0,
        pad_value=1.0,
    )
    save_image(
        whale_tile[:, 2:3],
        folder="test_folder",
        name="dawhales",
        columns=None,
        colorbar=True,
        max_width=500,
        padding=3,
        pad_value=0.0,
    )


# # test_save()
# test_view()
# test_save()
