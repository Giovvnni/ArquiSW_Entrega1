from models.pedido import Pedido


class PedidoFactory:
    @staticmethod
    def crear_pedido(id, origen, destino, tipo_entrega, canal_origen, tipo_carga, peso_volumen):
        return Pedido(id, origen, destino, tipo_entrega, canal_origen, tipo_carga, peso_volumen)