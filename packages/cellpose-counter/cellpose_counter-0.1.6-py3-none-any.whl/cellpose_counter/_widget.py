from typing import TYPE_CHECKING

from magicgui.widgets import (
    CheckBox,
    Combobox,
    Container,
    FloatSlider,
    LineEdit,
    PushButton,
    create_widget,
)
from napari.layers import Image
from napari.qt.threading import create_worker
from napari.utils import notifications

if TYPE_CHECKING:
    import napari
    import numpy as np


CP_MODELS = [
    "nuclei",
    "cyto3",
    "cyto2",
    "cyto",
    "tissuenet_cp3",
    "livecell_cp3",
]
RESTORE_MODELS = [
    "denoise_nuclei",
    "deblur_nuclei",
    "upsample_nuclei",
    "oneclick_nuclei",
    "denoise_cyto3",
    "deblur_cyto3",
    "upsample_cyto3",
    "oneclick_cyto3",
    "denoise_cyto2",
    "deblur_cyto2",
    "upsample_cyto2",
    "oneclick_cyto2",
    "None",
]


class Counter(Container):
    """
    Counter widget for Napari

    count cells and nuclei from images using cellpose models.
    """

    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self._viewer = viewer

        # make scale bar visible
        self._viewer.scale_bar.visible = True
        self._viewer.scale_bar.unit = "px"

        # create widgets
        self._image_layer_combo = create_widget(
            label="Input Image", annotation="napari.layers.Image"
        )
        self._roi_layer_combo = create_widget(
            label="ROI",
            annotation="napari.layers.Shapes",
            options={"nullable": True},
        )
        self._create_roi_btn = PushButton(text="Create ROI")
        self._use_gpu = CheckBox(text="Use GPU", value=True)
        self._batch_size = LineEdit(label="Initial Batch Size", value="64")

        # image restoration
        self._restore_models = Combobox(
            label="Restore Model",
            value="oneclick_nuclei",
            choices=RESTORE_MODELS,
        )
        self._restore_image_btn = PushButton(label="Restore image")

        # diameter estimation
        self._diam = LineEdit(label="Diameter", value="17")
        self._diam_estimate_btn = PushButton(label="Estimate Diameter")

        # segmentation
        self._cp_models = Combobox(
            label="Cellpose Model", value="nuclei", choices=CP_MODELS
        )
        self._cellprob_threshold = FloatSlider(
            label="Probability Threshold", value=0, min=-8.0, max=8.0, step=0.2
        )
        self._flow_threshold = FloatSlider(
            label="Flow Threshold", value=0.4, min=0.0, max=3.0, step=0.05
        )
        self._get_count_btn = PushButton(text="Get Automated Count")
        self._auto_count_display = LineEdit(label="Auto Count", value="0")
        self._manual_count_display = LineEdit(label="Manual Count", value="0")
        self._total_count_display = LineEdit(label="Total Count", value="0")

        # manual count adjustments
        self._auto_count_layer = create_widget(
            label="Auto Counts", annotation="napari.layers.Labels"
        )
        self._manual_count_layer = create_widget(
            label="Manual Counts", annotation="napari.layers.Points"
        )
        self._sync_count_btn = PushButton(text="Sync Auto+Manual Counts")

        # callbacks
        self._create_roi_btn.changed.connect(self._create_roi_layer)
        self._diam_estimate_btn.changed.connect(self._estimate_diam)
        self._restore_image_btn.changed.connect(self._restore_image)
        self._get_count_btn.changed.connect(self._get_count)
        self._sync_count_btn.changed.connect(self._update_count)

        # append into/extend the container with widgets
        self.extend(
            [
                self._image_layer_combo,
                self._roi_layer_combo,
                self._create_roi_btn,
                self._use_gpu,
                self._batch_size,
                self._restore_models,
                self._restore_image_btn,
                self._diam,
                self._diam_estimate_btn,
                self._cp_models,
                self._cellprob_threshold,
                self._flow_threshold,
                self._get_count_btn,
                self._auto_count_display,
                self._manual_count_display,
                self._total_count_display,
                self._auto_count_layer,
                self._manual_count_layer,
                self._sync_count_btn,
            ]
        )

    def _create_roi_layer(self):
        """Create custom Shape layer for selecting ROI in image."""

        # get first image layer
        image_layer = next(
            (
                layer
                for layer in self._viewer.layers
                if isinstance(layer, Image)
            ),
            None,
        )
        # we need to match the dimensions of the image layer
        # ...or else bad stuff happens
        ndim = 2 if image_layer is None else image_layer.ndim

        roi_layer = self._viewer.add_shapes(
            ndim=ndim,
            name="ROI",
            shape_type="rectangle",
            edge_width=2,
            edge_color="red",
            face_color="white",
            opacity=0.2,
            blending="additive",
        )
        roi_layer.mode = "add_rectangle"
        self._roi_layer_combo.value = self._viewer.layers[-1]

    def _prepare_job(
        self, job_name: str
    ) -> tuple["np.ndarray", tuple[int, int]]:
        """
        Prepare image for processing

        :param job_name: String to display as a notification when job is starting

        :return:
            Tuple containing prepared image (np.ndarray) and ROI offset relative to original image (tuple[int, int])
        """
        notifications.show_info(job_name)
        image_layer = self._image_layer_combo.value
        if image_layer is None:
            raise ValueError("No image selected.")

        from .counter import prepare_image

        checked_image = prepare_image(
            image_layer.data
        )  # can raise value error

        roi_layer = self._roi_layer_combo.value
        if roi_layer is None or len(roi_layer.data) == 0:
            image = checked_image
            offset = (0, 0)
        else:
            from .counter import get_image_roi

            if len(roi_layer.data) > 1:
                notifications.show_warning(
                    "Only 1 ROI per Shape layer is allowed. Defaulting to 1st ROI."
                )
            image, offset = get_image_roi(checked_image, roi_layer.data[0])

        return image, offset

    def _estimate_diam(self):
        """
        Estimate diameter of objects with Cellpose size models.

        Will use the entire image if no ROI selection is made. Otherwise, will use the first drawn ROI.
        """

        try:
            image, offset = self._prepare_job("Calculating diameter...")
        except ValueError as e:
            notifications.show_error(str(e))
            return

        from .counter import estimate_diameter

        estimate_diam_worker = create_worker(
            estimate_diameter,
            image,
            self._cp_models.value,
            self._use_gpu.value,
            _progress=True,
        )
        estimate_diam_worker.returned.connect(self._display_diam)
        estimate_diam_worker.start()

    def _restore_image(self):
        image, offset = self._prepare_job("Restoring image...")

        from .counter import restore_image

        restore_image_worker = create_worker(
            restore_image,
            image,
            self._image_layer_combo.value.name,
            self._restore_models.value,
            float(self._diam.value),
            self._use_gpu.value,
            int(self._batch_size.value),
            _progress=True,
        )
        restore_image_worker.returned.connect(self._display_restored_image)
        restore_image_worker.start()

    def _get_count(self):
        """Count cells/nuclei inside an ROI for a given image using cellpose"""
        image, offset = self._prepare_job("Counting objects...")

        from .counter import count_objects

        count_objects_worker = create_worker(
            count_objects,
            image,
            offset,
            self._cp_models.value,
            self._cellprob_threshold.value,  # cellprob and flow thresholds are
            self._flow_threshold.value,  # already floats. No need to convert.
            self._use_gpu.value,
            int(self._batch_size.value),
            float(self._diam.value),
            _progress=True,
        )
        count_objects_worker.returned.connect(self._display_count)
        count_objects_worker.start()

    def _update_count(self):
        """Update total number of cells from automatic and manual counting"""
        count = 0
        manual_layer = self._manual_count_layer.value
        auto_layer = self._auto_count_layer.value

        if manual_layer is not None:
            manual_count = len(manual_layer.data)
            count += manual_count
            self._manual_count_display.value = manual_count

        if auto_layer is not None:
            auto_count = auto_layer.data.max()
            count += auto_count
            self._auto_count_display.value = auto_count

        self._total_count_display.value = count
        notifications.show_info("Total count updated successfully.")

    def _display_diam(self, diam: float):
        """Purely for updating the diameter value"""
        self._diam.value = diam
        notifications.show_info("Successfully calculated diameter.")

    def _display_restored_image(self, image: "napari.layers.Image"):
        """Display restored image in the viewer"""
        self._viewer.add_layer(image)
        notifications.show_info("Successfully restored image.")

    def _display_count(self, result: tuple["np.ndarray", tuple[int, int]]):
        """Display count and add segmentation results"""
        masks, mask_offsets = result
        count = masks.max()
        self._total_count_display.value = count
        self._manual_count_display.value = 0
        self._auto_count_display.value = count

        self._viewer.add_labels(masks, translate=mask_offsets, name="Masks")
        manual_count_layer = self._viewer.add_points(
            name="Manual", size=float(self._diam.value)
        )
        manual_count_layer.mode = "add"
        self._manual_count_layer.value = self._viewer.layers[-1]
        self._auto_count_layer.value = self._viewer.layers[-2]
        notifications.show_info("Updated total count.")
