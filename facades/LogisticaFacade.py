"""Fachada para coordinar acciones entre subsistemas.

La fachada simplifica el uso de varias piezas: creación (fábricas), validación
y asignación. Depende de abstracciones para facilitar pruebas y cambios.
"""

from interfaces import IPedidoFactory, IRepartidorFactory
from validators.channel_validators import ChannelValidator
from managers.RepartidorManager import RepartidorManager
from managers.RouteManager import RouteManager
from managers.EventLogger import EventLogger
from managers.NotificationManager import NotificationManager
from managers.PedidoManager import PedidoManager


class LogisticaFacade:
    def __init__(self, pedido_factory: IPedidoFactory, repartidor_factory: IRepartidorFactory, route_factory=None):
        # Las fábricas son inyectadas para seguir DIP (dependencia de abstracciones)
        self.pedido_factory = pedido_factory
        self.repartidor_factory = repartidor_factory
        # Gestor de repartidores en memoria
        self.repartidor_manager = RepartidorManager(self.repartidor_factory)
        # Gestor de rutas (opcional)
        self.route_manager = None
        if route_factory is not None:
            # pasar referencia al manager de repartidores para vincular rutas
            self.route_manager = RouteManager(route_factory, repartidor_manager=self.repartidor_manager)
        # Managers de monitoreo
        self.event_logger = EventLogger(log_file=None)
        self.notification_manager = NotificationManager()
        self.pedido_manager = PedidoManager()

    def crear_y_asignar_pedido(self, pedido_data, repartidor_data):
        # Crea el pedido usando la fábrica
        pedido = self.pedido_factory.crear_pedido(**pedido_data)
        # Registrar pedido en manager para consultas/monitoring
        try:
            self.pedido_manager.registrar(pedido)
        except Exception:
            pass
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

    def obtener_estado_pedido(self, pedido_id):
        p = self.pedido_manager.obtener(pedido_id)
        if not p:
            return None
        return p.estado

    def eventos_de_pedido(self, pedido_id):
        return self.event_logger.query_for("pedido_id", pedido_id)

    # Métodos de gestión de repartidores
    def registrar_repartidor(self, id, capacidad, ubicacion=None):
        return self.repartidor_manager.registrar_repartidor(id, capacidad, ubicacion)

    def actualizar_ubicacion_repartidor(self, id, ubicacion):
        return self.repartidor_manager.actualizar_ubicacion(id, ubicacion)

    def obtener_ubicacion_repartidor(self, id):
        return self.repartidor_manager.obtener_ubicacion(id)

    def listar_repartidores_disponibles(self):
        return self.repartidor_manager.listar_disponibles()

    # Rutas: definición, asignación, ajuste y seguimiento
    def definir_ruta(self, id, waypoints=None, metadata=None):
        if not self.route_manager:
            raise RuntimeError("RouteFactory no configurada en la fachada")
        return self.route_manager.definir_ruta(id, waypoints=waypoints, metadata=metadata)

    def asignar_ruta(self, ruta_id, repartidor_id):
        if not self.route_manager:
            raise RuntimeError("RouteFactory no configurada en la fachada")
        return self.route_manager.asignar_ruta(ruta_id, repartidor_id)

    def ajustar_ruta(self, ruta_id, **kwargs):
        if not self.route_manager:
            raise RuntimeError("RouteFactory no configurada en la fachada")
        return self.route_manager.ajustar_ruta(ruta_id, **kwargs)

    def iniciar_ruta(self, ruta_id):
        if not self.route_manager:
            raise RuntimeError("RouteFactory no configurada en la fachada")
        ruta = self.route_manager.iniciar_ruta(ruta_id)
        # Marcar pedidos asignados al repartidor como 'En ruta'
        repartidor_id = ruta.assigned_repartidor
        if repartidor_id:
            repartidor = self.repartidor_manager.obtener_repartidor(repartidor_id)
            if repartidor:
                for pedido_id in list(repartidor.asignados):
                    pedido = self.pedido_manager.obtener(pedido_id)
                    if pedido:
                        try:
                            pedido.marcar_en_ruta()
                            pedido.flush_events()
                        except Exception:
                            pass
        return ruta

    def marcar_waypoint(self, ruta_id):
        if not self.route_manager:
            raise RuntimeError("RouteFactory no configurada en la fachada")
        ruta = self.route_manager.marcar_waypoint(ruta_id)
        # Obtener el waypoint alcanzado
        reached = getattr(ruta, "last_reached", None)
        repartidor_id = ruta.assigned_repartidor
        if reached and repartidor_id:
            repartidor = self.repartidor_manager.obtener_repartidor(repartidor_id)
            if repartidor:
                # Para cada pedido asignado, si su destino coincide con el waypoint alcanzado,
                # imprimir llegada, marcar entregado y publicar evento
                for pedido_id in list(repartidor.asignados):
                    pedido = self.pedido_manager.obtener(pedido_id)
                    if not pedido:
                        continue
                    destino = pedido.destino if isinstance(pedido.destino, dict) else None
                    match = False
                    if destino:
                        # comparar dirección o coordenadas si están disponibles
                        if 'direccion' in destino and 'address' in reached and destino.get('direccion') == reached.get('address'):
                            match = True
                        if 'lat' in destino and 'lon' in destino and 'lat' in reached and 'lon' in reached:
                            if destino.get('lat') == reached.get('lat') and destino.get('lon') == reached.get('lon'):
                                match = True
                    if match:
                        # Imprimir llegada antes de cambiar estado
                        try:
                            addr = reached.get('address') or f"{reached.get('lat')},{reached.get('lon')}"
                            print(f"Repartidor {repartidor_id} llegó a {addr}")
                        except Exception:
                            pass
                        try:
                            pedido.entregar()
                            pedido.flush_events()
                        except Exception:
                            pass
        # Si la ruta se completó y quedan pedidos no marcados, intentar marcarlos como entregados
        if ruta.estado == "Completada":
            repartidor_id = ruta.assigned_repartidor
            if repartidor_id:
                repartidor = self.repartidor_manager.obtener_repartidor(repartidor_id)
                if repartidor:
                    for pedido_id in list(repartidor.asignados):
                        pedido = self.pedido_manager.obtener(pedido_id)
                        if pedido and pedido.estado != "Entregado":
                            try:
                                pedido.entregar()
                                pedido.flush_events()
                            except Exception:
                                pass
        return ruta