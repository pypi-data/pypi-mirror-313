import enum


@enum.unique
class BaselineType(str, enum.Enum):
    STATIC = 'STATIC'
    ROLLING = 'ROLLING'


@enum.unique
class WindowBinSize(str, enum.Enum):
    HOUR = 'Hour'
    DAY = 'Day'
    WEEK = 'Week'
    MONTH = 'Month'
