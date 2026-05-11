"""Notification manager: subscribes to events and notifies clients.

Por ahora envía notificaciones por consola y registra en memoria.
"""

from managers.EventBus import EventBus


class NotificationManager:
    def __init__(self):
        self.sent = []
        # Suscribirse a cambios de estado de pedidos
        EventBus.subscribe("pedido.estado_cambiado", self._on_pedido_estado)

    def _on_pedido_estado(self, event_type, payload):
        pedido_id = payload.get("pedido_id")
        nuevo = payload.get("nuevo_estado")
        destinatario = payload.get("destinatario")
        # Decidir si notificar al cliente según estado
        if nuevo in ("Asignado", "En ruta", "Entregado", "Cancelado"):
            message = f"Pedido {pedido_id} ahora: {nuevo}"
            if destinatario:
                message = f"Notificación a {destinatario}: {message}"
            # 'Enviar' notificación (simulada)
            print(message)
            self.sent.append({"pedido_id": pedido_id, "message": message})
