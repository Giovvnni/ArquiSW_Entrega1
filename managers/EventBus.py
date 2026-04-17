"""Simple event bus singleton for pub/sub across the application."""

from collections import defaultdict


class EventBus:
    _subscribers = defaultdict(list)

    @classmethod
    def subscribe(cls, event_type: str, fn):
        cls._subscribers[event_type].append(fn)

    @classmethod
    def publish(cls, event_type: str, payload: dict):
        # Notify subscribers for the specific event and for wildcard '*'
        for fn in list(cls._subscribers.get(event_type, [])) + list(cls._subscribers.get("*", [])):
            try:
                fn(event_type, payload)
            except Exception:
                # Never let a subscriber break the bus
                pass
