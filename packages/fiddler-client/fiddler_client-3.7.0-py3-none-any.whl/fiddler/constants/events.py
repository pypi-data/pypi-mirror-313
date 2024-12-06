import enum


@enum.unique
class PublishEventsSourceType(str, enum.Enum):
    EVENTS = 'EVENTS'
    FILE = 'FILE'
