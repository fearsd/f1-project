from prometheus_client import Counter

EVENTS_PROCESSED = Counter("achievements_events_processed_total", "Total number of events processed")