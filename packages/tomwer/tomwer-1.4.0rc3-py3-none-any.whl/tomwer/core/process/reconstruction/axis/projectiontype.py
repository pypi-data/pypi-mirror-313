# coding: utf-8

from silx.utils.enum import Enum as _Enum


class ProjectionType(_Enum):
    """Type of projection"""

    transmission = "transmission"
    absorption = "absorption"
