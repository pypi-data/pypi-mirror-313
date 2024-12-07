# coding: utf-8

from silx.utils.enum import Enum as _Enum


class Target(_Enum):
    LOCAL = "local"
    SLURM = "slurm"
