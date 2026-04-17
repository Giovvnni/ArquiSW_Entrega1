"""Fachada para coordinar acciones entre subsistemas.

La fachada simplifica el uso de varias piezas: creación (fábricas), validación
y asignación. Depende de abstracciones para facilitar pruebas y cambios.
"""

from interfaces import IPedidoFactory, IRepartidorFactory
from validators.channel_validators import ChannelValidator
from managers.RepartidorManager import RepartidorManager


class LogisticaFacade:
    def __init__(self, pedido_factory: IPedidoFactory, repartidor_factory: IRepartidorFactory):
        # Las fábricas son inyectadas para seguir DIP (dependencia de abstracciones)
        self.pedido_factory = pedido_factory
        self.repartidor_factory = repartidor_factory
        # Gestor de repartidores en memoria
        self.repartidor_manager = RepartidorManager(self.repartidor_factory)

    def crear_y_asignar_pedido(self, pedido_data, repartidor_data):
        # Crea el pedido usando la fábrica
        pedido = self.pedido_factory.crear_pedido(**pedido_data)
        # Validar según reglas de negocio por canal antes de asignar
        ChannelValidator.validate(pedido.canal_origen, pedido)
        # Registrar o reutilizar repartidor desde el manager y asignar
        repartidor_id = repartidor_data.get("id")
        if repartidor_id and self.repartidor_manager.obtener_repartidor(repartidor_id):
            self.repartidor_manager.asignar_pedido_a_repartidor(repartidor_id, pedido)
        else:
            # Registrar nuevo repartidor en el manager y asignar
            repartidor = self.repartidor_manager.registrar_repartidor(
                repartidor_data.get("id"), repartidor_data.get("capacidad"), repartidor_data.get("ubicacion")
            )
            repartidor.asignar_pedido(pedido)
        return pedido

    # Métodos de gestión de repartidores
    def registrar_repartidor(self, id, capacidad, ubicacion=None):
        return self.repartidor_manager.registrar_repartidor(id, capacidad, ubicacion)

    def actualizar_ubicacion_repartidor(self, id, ubicacion):
        return self.repartidor_manager.actualizar_ubicacion(id, ubicacion)

    def obtener_ubicacion_repartidor(self, id):
        return self.repartidor_manager.obtener_ubicacion(id)

    def listar_repartidores_disponibles(self):
        return self.repartidor_manager.listar_disponibles()