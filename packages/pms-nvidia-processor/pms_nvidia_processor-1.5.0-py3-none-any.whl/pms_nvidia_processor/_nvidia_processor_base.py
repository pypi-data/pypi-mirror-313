from ._dependency import *
from ._const import *
from . import patcher


class NVIDIAProcessorBase(IEngineProcessor[InputTypeT, OutputTypeT], metaclass=ABCMeta):

    def __init__(
        self,
        index: int,
        concurrency: int,
        model_path: str,
        device: Union[Literal["auto"], int] = "auto",
    ):
        # set member var
        self.index = index
        self.model_path = model_path
        self._concurrency = concurrency
        self._session = None
        self.logger = logger
        # set loop policy
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        # set device_id
        device_count = TRT.get_device_count()
        if device is "auto":
            if "CUDA_VISIBLE_DEVICES" in os.environ:
                devices = [
                    int(s) for s in os.environ["CUDA_VISIBLE_DEVICES"].split(",")
                ]
                assert len(devices) > 0, f"ERROR, CUDA_VISIBLE_DEVICES is empty."
                device_id = devices[index % len(devices)]
            else:
                device_id = index % device_count
        else:
            assert type(device) is int, f"ERROR, The device's type is NOT int."
            assert device > -1, f"ERROR, The device must be 'x > -1' but {device}."
            device_id = device
        self.device_id = device_id

        # super
        super().__init__(
            concurrency=concurrency,
            index=index,
        )

    def initialize_trt_session(
        self,
        required_batch_size: int,
        io_shape: Dict[str, Tuple[List[int], np.dtype]],
    ):
        model_path = self.model_path
        device_id = self.device_id

        # set io shape
        self.batch_size = required_batch_size
        self.io_shapes = io_shape

        # init trt engine
        self._session = TRT.TRTSession(
            model_path=model_path,
            device_id=device_id,
            io_shapes=self.io_shapes,
        )

        # warm up
        self.session.run()

    @property
    def session(self) -> TRT.TRTSession:
        assert (
            self._session
        ), "ERROR!, session is NOT initialized. Please call 'initialize_trt_session'"
        return self._session
