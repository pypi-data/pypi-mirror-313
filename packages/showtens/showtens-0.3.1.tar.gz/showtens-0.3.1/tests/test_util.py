import sys, pathlib, os

sys.path.append(pathlib.Path(__file__).parent.parent.as_posix())

from src.showtens.util import gridify, import_torch, import_torchvision, _rescale_images
# None implemented yet

curpath = pathlib.Path(__file__).parent


def test_grid_pytorch():
    from PIL import Image

    torch = import_torch()
    transf = import_torchvision().transforms

    torchgrid = import_torchvision().utils.make_grid

    image = Image.open(os.path.join(curpath, "test_folder", "whale.png"))
    whale = transf.ToTensor()(image)  # (3,H,W)
    randAug = transf.RandomResizedCrop(whale.shape[-2:])

    whale_tile = torch.stack([randAug(whale) for _ in range(9)], dim=0)  # (10,3,H,W)

    grid = gridify(whale_tile, columns=5, pad_value=1.0, padding=0)  # (3,H',W')
    gridtorch = torchgrid(whale_tile, nrow=5, padding=0, pad_value=0.0)  # (3,H',W')

    assert torch.allclose(
        grid - gridtorch, torch.tensor(0.0)
    ), f"My grid does not correspond to pytorch make_grid in the padding 0 case. Max_diff = {torch.max(torch.abs(grid-gridtorch))}"


def test_grid_size():
    torch = import_torch()
    tens_size = [8, 32, 64]
    padding = [3, 5, 8]
    num_cols = [3, 5, 8]
    for sizu, paddingu, colu in zip(tens_size, padding, num_cols):
        tensor = torch.rand(10, 3, sizu, sizu)
        grid = gridify(tensor, columns=colu, max_width=sizu // 2 * colu, padding=0)

        assert grid.shape[-1] == sizu // 2 * colu, "Grid does not have the right width"

        max_width = 104
        grid = gridify(tensor, columns=colu, max_width=max_width, padding=3)

        new_W = sizu + paddingu * 2
        reshape_ratio = max_width / (new_W * colu)
        if reshape_ratio < 1:
            image_size = int((new_W) * reshape_ratio)
        else:
            image_size = new_W

        assert (
            grid.shape[-1] == image_size * colu
        ), f"Expected width {image_size*colu}, but got {grid.shape[-1]}"


def test_rescale():
    torch = import_torch()
    a = torch.randn(5, 3, 32, 32)
    reshaped_a = a.reshape(5, 3, 32 * 32)

    just_clip = _rescale_images(a, clamp_range=(0.0, 1.0), rescale=False)
    assert torch.max(just_clip) <= 1.0 and torch.min(just_clip) >= 0.0, "Rescale failed to clip to range"

    rescaled = _rescale_images(a, clamp_range=None, rescale=True)
    maxes, max_ind = torch.max(reshaped_a, dim=2, keepdim=True)  # (5,3,1) maxes for each channel
    mins, min_ind = torch.min(reshaped_a, dim=2, keepdim=True)  # (5,3,1) mins for each channel
    reshaped_rescaled_a = rescaled.reshape(5, 3, 32 * 32)

    rescaled_maxes = torch.gather(reshaped_rescaled_a, 2, max_ind)  # should all be 1
    rescaled_mins = torch.gather(reshaped_rescaled_a, 2, min_ind)  # should all be 0

    assert torch.allclose(
        rescaled_maxes, torch.tensor(1.0)
    ), "Rescale failed to rescale maxes PER CHANNELIMAGE"
    assert torch.allclose(rescaled_mins, torch.tensor(0.0)), "Rescale failed to rescale mins PER CHANNELIMAGE"

    rescaled = _rescale_images(a, clamp_range=(-1.0, 1.0), rescale=True)
    where_clamped_low = a < -1.0
    where_clamped_high = a > 1.0

    assert torch.allclose(rescaled[where_clamped_low], torch.tensor(0.0)), "Rescale failed to clamp low"
    assert torch.allclose(rescaled[where_clamped_high], torch.tensor(1.0)), "Rescale failed to clamp high"


# test_rescale()
