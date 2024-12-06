from datetime import datetime
from ._dependency import *
from ._const import *
from . import patcher
from ._nvidia_processor_base import NVIDIAProcessorBase


def _pre_processing(
    batch_input_images: List[np.ndarray],
    input_buffer: np.ndarray,
) -> None:
    b = len(batch_input_images)
    for batch_idx in range(b):
        image = batch_input_images[batch_idx]
        h, w, c = image.shape
        for channel_idx in range(c):
            np.divide(
                image[:, :, channel_idx],
                255,
                out=input_buffer[batch_idx, channel_idx, :h, :w],
            )


def _post_processing_patch(
    output_buffer: np.ndarray,  # BxCxHxW
    output_image: np.ndarray,  # BxHxWxC
) -> None:
    b, h, w, c = output_image.shape
    pred = output_buffer[:b, :, :h, :w]
    for i in range(3):
        np.copyto(src=pred[:, i, :, :], dst=output_image[:, :, :, i])


def _post_processing_merged(
    output_image: np.ndarray,
    scale_min: np.ndarray,
    scale_max: np.ndarray,
) -> np.ndarray:
    output_image = (output_image - scale_min) / (scale_max - scale_min)
    return np.clip(np.multiply(output_image, 255), 0, 255).astype(np.uint8)


def _get_scale_factor(output_image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    def _rgb2grayscale(rgb: np.ndarray):
        return (
            0.299 * rgb[..., :, :, 0:1]
            + 0.587 * rgb[..., :, :, 1:2]
            + 0.114 * rgb[..., :, :, 2:3]
        )

    scale_max = (
        np.amax(
            _rgb2grayscale(output_image),
            # axis=(-3, -2, -1),
            axis=(-2, -1, -3),
            keepdims=True,
        )
        + 0.0015
    )
    scale_min = (
        np.amin(
            _rgb2grayscale(output_image),
            # axis=(-3, -2, -1),
            axis=(-2, -1, -3),
            keepdims=True,
        )
        - 0.0015
    )
    return scale_min, scale_max


@register
class COLORRESNETPOSTProcessor(NVIDIAProcessorBase[EngineIOData, EngineIOData]):

    def __init__(
        self,
        concurrency: int,
        index: int,
        model_path: str,
        filter_coefficient: np.ndarray,
        device: Union[Literal["auto"], int] = "auto",
    ):
        # super
        super().__init__(
            concurrency=concurrency,
            index=index,
            model_path=model_path,
            device=device,
        )
        self.filter_coefficient = filter_coefficient
        self.config = ColorResnetPostConfig
        self.is_scale_factor_calculated = False
        assert True

    async def inference(self, batch_input_data: List[np.ndarray]) -> List[np.ndarray]:
        session = self.session
        patch_size = self.config.PATCH_SIZE
        # batch_input_data = [np.zeros_like(batch_input_data[0]), *batch_input_data]
        batch = len(batch_input_data)
        batch_output_data: np.ndarray = np.zeros(
            (batch, patch_size, patch_size, 3), np.float32
        )
        _pre_processing(
            batch_input_images=batch_input_data,
            input_buffer=self.input_buffer,
        )
        session.run()
        _post_processing_patch(
            output_buffer=self.output_buffer,
            output_image=batch_output_data,
        )
        # return [output_data for output_data in batch_output_data[1:]]  # unpack
        return [output_data for output_data in batch_output_data]  # unpack

    async def _run(self, input_data: EngineIOData) -> EngineIOData:
        # max_batch_size = self.io_shapes["input"][0][0] - 1
        max_batch_size = 1
        # 여기서 patching
        input_image: np.ndarray = input_data.frame  # type: ignore
        patcher_config = self.config.PATCHER_CONFIG
        padded_input_image = patcher.pad_vector(
            vector=input_image,
            overlap_length=patcher_config.input_overlab_length,
        )
        output_image: np.ndarray = np.zeros(input_image.shape, np.float32)

        # slice
        input_patches = self.patcher.slice(input_vector=padded_input_image)

        # batch inference
        output_patches = []
        for batch_items in TRT.batch(input_patches, max_batch_size):
            ops = await self.inference(batch_input_data=batch_items)
            output_patches += ops
        self.patcher.merge(output_vector=output_image, patches=output_patches)
        if not self.is_scale_factor_calculated:
            self.scale_min, self.scale_max = _get_scale_factor(output_image)
            self.is_scale_factor_calculated = True
        output_image = _post_processing_merged(
            output_image=output_image,
            scale_min=self.scale_min,
            scale_max=self.scale_max,
        )
        return EngineIOData(frame_id=input_data.frame_id, frame=output_image)

    def _ready_processor(self) -> bool:
        return True

    def _bind_io(self, input_data: EngineIOData):
        patcher_config = self.config.PATCHER_CONFIG
        trt_config = self.config.TRT_CONFIG

        input_image: np.ndarray = input_data.frame  # type: ignore
        padded_input_image = patcher.pad_vector(
            input_image,
            overlap_length=patcher_config.input_overlab_length,
        )
        output_image: np.ndarray = np.zeros(input_image.shape, np.float32)
        self.patcher = patcher.Patcher(
            **patcher_config.build_patcher_params(
                input_vector=padded_input_image,
                output_vector=output_image,
            )
        )
        n_patches = len(self.patcher.slice(input_vector=padded_input_image))

        # set io shape
        # self.batch_size = min(n_patches + 1, self.config.MAX_BATCH_SIZE - 1)
        self.batch_size = self.config.MAX_BATCH_SIZE
        self.io_shapes = {
            "input": (
                [self.batch_size, *trt_config.input_shape],
                np.float32,
            ),
            "model_output": (
                [1, *self.config.TRT_SHAPE_MODEL_OUTPUT],
                np.float32,
            ),
            "output": (
                [self.batch_size, *trt_config.output_shape],
                np.float32,
            ),
        }

        # init trt engine
        self.initialize_trt_session(
            required_batch_size=self.batch_size,
            io_shape=self.io_shapes,
        )

        # set io buffer
        self.input_buffer = self.session._input_bindings[0].host_buffer.reshape(
            self.io_shapes["input"][0]
        )
        self.filter_coefficient_buffer = self.session._input_bindings[
            1
        ].host_buffer.reshape(self.io_shapes["model_output"][0])
        self.output_buffer = self.session._output_bindings[0].host_buffer.reshape(
            self.io_shapes["output"][0]
        )
        self.filter_coefficient_buffer[:] = self.filter_coefficient[:]
        self.session.run()
        return True

    def _get_live(self) -> bool:
        return True

    def _get_concurrency(self) -> int:
        return self._concurrency
