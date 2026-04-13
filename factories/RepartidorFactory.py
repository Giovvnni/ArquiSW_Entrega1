from models.repartidor import Repartidor
from interfaces import IRepartidorFactory


class RepartidorFactory(IRepartidorFactory):
    @staticmethod
    def crear_repartidor(id, capacidad):
        return Repartidor(id, capacidad)