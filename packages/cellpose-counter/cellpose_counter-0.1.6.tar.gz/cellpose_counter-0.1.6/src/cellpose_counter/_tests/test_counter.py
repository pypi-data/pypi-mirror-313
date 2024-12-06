import numpy as np
from skimage import io

from cellpose_counter.counter import (
    estimate_diameter,
    get_image_patches,
    get_image_roi,
    restore_image,
)

SMALL_IMAGE_PATH = "src/cellpose_counter/_tests/data/image_small_512.tif"
LARGE_IMAGE_PATH = "src/cellpose_counter/_tests/data/image_large_1024.tif"

SMALL_IMAGE = io.imread(SMALL_IMAGE_PATH, as_gray=True)
LARGE_IMAGE = io.imread(LARGE_IMAGE_PATH, as_gray=True)

SMALL_ROI_LAYER = [
    np.array([[0.0, 256.0], [0.0, 512.0], [256.0, 512.0], [256.0, 256.0]])
]
LARGE_ROI_LAYER = [
    np.array([[0.0, 0.0], [0.0, 1024.0], [1024.0, 1024.0], [1024.0, 0.0]])
]

# Targets
SMALL_IMAGE_DIAMETER = np.float64(7.0)
SMALL_ROI_SHAPE = (
    (SMALL_ROI_LAYER[0][1][1] - SMALL_ROI_LAYER[0][0][1]).astype(int),
    (SMALL_ROI_LAYER[0][2][1] - SMALL_ROI_LAYER[0][3][1]).astype(int),
)


def test_roi_extraction():
    roi, _ = get_image_roi(SMALL_IMAGE, SMALL_ROI_LAYER[0])
    assert roi.shape == SMALL_ROI_SHAPE


def test_estimate_diameter():
    model_type = "nuclei"
    use_gpu = False  # for testing
    diam = estimate_diameter(SMALL_IMAGE, model_type, use_gpu)
    assert diam == SMALL_IMAGE_DIAMETER


def test_image_restoration():
    restore_type = "nuclei_oneclick"
    use_gpu = False
    diameter = 6.48
    batch_size = 8

    restored_images = restore_image(
        SMALL_IMAGE,
        "small_image_512",
        restore_type,
        diameter,
        use_gpu,
        batch_size,
    )

    assert restored_images.data.shape == (512, 512)


def test_image_split() -> None:
    """
    Test batch processing is enabled for larger images
    """
    target_dim = (512, 512)
    split_image_scale_threshold = (1.5, 1.5)

    small_batch = get_image_patches(
        SMALL_IMAGE, target_dim, split_image_scale_threshold
    )
    n_rows_small = np.ceil(SMALL_IMAGE.shape[0] / target_dim[0])
    n_cols_small = np.ceil(SMALL_IMAGE.shape[1] / target_dim[1])
    n_small_image_patches = n_rows_small * n_cols_small

    large_batch = get_image_patches(
        LARGE_IMAGE, target_dim, split_image_scale_threshold
    )
    n_rows_large = np.ceil(LARGE_IMAGE.shape[0] / target_dim[0])
    n_cols_large = np.ceil(LARGE_IMAGE.shape[1] / target_dim[1])
    n_large_image_patches = n_rows_large * n_cols_large

    assert len(list(small_batch)) == n_small_image_patches
    assert len(list(large_batch)) == n_large_image_patches
