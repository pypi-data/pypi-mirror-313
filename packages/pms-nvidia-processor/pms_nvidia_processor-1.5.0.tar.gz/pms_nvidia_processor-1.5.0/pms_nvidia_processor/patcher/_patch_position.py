from pms_nvidia_processor._const import *


@dataclass
class PatchPosition:
    target_pos: int
    target_length: int
    patch_length: int

    def __iter__(self):
        yield self.p1
        yield self.p2

    @property
    def p1(self) -> int:
        assert (
            self.target_pos < self.target_length
        ), f"ERROR, assert self.target_pos < self.target_length"
        return self.target_pos

    @property
    def p2(self) -> int:
        pos = self.target_pos + self.patch_length
        pos = pos if pos < self.target_length else self.target_length
        assert pos != self.p1, f"ERROR, pos != self.p1"
        return pos

    @property
    def dp(self) -> int:
        dp = self.p2 - self.p1
        assert dp > 0, f"ERROR, p1 and p2 are same. p1: {self.p1}, p2: {self.p2}"
        return dp

    @property
    def range(self) -> slice:
        return slice(self.p1, self.p2)


@dataclass
class PatchPositionXY:
    x: PatchPosition
    y: PatchPosition
