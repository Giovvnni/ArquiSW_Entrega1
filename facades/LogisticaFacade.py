"""Fachada para coordinar acciones entre subsistemas.

Depende de abstracciones de fábricas (DIP).
"""

from interfaces import IPedidoFactory, IRepartidorFactory


class LogisticaFacade:
    def __init__(self, pedido_factory: IPedidoFactory, repartidor_factory: IRepartidorFactory):
        self.pedido_factory = pedido_factory
        self.repartidor_factory = repartidor_factory

    def crear_y_asignar_pedido(self, pedido_data, repartidor_data):
        pedido = self.pedido_factory.crear_pedido(**pedido_data)
        # validar antes de intentar asignar
        pedido.validar()
        repartidor = self.repartidor_factory.crear_repartidor(**repartidor_data)
        repartidor.asignar_pedido(pedido)
        return pedido