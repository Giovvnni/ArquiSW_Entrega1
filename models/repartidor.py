from .pedido import Pedido
from interfaces import IRepartidor


class Repartidor(IRepartidor):
    def __init__(self, id, capacidad):
        self.id = id
        self.capacidad = capacidad
        self.asignados = []

    @property
    def disponible(self):
        return len(self.asignados) < self.capacidad

    def asignar_pedido(self, pedido: Pedido):
        if not pedido:
            raise ValueError("Pedido inválido")
        if not pedido.estado == "Validado":
            raise ValueError("Solo se pueden asignar pedidos validados")
        if not self.disponible:
            raise ValueError("Repartidor no disponible")
        self.asignados.append(pedido.id)
        pedido.asignar(self.id)
        return True
