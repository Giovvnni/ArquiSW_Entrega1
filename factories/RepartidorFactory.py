from models.repartidor import Repartidor


class RepartidorFactory:
    @staticmethod
    def crear_repartidor(id, capacidad):
        return Repartidor(id, capacidad)