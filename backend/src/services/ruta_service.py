class RutaService:
    def __init__(self, facade, ruta_repo):
        self._facade = facade
        self._repo = ruta_repo

    def definir_ruta(self, data):
        ruta_id = data.get("id")
        waypoints = data.get("waypoints", [])
        metadata = data.get("metadata")
        repartidor_id = data.get("repartidor_id")
        ruta = self._facade.definir_ruta(ruta_id, waypoints=waypoints, metadata=metadata)
        if repartidor_id:
            self._facade.asignar_ruta(ruta_id, repartidor_id)
        return ruta

    def avanzar_waypoint(self, ruta_id):
        ruta = self._repo.obtener(ruta_id)
        if not ruta:
            raise KeyError("Ruta no encontrada")
        # Auto-iniciar si está asignada pero no en progreso todavía
        if ruta.estado == "Activa":
            self._facade.iniciar_ruta(ruta_id)
        return self._facade.marcar_waypoint(ruta_id)

    def obtener_ruta(self, ruta_id):
        ruta = self._repo.obtener(ruta_id)
        if not ruta:
            raise KeyError("Ruta no encontrada")
        return ruta
