HFI_CACHE_DURATION = 10
HFI_CACHE_DURATION_ON_ERROR = 60
HFI_CACHE_RETRY_DURATION_ON_ERROR = 1
HFI_SEMAPHORE_MINIMUM_CHECK_SIZE = 16 * 1024

DEFAULT_HFI_SEMAPHORE_COUNTER = 2
DEFAULT_HFI_SEMAPHORE_TIMEOUT = 5
DEFAULT_HFI_RATE_LIMIT_PACE = 1_000
DEFAULT_HFI_RATE_LIMIT_BURST = 1_000
DEFAULT_HFI_MAX_REQUEST_MB = 10
RATE_LIMITS_TOKENS_PER_REQUEST = 10
DEFAULT_HTTP_ERROR = 500
# HFI rate limits uses an hybrid approach
# They rely on Redis, but do not make a request
# to Redis per incoming request
# Instead, it will request multiple tokens
# (RATE_LIMITS_TOKENS_PER_REQUEST)
# and will use those "local" tokens
# until they are depleted, when depleted
# it will make a new request to Redis
# This solution provides global, number of workers
# independent rate-limiting, while having
# almost no overhead for communicating with
# Redis
HFI_SAMPLING_BUCKET = 100
REDIS_TIMEOUT = 2

LAG_MONITOR_THRESHOLD_IN_SECS = 0.5


class HfiDefaults:
    CH_INGESTION_BURST_SIZE = 2
    CH_INGESTION_TOKENS_PER_SECOND_DEFAULT = 0.25
    CH_INGESTION_TOKENS_PER_SECOND_GATHERER_DEFAULT = 0.25
    WAIT_FALSE_TRAFFIC_THROUGH_GATHERER = 1
    WAIT_TRUE_TRAFFIC_THROUGH_GATHERER = 1
