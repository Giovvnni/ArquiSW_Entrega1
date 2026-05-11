class TrackingService:
    def __init__(self, facade):
        self._facade = facade

    def obtener_estado(self, pedido_id):
        pedido = self._facade.pedido_manager.obtener(pedido_id)
        if not pedido:
            raise KeyError("Pedido no encontrado")
        return pedido

    def obtener_notificaciones(self, pedido_id):
        return [
            n for n in self._facade.notification_manager.sent
            if n.get("pedido_id") == pedido_id
        ]
