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

    # --- Nuevo pedido express que debe sobrepasar prioridad ---
    pedido_data2 = {
        "id": "124",
        "origen": {"direccion": "Calle 1", "id_punto_origen": "A1"},
        "destino": {"direccion": "Calle 3", "nombre_destinatario": "Rodrigo", "medio_contacto": "987654321"},
        "tipo_entrega": "express",
        "canal_origen": "telefono",
        "canal_detalle": {"numero": "555-0100"},
        "tipo_carga": "paquete",
        "peso_volumen": 2
    }

    pedido2 = PedidoFactory.crear_pedido(**pedido_data2)
    try:
        facade.pedido_manager.registrar(pedido2)
    except Exception:
        pass
    print(f"[CREADO] Pedido {pedido2.id} estado: {pedido2.estado} (canal: {pedido2.canal_origen}, detalle: {pedido2.canal_detalle}, tipo_entrega: {pedido2.tipo_entrega})")
    ChannelValidator.validate(pedido2.canal_origen, pedido2)
    print(f"[VALIDADO] Pedido {pedido2.id} estado: {pedido2.estado}")
    try:
        facade.repartidor_manager.asignar_pedido_a_repartidor("R1", pedido2)
    except Exception:
        facade.registrar_repartidor("R1", 10)
        facade.repartidor_manager.asignar_pedido_a_repartidor("R1", pedido2)
    print(f"[ASIGNADO] Pedido {pedido2.id} estado: {pedido2.estado}, repartidor: {pedido2.repartidor_asignado}")
    try:
        pedido2.flush_events()
    except Exception:
        pass

    # Mostrar estado actual de repartidores (depuración)
    print("Repartidores registrados:")
    for r in facade.repartidor_manager._repartidores.values():
        print(f" - {r.id}: asignados={r.asignados}, ubicacion={r.ubicacion}")

    # Consolidado: mostrar destinos de todos los pedidos actualmente asignados
    print("Destinos de pedidos asignados:")
    for p in facade.pedido_manager.listar():
        if not getattr(p, 'repartidor_asignado', None):
            continue
        dests = p.destino if not isinstance(p.destino, list) else p.destino
        if isinstance(dests, dict):
            dests = [dests]
        print(f" Pedido {p.id} (repartidor: {p.repartidor_asignado}):")
        for d in dests:
            print(f"  - {d.get('direccion')} (destinatario: {d.get('nombre_destinatario')}, contacto: {d.get('medio_contacto')})")

    # (DEBUG) Actualmente sólo usamos el repartidor R1 y un pedido.

    # Monitorizar ubicación del repartidor R1
    ubic = facade.obtener_ubicacion_repartidor("R1")
    print(f"Ubicación R1: {ubic}")

    # Listar repartidores disponibles
    disponibles = facade.listar_repartidores_disponibles()
    print(f"Repartidores disponibles: {[r.id for r in disponibles]}")

    # (En este debug no simulamos entregas adicionales)

    # Definir una ruta basada en los pedidos asignados a R1.
    # Priorizar pedidos `express` por delante de `normal`.
    waypoints = []
    repartidor_ubic = facade.obtener_ubicacion_repartidor("R1")
    if repartidor_ubic:
        if 'lat' in repartidor_ubic and 'lon' in repartidor_ubic:
            waypoints.append({'lat': repartidor_ubic['lat'], 'lon': repartidor_ubic['lon']})
        else:
            addr = repartidor_ubic.get('direccion') or repartidor_ubic.get('address')
            waypoints.append({'address': addr})
    # Obtener pedidos asignados al repartidor y ordenarlos por prioridad (express primero)
    repartidor = facade.repartidor_manager.obtener_repartidor("R1")
    assigned_ids = list(repartidor.asignados) if repartidor else []
    assigned_pedidos = [facade.pedido_manager.obtener(pid) for pid in assigned_ids]
    # Orden simple: express -> normal -> otros
    assigned_pedidos_sorted = sorted(assigned_pedidos, key=lambda p: 0 if getattr(p, 'tipo_entrega', None) == 'express' else 1)
    for p in assigned_pedidos_sorted:
        if not p:
            continue
        dests = p.destino if not isinstance(p.destino, list) else p.destino
        if isinstance(dests, dict):
            dests = [dests]
        for d in dests:
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