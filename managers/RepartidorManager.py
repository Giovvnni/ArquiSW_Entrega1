"""Gestor simple de repartidores: registro, disponibilidad, asignación y ubicación.

Usa la fábrica para crear instancias y mantiene un registro en memoria.
"""

from typing import Dict
from managers.EventBus import EventBus


class RepartidorManager:
    def __init__(self, repartidor_factory):
        self._factory = repartidor_factory
        self._repartidores: Dict[str, object] = {}

    def registrar_repartidor(self, id, capacidad, ubicacion=None):
        if id in self._repartidores:
            raise ValueError("Repartidor ya registrado")
        repartidor = self._factory.crear_repartidor(id, capacidad)
        if ubicacion:
            try:
                repartidor.actualizar_ubicacion(ubicacion)
            except Exception:
                pass
        self._repartidores[id] = repartidor
        # Informar sobre el registro de repartidor
        try:
            print(f"Repartidor {id} registrado (capacidad={capacidad}).")
            EventBus.publish("repartidor.registrado", {"repartidor_id": id, "capacidad": capacidad})
        except Exception:
            pass
        return repartidor

    def obtener_repartidor(self, id):
        return self._repartidores.get(id)

    def listar_disponibles(self):
        return [r for r in self._repartidores.values() if r.disponible]

    def asignar_pedido_a_repartidor(self, repartidor_id, pedido):
        repartidor = self.obtener_repartidor(repartidor_id)
        if not repartidor:
            raise ValueError("Repartidor no encontrado")
        return repartidor.asignar_pedido(pedido)

    def actualizar_ubicacion(self, repartidor_id, ubicacion):
        repartidor = self.obtener_repartidor(repartidor_id)
        if not repartidor:
            raise ValueError("Repartidor no encontrado")
        return repartidor.actualizar_ubicacion(ubicacion)

    def obtener_ubicacion(self, repartidor_id):
        repartidor = self.obtener_repartidor(repartidor_id)
        if not repartidor:
            return None
        return repartidor.obtener_ubicacion()
