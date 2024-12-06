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


def _post_processing(
    output_buffer: np.ndarray,  # BxCxHxW
    output_image: np.ndarray,  # BxHxWxC
) -> None:

    b, h, w, c = output_image.shape
    pred = np.clip(np.multiply(output_buffer[:b, :, :h, :w], 255), 0, 255).astype(
        np.uint8
    )
    for i in range(3):
        np.copyto(src=pred[:, i, :, :], dst=output_image[:, :, :, i])


@register
class DRURBPNDEINTERF3GLOSSProcessor(NVIDIAProcessorBase[EngineIOData, EngineIOData]):

    def __init__(
        self,
        concurrency: int,
        index: int,
        model_path: str,
        device: Union[Literal["auto"], int] = "auto",
    ):
        # super
        super().__init__(
            concurrency=concurrency,
            index=index,
            model_path=model_path,
            device=device,
        )

        self.config = DRURBPNDEINTERF3GLOSSConfig

    async def inference(self, batch_input_data: List[np.ndarray]) -> List[np.ndarray]:
        session = self.session
        patch_size = self.config.PATCH_SIZE
        batch = len(batch_input_data)

        batch_output_data: np.ndarray = np.zeros(
            (
                batch,
                self.config.PATCHER_CONFIG.patch_size * self.config.UPSCALE_RATIO,
                self.config.PATCHER_CONFIG.patch_size * self.config.UPSCALE_RATIO,
                self.config.NUMBER_OF_OUTPUT_CHANNELS,
            ),
            np.uint8,
        )
        _pre_processing(
            batch_input_images=batch_input_data,
            input_buffer=self.input_buffer,
        )
        session.run()
        _post_processing(
            output_buffer=self.output_buffer,
            output_image=batch_output_data,
        )
        return [output_data for output_data in batch_output_data]  # unpack

    async def _run(self, input_data: EngineIOData) -> EngineIOData:
        max_batch_size = self.io_shapes["input"][0][0]
        # 여기서 patching
        input_image: np.ndarray = input_data.frame  # type: ignore
        patcher_config = self.config.PATCHER_CONFIG
        padded_input_image = patcher.pad_vector(
            vector=input_image,
            overlap_length=patcher_config.input_overlab_length,
        )
        output_image: np.ndarray = np.zeros(
            (
                input_image.shape[0] * self.config.UPSCALE_RATIO,
                input_image.shape[1] * self.config.UPSCALE_RATIO,
                self.config.NUMBER_OF_OUTPUT_CHANNELS,
            ),
            np.uint8,
        )

        # slice
        input_patches = self.patcher.slice(input_vector=padded_input_image)

        # batch inference
        output_patches = []
        for batch_items in TRT.batch(input_patches, max_batch_size):
            ops = await self.inference(batch_input_data=batch_items)
            output_patches += ops

        self.patcher.merge(output_vector=output_image, patches=output_patches)
        return EngineIOData(frame_id=input_data.frame_id, frame=output_image)

    def _ready_processor(self) -> bool:
        return True

    def _bind_io(self, input_data: EngineIOData):
        model_path = self.model_path
        device_id = self.device_id
        patcher_config = self.config.PATCHER_CONFIG
        trt_config = self.config.TRT_CONFIG

        input_image: np.ndarray = input_data.frame  # type: ignore
        padded_input_image = patcher.pad_vector(
            input_image,
            overlap_length=patcher_config.input_overlab_length,
        )
        output_image: np.ndarray = np.zeros(
            (
                input_image.shape[0] * self.config.UPSCALE_RATIO,
                input_image.shape[1] * self.config.UPSCALE_RATIO,
                self.config.NUMBER_OF_OUTPUT_CHANNELS,
            )
        )
        self.patcher = patcher.Patcher(
            **patcher_config.build_patcher_params(
                input_vector=padded_input_image,
                output_vector=output_image,
            )
        )
        n_patches = len(self.patcher.slice(input_vector=padded_input_image))

        # set io shape
        self.batch_size = min(n_patches, self.config.MAX_BATCH_SIZE)
        self.io_shapes = {
            "input": (
                [self.batch_size, *trt_config.input_shape],
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
        self.output_buffer = self.session._output_bindings[0].host_buffer.reshape(
            *self.io_shapes["output"][0]
        )

        return True

    def _get_live(self) -> bool:
        return True

    def _get_concurrency(self) -> int:
        return self._concurrency
