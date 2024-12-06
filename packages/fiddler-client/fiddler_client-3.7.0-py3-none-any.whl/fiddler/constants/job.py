import enum


@enum.unique
class JobStatus(str, enum.Enum):
    """Async job status enum"""

    PENDING = 'PENDING'
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    RETRY = 'RETRY'
    REVOKED = 'REVOKED'
