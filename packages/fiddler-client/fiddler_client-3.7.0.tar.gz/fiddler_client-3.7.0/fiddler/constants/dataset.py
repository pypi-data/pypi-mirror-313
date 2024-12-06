import enum


@enum.unique
class EnvType(str, enum.Enum):
    PRODUCTION = 'PRODUCTION'
    PRE_PRODUCTION = 'PRE_PRODUCTION'
