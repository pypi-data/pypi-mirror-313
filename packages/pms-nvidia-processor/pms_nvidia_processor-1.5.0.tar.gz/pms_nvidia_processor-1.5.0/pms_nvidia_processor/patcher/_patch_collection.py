from pms_nvidia_processor._const import *
from pms_nvidia_processor.patcher._patch_position import (
    PatchPositionXY,
    PatchPosition,
)


class PatchPosXYCollection:
    def __init__(self, patch_pos_list: List[List[PatchPositionXY]]):
        self.patch_pos_list = patch_pos_list

    def __iter__(self):
        for poses in self.__patch_pos_list:
            for pos in poses:
                yield pos

    def __len__(self):
        return self.__size

    def __getitem__(self, idx):
        y = idx // self.__cols
        x = idx % self.__cols
        return self.__patch_pos_list[y][x]

    def get_patch(
        self,
        vector: np.ndarray,
    ) -> List[np.ndarray]:
        return [vector[pos.y.range, pos.x.range] for pos in self]

    def set_patch(
        self,
        vector: np.ndarray,
        patches: List[np.ndarray],
        overlab_length: int,
    ):
        for pos, patch in zip(self, patches, strict=True):  # inplace copy
            h, w, c = patch.shape
            vector[pos.y.range, pos.x.range] = patch[
                overlab_length : overlab_length + pos.y.dp,
                overlab_length : overlab_length + pos.x.dp,
            ]

    @property
    def patch_pos_list(self) -> List[List[PatchPositionXY]]:
        return self.__patch_pos_list

    @patch_pos_list.setter
    def patch_pos_list(self, patch_pos_list: List[List[PatchPositionXY]]):
        self.__rows = len(patch_pos_list)
        self.__cols = len(patch_pos_list[0])
        assert all([len(c) == self.__cols for c in patch_pos_list])
        self.__size = self.__rows * self.__cols
        self.__patch_pos_list = patch_pos_list

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols

    @property
    def size(self):
        return self.__size

    @property
    def shape(self):
        return (self.rows, self.cols)

    @staticmethod
    def create(
        vector_shape: Tuple[int, int, int],
        patch_shape: Tuple[int, int, int],
        overlap_length: int,
    ):
        vector_height, vector_width, vector_c = vector_shape
        shape_height, shape_width, shape_c = patch_shape
        overlap_length = overlap_length
        pos_y = 0
        pos_x = 0
        patch_rows = 0
        patch_cols = 0
        pos_list: List[List[PatchPositionXY]] = []
        # loop for y
        while pos_y < vector_height - overlap_length * 2:
            pos_x = 0
            p_list_for_cols: List[PatchPositionXY] = []
            # loop for x
            while pos_x < vector_width - overlap_length * 2:
                p_list_for_cols.append(
                    PatchPositionXY(
                        PatchPosition(pos_x, vector_width, shape_width),
                        PatchPosition(pos_y, vector_height, shape_height),
                    )
                )
                pos_x = pos_x + shape_width - (overlap_length * 2)
                patch_cols += 1
            pos_list.append(p_list_for_cols)
            pos_y = pos_y + shape_height - (overlap_length * 2)
            patch_rows += 1
        return PatchPosXYCollection(patch_pos_list=pos_list)
