from .base import Axis
from .component import AxisTick, AxisLabel, AxisLine, AxisPointer, AxisPointerLabel, SplitArea, SplitLine
from .style import AreaStyle, NameTextStyle, ShadowStyle, LineStyle

__all__ = ["Axis", 'AxisTick', 'AxisLabel', 'AxisLine', 'AxisPointer', 'AxisPointerLabel',
          'SplitArea', 'AreaStyle', 'NameTextStyle', 'ShadowStyle', 'LineStyle', 'SplitLine']


def get_all_supported_axis_components():
    return sorted(__all__)