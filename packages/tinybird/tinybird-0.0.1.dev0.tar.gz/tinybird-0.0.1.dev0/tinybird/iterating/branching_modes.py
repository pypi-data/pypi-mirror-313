from enum import Enum


class BranchMode(Enum):
    FORK = "fork"
    DEFAULT = "version"
    NONE = "None"

    def is_default(self):
        return self == BranchMode.DEFAULT or self == BranchMode.NONE


BRANCH_MODES = [a.value for a in BranchMode]
