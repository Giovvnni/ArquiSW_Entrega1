from abc import ABC, abstractmethod


class IPedido(ABC):
    @abstractmethod
    def validar(self):
        pass

    @abstractmethod
    def asignar(self, repartidor_id):
        pass


class IRepartidor(ABC):
    @property
    @abstractmethod
    def disponible(self):
        pass

    @abstractmethod
    def asignar_pedido(self, pedido: IPedido):
        pass


class IPedidoFactory(ABC):
    @staticmethod
    @abstractmethod
    def crear_pedido(id, origen, destino, tipo_entrega, canal_origen, tipo_carga, peso_volumen):
        pass


class IRepartidorFactory(ABC):
    @staticmethod
    @abstractmethod
    def crear_repartidor(id, capacidad):
        pass
