"""Modelo `Route` que representa una ruta con waypoints y estado.

Diseñado para ser simple y permitir ajustes dinámicos y seguimiento.
"""

class Route:
    ESTADOS = ("Definida", "Activa", "En progreso", "Completada", "Cancelada")

    def __init__(self, id, waypoints=None, metadata=None):
        self.id = id
        self.waypoints = list(waypoints or [])
        self.metadata = metadata or {}
        self.estado = "Definida"
        self.assigned_repartidor = None
        self.current_index = 0  # índice del waypoint siguiente a completar
        self.last_reached = None

    def asignar_a(self, repartidor_id):
        self.assigned_repartidor = repartidor_id
        self.estado = "Activa"

    def add_waypoint(self, waypoint, index=None):
        if index is None:
            self.waypoints.append(waypoint)
        else:
            self.waypoints.insert(index, waypoint)

    def remove_waypoint(self, index):
        if index < 0 or index >= len(self.waypoints):
            raise IndexError("Waypoint index out of range")
        del self.waypoints[index]

    def reroute(self, new_waypoints):
        self.waypoints = list(new_waypoints)
        # Reset progress if needed
        self.current_index = 0

    def start(self):
        if not self.waypoints:
            raise ValueError("No hay waypoints para iniciar la ruta")
        self.estado = "En progreso"

    def mark_waypoint_reached(self):
        if self.estado != "En progreso":
            raise ValueError("La ruta no está en progreso")
        if self.current_index < len(self.waypoints):
            # registrar el waypoint alcanzado
            self.last_reached = self.waypoints[self.current_index]
            self.current_index += 1
        else:
            self.last_reached = None
        if self.current_index >= len(self.waypoints):
            self.estado = "Completada"
        return self.last_reached

    def get_next_waypoint(self):
        if self.current_index < len(self.waypoints):
            return self.waypoints[self.current_index]
        return None

    def cancel(self):
        self.estado = "Cancelada"
