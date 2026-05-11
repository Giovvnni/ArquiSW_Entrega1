"""Gestor de rutas: define rutas, ajusta dinámicamente y permite seguimiento.

Depende de una `route_factory` para crear instancias `Route`.
"""

from typing import Dict


class RouteManager:
    def __init__(self, route_factory, repartidor_manager=None):
        self._factory = route_factory
        self._routes: Dict[str, object] = {}
        self._repartidor_manager = repartidor_manager

    def definir_ruta(self, id, waypoints=None, metadata=None):
        if id in self._routes:
            raise ValueError("Ruta ya existe")
        ruta = self._factory.crear_ruta(id, waypoints=waypoints, metadata=metadata)
        self._routes[id] = ruta
        return ruta

    def obtener_ruta(self, id):
        return self._routes.get(id)

    def asignar_ruta(self, ruta_id, repartidor_id):
        ruta = self.obtener_ruta(ruta_id)
        if not ruta:
            raise ValueError("Ruta no encontrada")
        # Verificar repartidor existente si manager provisto
        if self._repartidor_manager and not self._repartidor_manager.obtener_repartidor(repartidor_id):
            raise ValueError("Repartidor no encontrado")
        ruta.asignar_a(repartidor_id)
        # Vincular en el repartidor si es posible
        if self._repartidor_manager:
            repartidor = self._repartidor_manager.obtener_repartidor(repartidor_id)
            if repartidor:
                repartidor.current_route = ruta.id
                repartidor.route_history.append(ruta.id)
        return ruta

    def ajustar_ruta(self, ruta_id, new_waypoints=None, add_waypoint=None, remove_index=None):
        ruta = self.obtener_ruta(ruta_id)
        if not ruta:
            raise ValueError("Ruta no encontrada")
        if new_waypoints is not None:
            ruta.reroute(new_waypoints)
        if add_waypoint is not None:
            ruta.add_waypoint(add_waypoint)
        if remove_index is not None:
            ruta.remove_waypoint(remove_index)
        return ruta

    def iniciar_ruta(self, ruta_id):
        ruta = self.obtener_ruta(ruta_id)
        if not ruta:
            raise ValueError("Ruta no encontrada")
        ruta.start()
        return ruta

    def marcar_waypoint(self, ruta_id):
        ruta = self.obtener_ruta(ruta_id)
        if not ruta:
            raise ValueError("Ruta no encontrada")
        reached = ruta.mark_waypoint_reached()
        return ruta
