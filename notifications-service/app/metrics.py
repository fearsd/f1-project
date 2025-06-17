from prometheus_client import Counter

EVENTS_PROCESSED = Counter("events_processed_total", "Total number of events processed")