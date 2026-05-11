class RepartidorRepository:
    def __init__(self, repartidor_manager):
        self._manager = repartidor_manager

    def obtener(self, repartidor_id):
        return self._manager.obtener_repartidor(repartidor_id)

    def listar_disponibles(self):
        return self._manager.listar_disponibles()
