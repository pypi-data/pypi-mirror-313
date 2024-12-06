import itertools
from collections.abc import Iterator
from typing import Any

import numpy as np
from accelerate import find_executable_batch_size
from napari.layers import Image
from napari.utils import notifications


def prepare_image(image: np.ndarray) -> np.ndarray:
    """
    Prepare image for processing (i.e., ensure proper dimensions).

    :param image: Image data (np.ndarray).

    :returns:
        2D image array (np.ndarray).
    """

    if image.ndim == 2:
        return image
    else:
        squeezed_image = np.squeeze(image)
        if squeezed_image.ndim == 2:
            return squeezed_image
        else:
            raise ValueError(
                f"Expected 2D image but got shape: {squeezed_image.shape}"
            )


def get_image_roi(
    image: np.ndarray, roi_coords: np.ndarray
) -> tuple[np.ndarray, tuple[int, int]]:
    """
    Get ROI from image.

    :param image: Image data (np.ndarray).
    :param roi_coords: ROI coordinates (np.ndarray).

    :returns:
        Tuple of image ROI (np.ndarray) and ROI offset relative to the input image (tuple[int, int]).
    """
    # use last 2 columns if number of columns is greater than 2.
    if roi_coords.shape[1] != 2:
        notifications.show_info(
            "Expected ROI to be (x,y) pairs. Reshaping ROI"
        )
        roi_coords = roi_coords[:, -2:]

    minr, minc = np.min(roi_coords, axis=0).astype(int)
    maxr, maxc = np.max(roi_coords, axis=0).astype(int)

    return image[minr:maxr, minc:maxc], (minr, minc)


def estimate_diameter(
    image: np.ndarray, model_type: str, use_gpu: bool
) -> np.ndarray[Any, np.dtype[np.float16]]:
    """
    Estimate diameters using cellpose size models.

    :param image: Image data (np.ndarray).
    :param model_type: Cellpose model type (str).
    :param use_gpu: whether to use gpu acceleration (bool).

    :returns:
        Estimated diameter (np.ndarray[Any, np.dtype[np.float16]]).
    """

    from cellpose import models

    model = models.Cellpose(model_type=model_type, gpu=use_gpu)
    diameter = model.sz.eval(image, channels=[0, 0], channel_axis=-1)[0]

    diameter = np.round(diameter, 2)

    del model
    return diameter


def restore_image(
    image: np.ndarray,
    image_name: str,
    restore_type: str,
    diameter: float,
    use_gpu: bool,
    batch_size: int,
) -> Image:
    """
    Run Cellpose image restoration

    :param image: Image layer (napari.layers.Image).
    :param image_name: Image name (str).
    :param restore_type: Restoration type (str).
    :param diameter: Object diameter in image (float).
    :param use_gpu: Whether to use GPU acceleration (bool).
    :param batch_size: Batch size for model inference (int).

    :returns:
        Restored image (napari.layers.Image).
    """

    image_name = f"{image_name}_{restore_type}"
    from cellpose.denoise import DenoiseModel

    restore_model = DenoiseModel(
        model_type=restore_type, diam_mean=diameter, gpu=use_gpu
    )

    restored_image = restore_model.eval(
        [image], channels=[0, 0], channel_axis=-1, batch_size=batch_size
    )

    del restore_model
    return Image(restored_image[0][:, :, 0], name=image_name, rgb=False)


def get_image_patches(
    image: np.ndarray,
    image_patch_dim: tuple[int, int],
    split_image_threshold: tuple[float, float],
) -> Iterator[tuple[np.ndarray, tuple[int, int]]]:
    """
    Split image into N patches for processing.

    :param image: 2D image array (np.ndarray)
    :param image_patch_dim: Dimension of the image patches (tuple[int, int])
    :param split_image_threshold:
        At which scale relative to the image_patch_dim should images be split (tuple[float, float]).
        For (1.5, 1.5) images are split if their height and width are 1.5X larger than `image_patch_dim`.

    :returns:
        Iterator over image patches as numpy arrays.
    """

    image_height, image_width = image.shape
    target_image_height, target_image_width = image_patch_dim
    scale = (
        image_height / target_image_height,
        image_width / target_image_width,
    )
    if scale <= split_image_threshold:
        yield image, (0, 0)
    else:
        notifications.show_info("Processing image in batches...")
        for i, j in itertools.product(
            range(0, image_height, target_image_height),
            range(0, image_width, target_image_width),
        ):
            yield image[
                i : i + target_image_height, j : j + target_image_width
            ], (i, j)


def count_objects(
    image: np.ndarray,
    roi_offset: tuple[int, int],
    model_type: str,
    cellprob_threshold: float,
    flow_threshold: float,
    use_gpu: bool,
    batch_size: int,
    diameter: float,
):
    """
    Count objects in an image, or selected ROIs is available.

    :param image: Image data  (np.ndarray).
    :param roi_offset: Offset or ROI relative to original image (tuple[int, int]).
    :param model_type: Segmentation model type (str).
    :param cellprob_threshold: Cell probability threshold (float).
    :param flow_threshold: Flow threshold (float).
    :param use_gpu: Whether to use GPU acceleration (bool).
    :param batch_size: Batch size for model inference (int).
    :param diameter: Object diameter (float).

    :returns:
        tuple containing segmentation masks (napari.layers.Labels), mask offset.
    """

    from cellpose import models

    model = models.Cellpose(model_type=model_type, gpu=use_gpu)

    @find_executable_batch_size(starting_batch_size=batch_size)
    def compute_masks(batch_size, model=None):

        masks, _, _, _ = model.eval(
            image,
            channels=[0, 0],
            cellprob_threshold=cellprob_threshold,
            flow_threshold=flow_threshold,
            diameter=diameter,
            batch_size=batch_size,
        )

        return masks

    masks = compute_masks(model=model)
    del model

    return masks, roi_offset
