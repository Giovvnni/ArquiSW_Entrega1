from abc import ABC, abstractmethod


class IPedido(ABC):
    """Interfaz mínima para Pedido: expone operaciones necesarias para el flujo."""

    @abstractmethod
    def validar(self):
        pass

    @abstractmethod
    def asignar(self, repartidor_id):
        pass


class IRepartidor(ABC):
    """Interfaz mínima para Repartidor: disponibilidades y asignaciones."""

    @property
    @abstractmethod
    def disponible(self):
        pass

    @abstractmethod
    def asignar_pedido(self, pedido: IPedido):
        pass


class IPedidoFactory(ABC):
    """Fábrica para crear pedidos; permite cambiar la construcción sin tocar usuarios."""

    @staticmethod
    @abstractmethod
    def crear_pedido(id, origen, destino, tipo_entrega, canal_origen, tipo_carga, peso_volumen):
        pass


class IRepartidorFactory(ABC):
    """Fábrica para crear repartidores."""

    @staticmethod
    @abstractmethod
    def crear_repartidor(id, capacidad):
        pass
