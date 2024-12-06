from pms_nvidia_processor._const import *
from pms_nvidia_processor.patcher._patch_collection import PatchPosXYCollection


def pad_vector(
    vector: np.ndarray,
    overlap_length: int,
    mode: Literal[
        "edge",
        "mean",
        "median",
        "reflect",
        "symmetric",
    ] = "edge",
) -> np.ndarray:
    # create padding image
    padded_vector = np.pad(
        vector,
        pad_width=(
            (overlap_length, overlap_length),
            (overlap_length, overlap_length),
            (0, 0),
        ),
        mode=mode,
    )
    return padded_vector


class Patcher:

    def __init__(
        self,
        input_vector_shape: Tuple[int, int, int],
        input_patch_shape: Tuple[int, int, int],
        input_overlap_length: int,
        output_vector_shape: Tuple[int, int, int],
        output_patch_shape: Tuple[int, int, int],
        output_overlap_length: int,
    ) -> None:
        assert input_overlap_length > -1, "assert input_overlap_length > -1"
        assert output_overlap_length > -1, "assert output_overlap_length > -1"
        assert all(
            [e > 0 for e in input_patch_shape]
        ), "assert all([e > 0 for e in input_patch_shape])"
        assert all(
            [e > 0 for e in output_patch_shape]
        ), "assert all([e > 0 for e in output_patch_shape])"
        assert (
            len(input_patch_shape) == 3
        ), "assert len(input_patch_shape) == 3"  # only allow image-like vector
        assert (
            len(output_patch_shape) == 3
        ), "assert len(output_patch_shape) == 3"  # only allow image-like vector

        input_pos_collection = PatchPosXYCollection.create(
            vector_shape=input_vector_shape,
            patch_shape=input_patch_shape,
            overlap_length=input_overlap_length,
        )
        output_pos_collection = PatchPosXYCollection.create(
            vector_shape=output_vector_shape,
            patch_shape=output_patch_shape,
            overlap_length=0,
        )
        assert (
            input_pos_collection.shape == output_pos_collection.shape
        ), f"assert input_pos_collection.shape == output_pos_collection.shape | {input_pos_collection.shape} != {output_pos_collection.shape}"
        self._input_pos_collection = input_pos_collection
        self._output_pos_collection = output_pos_collection
        self._input_overlap_length = input_overlap_length
        self._output_overlap_length = output_overlap_length

    def slice(self, input_vector: np.ndarray):  # -> List[ndarray[Any, Any]]:
        return self._input_pos_collection.get_patch(input_vector)

    def merge(self, output_vector: np.ndarray, patches: List[np.ndarray]):
        self._output_pos_collection.set_patch(
            vector=output_vector,
            patches=patches,
            overlab_length=self._output_overlap_length,
        )
