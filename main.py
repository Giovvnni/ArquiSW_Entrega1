import sys
import os
# Asegura que el directorio actual esté en el path para imports locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from factories.PedidoFactory import PedidoFactory
from factories.RepartidorFactory import RepartidorFactory
from factories.RouteFactory import RouteFactory
from decorators.PedidoDecorator import PedidoPrioritario
from facades.LogisticaFacade import LogisticaFacade
from validators.channel_validators import ChannelValidator

# Ejemplo de uso: flujo mínimo que crea, valida y asigna un pedido
if __name__ == "__main__":
    # Crear una fachada para gestionar la logística. La fachada orquesta fábricas y asignaciones.
    facade = LogisticaFacade(PedidoFactory, RepartidorFactory, route_factory=RouteFactory)

    # Datos de ejemplo para un pedido y un repartidor
    pedido_data = {
        "id": "123",
        "origen": {"direccion": "Calle 1", "id_punto_origen": "A1"},
        "destino": {"direccion": "Calle 2", "nombre_destinatario": "Juan", "medio_contacto": "123456789"},
        "tipo_entrega": "normal",
        "canal_origen": "web",
        "canal_detalle": {"ip": "192.0.2.1", "user_agent": "cli-test/1.0"},
        "tipo_carga": "paquete",
        "peso_volumen": 5
    }

    repartidor_data = {
        "id": "R1",
        "capacidad": 10
    }

    # Registrar un repartidor en el sistema y actualizar su ubicación (Centro de distribución)
    facade.registrar_repartidor("R1", 10, ubicacion={"direccion": "Centro de distribución"})
    print("Repartidor R1 registrado y ubicado en Centro de distribución.")

    # Crear pedido (factory) y mostrar estado en cada punto
    pedido = PedidoFactory.crear_pedido(**pedido_data)
    # Registrar para monitoreo
    try:
        facade.pedido_manager.registrar(pedido)
    except Exception:
        pass
    origen_info = pedido.origen if isinstance(pedido.origen, dict) else {}
    punto_origen = f"{origen_info.get('direccion')} (id: {origen_info.get('id_punto_origen')})" if origen_info else "desconocido"
    print(f"[CREADO] Pedido {pedido.id} estado: {pedido.estado} (canal: {pedido.canal_origen}, detalle: {pedido.canal_detalle}, tipo_entrega: {pedido.tipo_entrega}, punto_origen: {punto_origen})")

    # Validar según canal
    ChannelValidator.validate(pedido.canal_origen, pedido)
    print(f"[VALIDADO] Pedido {pedido.id} estado: {pedido.estado}")

    # Asignar al repartidor registrado R1 (si no existe, registrar y reintentar)
    try:
        facade.repartidor_manager.asignar_pedido_a_repartidor("R1", pedido)
    except Exception:
        facade.registrar_repartidor("R1", 10)
        facade.repartidor_manager.asignar_pedido_a_repartidor("R1", pedido)
    print(f"[ASIGNADO] Pedido {pedido.id} estado: {pedido.estado}, repartidor: {pedido.repartidor_asignado}")
    try:
        pedido.flush_events()
    except Exception:
        pass

    # Mostrar estado actual de repartidores (depuración)
    print("Repartidores registrados:")
    for r in facade.repartidor_manager._repartidores.values():
        print(f" - {r.id}: asignados={r.asignados}, ubicacion={r.ubicacion}")

    # Mostrar detalles del destino(s) del pedido 123
    destinos = pedido.destino if not isinstance(pedido.destino, list) else pedido.destino
    if isinstance(destinos, dict):
        destinos_list = [destinos]
    else:
        destinos_list = destinos
    print(f"Destinos pedido {pedido.id}:")
    for d in destinos_list:
        print(f" - {d.get('direccion')} (destinatario: {d.get('nombre_destinatario')}, contacto: {d.get('medio_contacto')})")

    # (DEBUG) Actualmente sólo usamos el repartidor R1 y un pedido.

    # Monitorizar ubicación del repartidor R1
    ubic = facade.obtener_ubicacion_repartidor("R1")
    print(f"Ubicación R1: {ubic}")

    # Listar repartidores disponibles
    disponibles = facade.listar_repartidores_disponibles()
    print(f"Repartidores disponibles: {[r.id for r in disponibles]}")

    # (En este debug no simulamos entregas adicionales)

    # Definir una ruta basada en origen y destino(s) del pedido 123 y asignarla a R1
    waypoints = []
    # Usar la ubicación actual del repartidor (Centro de distribución) como punto de inicio si existe
    repartidor_ubic = facade.obtener_ubicacion_repartidor("R1")
    if repartidor_ubic:
        if 'lat' in repartidor_ubic and 'lon' in repartidor_ubic:
            waypoints.append({'lat': repartidor_ubic['lat'], 'lon': repartidor_ubic['lon']})
        else:
            # aceptar claves 'direccion' o 'address'
            addr = repartidor_ubic.get('direccion') or repartidor_ubic.get('address')
            waypoints.append({'address': addr})
    else:
        origen = pedido.origen if pedido.origen else {}
        if isinstance(origen, dict):
            if 'lat' in origen and 'lon' in origen:
                waypoints.append({'lat': origen['lat'], 'lon': origen['lon']})
            else:
                waypoints.append({'address': origen.get('direccion')})
    for d in destinos_list:
        if 'lat' in d and 'lon' in d:
            waypoints.append({'lat': d['lat'], 'lon': d['lon']})
        else:
            waypoints.append({'address': d.get('direccion')})

    ruta = facade.definir_ruta("ruta-1", waypoints=waypoints)
    facade.asignar_ruta("ruta-1", "R1")
    print(f"Ruta {ruta.id} asignada a {ruta.assigned_repartidor}, estado {ruta.estado}")

    # Iniciar la ruta y simular avance
    facade.iniciar_ruta("ruta-1")
    print(f"Ruta {ruta.id} estado tras iniciar: {ruta.estado}, siguiente waypoint: {ruta.get_next_waypoint()}")
    facade.marcar_waypoint("ruta-1")
    print(f"Ruta {ruta.id} estado: {ruta.estado}, siguiente waypoint: {ruta.get_next_waypoint()}")

    # Waypoints actuales (no añadimos waypoints extra en este debug)
    print(f"Waypoints actuales: {ruta.waypoints}")
    # Simular avance de la ruta hasta completarla
    while ruta.estado != "Completada":
        ruta = facade.marcar_waypoint("ruta-1")
        print(f"Ruta {ruta.id} estado: {ruta.estado}, siguiente waypoint: {ruta.get_next_waypoint()}")

    # MONITORIZACIÓN Y TRACKING: visualizar estados, registrar eventos y notificar
    estado_123 = facade.obtener_estado_pedido("123")
    print(f"Estado actual pedido 123: {estado_123}")

    eventos_123 = facade.eventos_de_pedido("123")
    print(f"Eventos para pedido 123 (últimos {len(eventos_123)}):")
    for e in eventos_123:
        print(e)