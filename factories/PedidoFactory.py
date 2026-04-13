from models.pedido import Pedido
from interfaces import IPedidoFactory


class PedidoFactory(IPedidoFactory):
    """Factory Method para crear instancias de `Pedido`.

    Centraliza la creación para poder cambiar la construcción en un solo lugar.
    """

    @staticmethod
    def crear_pedido(id, origen, destino, tipo_entrega, canal_origen, tipo_carga, peso_volumen):
        return Pedido(id, origen, destino, tipo_entrega, canal_origen, tipo_carga, peso_volumen)