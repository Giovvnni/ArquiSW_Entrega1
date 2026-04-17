"""Event logger: registra eventos en memoria y archivo.

Se suscribe al `EventBus` y guarda eventos para auditoría y consulta.
"""

import json
from datetime import datetime
from managers.EventBus import EventBus


class EventLogger:
    def __init__(self, log_file=None):
        self.events = []
        self.log_file = log_file
        EventBus.subscribe("*", self._handle_event)

    def _handle_event(self, event_type, payload):
        entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "event": event_type,
            "payload": payload,
        }
        self.events.append(entry)
        if self.log_file:
            try:
                with open(self.log_file, "a") as f:
                    f.write(json.dumps(entry) + "\n")
            except Exception:
                pass

    def query_for(self, key, value):
        return [e for e in self.events if e["payload"].get(key) == value]
