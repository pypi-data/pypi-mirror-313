# ShowTens : visualize torch tensors EASILY

ShowTens is a simple pytorch package that allows painless and flexible visualizations of image and video tensors.

\<ADD VISUALIZATION VIDEO HERE\>

## Installation

`pip install showtens`

Make sure `torch`and `torchvision` are installed, as the package depends on them.

## Usage
```python
import torch
from showtens import show_image

image1 = torch.rand((3, 100, 100))  # (C,H,W) image
show_image(image1)  # Displays the image using matplotlib
image2 = torch.rand((4, 4, 3, 100, 100))  # (B1,B2,C,H,W), two batch dimensions
# Will display as a 4*4 grid, 2 pixel padding, white padding color:
show_image(image2, columns=4, padding=2, pad_value=1.0)

from showtens import save_image

save_image(tensor=image1, folder="saved_images", name="imagetensor")

from showtens import save_video

video1 = torch.rand((60, 3, 200, 200))
save_video(tensor=video1, folder="saved_videos", name="videotensor", fps=30)
video2 = torch.rand((4, 60, 3, 200, 200))  # (B,T,C,H,W), batch of videos
save_video(tensor=video2, folder="saved_videos", name="videobatch", fps=30, columns=2)  # 2*2 video grid

# show_video not available yet
```