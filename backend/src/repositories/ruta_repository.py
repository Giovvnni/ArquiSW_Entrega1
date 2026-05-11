class RutaRepository:
    def __init__(self, route_manager):
        self._manager = route_manager

    def obtener(self, ruta_id):
        if self._manager is None:
            return None
        return self._manager.obtener_ruta(ruta_id)
