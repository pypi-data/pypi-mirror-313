MIN_SERVER_VERSION = '24.4.0'
DEFAULT_PAGE_SIZE = 50

# In seconds. For example, this generates a log message every N seconds. Was
# once set to 3, and I think that was too frequent. If this needs to be
# snappier and apply to both, short-running jobs as well as long-running jobs:
# we can grow the interval between polls.
JOB_POLL_INTERVAL = 6
JOB_WAIT_TIMEOUT = 1800

STREAM_EVENT_LIMIT = 1000
DEFAULT_NUM_CLUSTERS = 5
DEFAULT_NUM_TAGS = 5
