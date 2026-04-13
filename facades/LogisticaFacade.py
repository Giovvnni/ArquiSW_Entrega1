"""Fachada para coordinar acciones entre subsistemas.

La fachada simplifica el uso de varias piezas: creación (fábricas), validación
y asignación. Depende de abstracciones para facilitar pruebas y cambios.
"""

from interfaces import IPedidoFactory, IRepartidorFactory


class LogisticaFacade:
    def __init__(self, pedido_factory: IPedidoFactory, repartidor_factory: IRepartidorFactory):
        # Las fábricas son inyectadas para seguir DIP (dependencia de abstracciones)
        self.pedido_factory = pedido_factory
        self.repartidor_factory = repartidor_factory

    def crear_y_asignar_pedido(self, pedido_data, repartidor_data):
        # Crea el pedido usando la fábrica
        pedido = self.pedido_factory.crear_pedido(**pedido_data)
        # Validar según reglas de negocio antes de asignar
        pedido.validar()
        # Crear repartidor y asignar
        repartidor = self.repartidor_factory.crear_repartidor(**repartidor_data)
        repartidor.asignar_pedido(pedido)
        return pedido