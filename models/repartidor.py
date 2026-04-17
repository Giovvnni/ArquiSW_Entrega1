from .pedido import Pedido
from interfaces import IRepartidor


class Repartidor(IRepartidor):
    """Entidad Repartidor: mantiene capacidad y lista de pedidos asignados.

    `asignar_pedido` verifica disponibilidad y que el pedido esté validado.
    """
    def __init__(self, id, capacidad):
        self.id = id
        self.capacidad = capacidad
        self.asignados = []
        # Ubicación actual del repartidor (puede ser None o dict con lat/lon)
        self.ubicacion = None

    @property
    def disponible(self):
        # Disponible si número de pedidos asignados es menor que la capacidad
        return len(self.asignados) < self.capacidad

    def asignar_pedido(self, pedido: Pedido):
        # Validaciones básicas antes de asignar
        if not pedido:
            raise ValueError("Pedido inválido")
        if not pedido.estado == "Validado":
            raise ValueError("Solo se pueden asignar pedidos validados")
        if not self.disponible:
            raise ValueError("Repartidor no disponible")

        # Registrar y actualizar estado del pedido
        self.asignados.append(pedido.id)
        pedido.asignar(self.id)
        return True

    def actualizar_ubicacion(self, ubicacion: dict):
        """Actualiza la ubicación del repartidor.

        `ubicacion` debe ser un dict mínimo con claves 'lat' y 'lon', aunque
        se permiten otros metadatos.
        """
        if not isinstance(ubicacion, dict) or 'lat' not in ubicacion or 'lon' not in ubicacion:
            raise ValueError("Ubicación inválida: se requiere dict con 'lat' y 'lon'")
        self.ubicacion = ubicacion

    def obtener_ubicacion(self):
        return self.ubicacion
