from ._dependency import *


@dataclass
class PatcherIOConfig:
    patch_size: int
    upscale_ratio: int
    number_of_input_channels: int
    number_of_output_channels: int
    input_overlab_length: int

    @property
    def output_overlab_length(self) -> int:
        return self.input_overlab_length * self.upscale_ratio

    @property
    def input_shape(self) -> Tuple[int, int, int]:
        return (
            self.patch_size,
            self.patch_size,
            self.number_of_input_channels,
        )

    @property
    def output_shape(self) -> Tuple[int, int, int]:
        output_patch_size = (
            self.patch_size - self.input_overlab_length * 2
        ) * self.upscale_ratio
        return (
            output_patch_size,
            output_patch_size,
            self.number_of_output_channels,
        )

    def build_patcher_params(
        self,
        input_vector: np.ndarray,
        output_vector: np.ndarray,
    ) -> Dict[str, Any]:
        input_vector_shape = input_vector.shape
        output_vector_shape = output_vector.shape
        return {
            "input_vector_shape": input_vector_shape,  # type: ignore
            "input_patch_shape": self.input_shape,
            "input_overlap_length": self.input_overlab_length,
            "output_vector_shape": output_vector_shape,  # type: ignore
            "output_patch_shape": self.output_shape,
            "output_overlap_length": self.output_overlab_length,
        }


@dataclass
class TRTIOConfig:
    patch_size: int
    upscale_ratio: int
    number_of_input_channels: int
    number_of_output_channels: int

    @property
    def input_shape(self) -> Tuple[int, int, int]:
        return (self.number_of_input_channels, self.patch_size, self.patch_size)

    @property
    def output_shape(self) -> Tuple[int, int, int]:
        return (
            self.number_of_output_channels,
            self.patch_size * self.upscale_ratio,
            self.patch_size * self.upscale_ratio,
        )


class DPIRConfig:
    NUMBER_OF_INPUT_CHANNELS: int = 4
    NUMBER_OF_OUTPUT_CHANNELS: int = 3
    UPSCALE_RATIO: int = 1
    PATCH_SIZE = 256
    MAX_BATCH_SIZE = 8
    MIN_BATCH_SIZE = 1
    OPT_BATCH_SIZE = MAX_BATCH_SIZE // 2
    INPUT_OVERLAB_LENGTH = 5

    PATCHER_CONFIG = PatcherIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
        input_overlab_length=INPUT_OVERLAB_LENGTH,
    )
    TRT_CONFIG = TRTIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
    )


class DRURBPNSRF3Config:
    NUMBER_OF_FRAMES = 3
    NUMBER_OF_INPUT_CHANNELS: int = 3 * NUMBER_OF_FRAMES
    NUMBER_OF_OUTPUT_CHANNELS: int = 3
    UPSCALE_RATIO: int = 2
    PATCH_SIZE = 512
    MAX_BATCH_SIZE = 8
    MIN_BATCH_SIZE = 1
    OPT_BATCH_SIZE = MAX_BATCH_SIZE // 2
    INPUT_OVERLAB_LENGTH = 32

    PATCHER_CONFIG = PatcherIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
        input_overlab_length=INPUT_OVERLAB_LENGTH,
    )
    TRT_CONFIG = TRTIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
    )


class DRURBPNSRF5Config:
    NUMBER_OF_FRAMES = 5
    NUMBER_OF_INPUT_CHANNELS: int = 3 * NUMBER_OF_FRAMES
    NUMBER_OF_OUTPUT_CHANNELS: int = 3
    UPSCALE_RATIO: int = 2
    PATCH_SIZE = 512
    MAX_BATCH_SIZE = 8
    MIN_BATCH_SIZE = 1
    OPT_BATCH_SIZE = MAX_BATCH_SIZE // 2
    INPUT_OVERLAB_LENGTH = 32

    PATCHER_CONFIG = PatcherIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
        input_overlab_length=INPUT_OVERLAB_LENGTH,
    )
    TRT_CONFIG = TRTIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
    )


class DRUASMSRF3Config:
    NUMBER_OF_FRAMES = 3
    NUMBER_OF_INPUT_CHANNELS: int = 3 * NUMBER_OF_FRAMES
    NUMBER_OF_OUTPUT_CHANNELS: int = 3
    UPSCALE_RATIO: int = 2
    PATCH_SIZE = 512
    MAX_BATCH_SIZE = 8
    MIN_BATCH_SIZE = 1
    OPT_BATCH_SIZE = MAX_BATCH_SIZE // 2
    INPUT_OVERLAB_LENGTH = 16

    PATCHER_CONFIG = PatcherIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
        input_overlab_length=INPUT_OVERLAB_LENGTH,
    )
    TRT_CONFIG = TRTIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS + 1,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
    )


class DRURBPNDEINTERF3GLOSSConfig:
    NUMBER_OF_FRAMES = 3
    NUMBER_OF_INPUT_CHANNELS: int = 3 * NUMBER_OF_FRAMES
    NUMBER_OF_OUTPUT_CHANNELS: int = 3
    UPSCALE_RATIO: int = 1
    PATCH_SIZE = 512
    MAX_BATCH_SIZE = 8
    MIN_BATCH_SIZE = 1
    OPT_BATCH_SIZE = MAX_BATCH_SIZE // 2
    INPUT_OVERLAB_LENGTH = 16

    PATCHER_CONFIG = PatcherIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
        input_overlab_length=INPUT_OVERLAB_LENGTH,
    )
    TRT_CONFIG = TRTIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
    )


class FISFConfig:
    NUMBER_OF_FRAMES = 1
    NUMBER_OF_INPUT_CHANNELS: int = 3 * NUMBER_OF_FRAMES
    NUMBER_OF_OUTPUT_CHANNELS: int = 3
    UPSCALE_RATIO: int = 1
    PATCH_SIZE = 512
    MAX_BATCH_SIZE = 8
    MIN_BATCH_SIZE = 1
    OPT_BATCH_SIZE = MAX_BATCH_SIZE // 2
    INPUT_OVERLAB_LENGTH = 16

    PATCHER_CONFIG = PatcherIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
        input_overlab_length=INPUT_OVERLAB_LENGTH,
    )
    TRT_CONFIG = TRTIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
    )


class ColorResnetPreConfig:
    NUMBER_OF_INPUT_CHANNELS: int = 3
    NUMBER_OF_OUTPUT_CHANNELS: int = 30
    UPSCALE_RATIO: int = 1
    PATCH_SIZE = 256
    MAX_BATCH_SIZE = 1
    MIN_BATCH_SIZE = 1
    OPT_BATCH_SIZE = 1

    TRT_SHAPE_INPUT = (NUMBER_OF_INPUT_CHANNELS, PATCH_SIZE, PATCH_SIZE)
    TRT_SHAPE_OUTPUT = (NUMBER_OF_OUTPUT_CHANNELS,)


class ColorResnetPostConfig:
    NUMBER_OF_FRAMES = 1
    NUMBER_OF_INPUT_CHANNELS: int = 3 * NUMBER_OF_FRAMES
    NUMBER_OF_MODEL_OUTPUT_CHANNELS: int = 30
    NUMBER_OF_OUTPUT_CHANNELS: int = 3
    UPSCALE_RATIO: int = 1
    PATCH_SIZE = 512
    # MAX_BATCH_SIZE = 8
    MAX_BATCH_SIZE = 1
    MIN_BATCH_SIZE = 1
    OPT_BATCH_SIZE = MAX_BATCH_SIZE // 2
    INPUT_OVERLAB_LENGTH = 16 * 2

    PATCHER_CONFIG = PatcherIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
        input_overlab_length=INPUT_OVERLAB_LENGTH,
    )
    TRT_CONFIG = TRTIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
    )
    TRT_SHAPE_MODEL_OUTPUT = (NUMBER_OF_MODEL_OUTPUT_CHANNELS,)


class GGConfig:
    NUMBER_OF_INPUT_CHANNELS: int = 4
    NUMBER_OF_OUTPUT_CHANNELS: int = 3
    UPSCALE_RATIO: int = 1
    PATCH_SIZE = 512
    MAX_BATCH_SIZE = 8
    MIN_BATCH_SIZE = 1
    OPT_BATCH_SIZE = MAX_BATCH_SIZE // 2
    INPUT_OVERLAB_LENGTH = 5

    PATCHER_CONFIG = PatcherIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
        input_overlab_length=INPUT_OVERLAB_LENGTH,
    )
    TRT_CONFIG = TRTIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
    )
