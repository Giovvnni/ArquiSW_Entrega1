class RepartidorService:
    def __init__(self, facade, repartidor_repo, pedido_repo):
        self._facade = facade
        self._repo = repartidor_repo
        self._pedido_repo = pedido_repo

    def registrar(self, data):
        return self._facade.registrar_repartidor(
            data.get("id"), data.get("capacidad"), data.get("ubicacion")
        )

    def asignar_pedido(self, pedido_id, repartidor_id):
        pedido = self._pedido_repo.obtener(pedido_id)
        if not pedido:
            raise KeyError("Pedido no encontrado")
        repartidor = self._repo.obtener(repartidor_id)
        if not repartidor:
            raise KeyError("Repartidor no encontrado")
        self._facade.repartidor_manager.asignar_pedido_a_repartidor(repartidor_id, pedido)
        pedido.flush_events()
        return pedido

    def obtener_repartidor(self, repartidor_id):
        repartidor = self._repo.obtener(repartidor_id)
        if not repartidor:
            raise KeyError("Repartidor no encontrado")
        return repartidor
