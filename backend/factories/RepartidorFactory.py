from models.repartidor import Repartidor
from interfaces import IRepartidorFactory


class RepartidorFactory(IRepartidorFactory):
    """Factory Method para crear instancias de `Repartidor`."""

    @staticmethod
    def crear_repartidor(id, capacidad):
        return Repartidor(id, capacidad)