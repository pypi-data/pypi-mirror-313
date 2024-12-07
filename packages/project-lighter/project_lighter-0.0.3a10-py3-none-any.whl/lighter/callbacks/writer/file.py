from typing import Callable, Dict, Union

from functools import partial

import torch
import torchvision
from monai.data import metatensor_to_itk_image
from monai.transforms import DivisiblePad
from torch import Tensor

from lighter.callbacks.utils import preprocess_image
from lighter.callbacks.writer.base import LighterBaseWriter
from lighter.utils.dynamic_imports import OPTIONAL_IMPORTS


class LighterFileWriter(LighterBaseWriter):
    """
    Writer for writing predictions to files. Supports writing tensors, images, videos, and ITK images.
    To write to other formats, a custom writer function can be provided to the `writer` argument or,
    for a more permanent solution, it can be added to the `self.writers` dictionary.

    Args:
        path (Union[str, Path]): Directory where the files should be written.
        writer (Union[str, Callable]): Name of the writer function registered in `self.writers` or a custom writer function.
            Available writers: "tensor", "image", "video", "itk_nrrd", "itk_seg_nrrd", "itk_nifti".
            A custom writer function must take two arguments: `path` and `tensor`, and write the tensor to the specified path.
            `tensor` is a single tensor without the batch dimension.
    """

    @property
    def writers(self) -> Dict[str, Callable]:
        return {
            "tensor": write_tensor,
            "image": write_image,
            "video": write_video,
            "itk_nrrd": partial(write_itk_image, suffix=".nrrd"),
            "itk_seg_nrrd": partial(write_itk_image, suffix=".seg.nrrd"),
            "itk_nifti": partial(write_itk_image, suffix=".nii.gz"),
        }

    def write(self, tensor: Tensor, id: Union[int, str]) -> None:
        """
        Write the tensor using the writer specified at the instatiation.

        Args:
            tensor (Tensor): Tensor, without the batch dimension, to be written.
            id (Union[int, str]): Identifier, used for file-naming.
        """
        if not self.path.is_dir():
            raise RuntimeError(f"LighterFileWriter expects a directory path, got {self.path}")

        # Determine the path for the file based on prediction count. The suffix must be added by the writer function.
        path = self.path / str(id)
        # Write the tensor to the file.
        self.writer(path, tensor)


def write_tensor(path, tensor):
    torch.save(tensor, path.with_suffix(".pt"))


def write_image(path, tensor):
    path = path.with_suffix(".png")
    tensor = preprocess_image(tensor)
    torchvision.io.write_png(tensor, path)


def write_video(path, tensor):
    path = path.with_suffix(".mp4")
    # Video tensor must be divisible by 2. Pad the height and width.
    tensor = DivisiblePad(k=(0, 2, 2), mode="minimum")(tensor)
    # Video tensor must be THWC. Permute CTHW -> THWC.
    tensor = tensor.permute(1, 2, 3, 0)
    # Video tensor must have 3 channels (RGB). Repeat the channel dim to convert grayscale to RGB.
    if tensor.shape[-1] == 1:
        tensor = tensor.repeat(1, 1, 1, 3)
    # Video tensor must be in the range [0, 1]. Scale to [0, 255].
    tensor = (tensor * 255).to(torch.uint8)
    torchvision.io.write_video(str(path), tensor, fps=24)


def write_itk_image(path: str, tensor: Tensor, suffix) -> None:
    path = path.with_suffix(suffix)
    itk_image = metatensor_to_itk_image(tensor, channel_dim=0, dtype=tensor.dtype)
    OPTIONAL_IMPORTS["itk"].imwrite(itk_image, str(path), True)
