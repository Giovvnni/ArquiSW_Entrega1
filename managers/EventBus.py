"""Simple event bus singleton for pub/sub across the application."""

from collections import defaultdict
import threading


class EventBus:
    _subscribers = defaultdict(list)

    @classmethod
    def subscribe(cls, event_type: str, fn):
        cls._subscribers[event_type].append(fn)

    @classmethod
    def publish(cls, event_type: str, payload: dict):
        # Notify subscribers asynchronously so publishers are not blocked
        subscribers = list(cls._subscribers.get(event_type, [])) + list(cls._subscribers.get("*", []))

        def _notify_all():
            for fn in subscribers:
                try:
                    fn(event_type, payload)
                except Exception:
                    pass

        t = threading.Thread(target=_notify_all, daemon=True)
        t.start()
