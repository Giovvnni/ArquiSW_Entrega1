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
        "tipo_carga": "paquete",
        "peso_volumen": 5
    }

    repartidor_data = {
        "id": "R1",
        "capacidad": 10
    }

    # Registrar un repartidor en el sistema y actualizar su ubicación
    facade.registrar_repartidor("R1", 10, ubicacion={"lat": 40.0, "lon": -3.0})
    print("Repartidor R1 registrado y ubicado.")

    # Crear pedido (factory) y mostrar estado en cada punto
    pedido = PedidoFactory.crear_pedido(**pedido_data)
    # Registrar para monitoreo
    try:
        facade.pedido_manager.registrar(pedido)
    except Exception:
        pass
    print(f"[CREADO] Pedido {pedido.id} estado: {pedido.estado}")

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

    # Ejemplo adicional: pedido desde 'telefono' (mismo flujo, validación por canal)
    pedido_data_tel = pedido_data.copy()
    pedido_data_tel["id"] = "124"
    pedido_data_tel["canal_origen"] = "telefono"

    repartidor_data2 = {"id": "R2", "capacidad": 1}
    # Registrar R2 y crear pedido 124 paso a paso mostrando estados
    facade.registrar_repartidor("R2", 1)
    pedido2 = PedidoFactory.crear_pedido(**pedido_data_tel)
    try:
        facade.pedido_manager.registrar(pedido2)
    except Exception:
        pass
    print(f"[CREADO] Pedido {pedido2.id} estado: {pedido2.estado}")
    ChannelValidator.validate(pedido2.canal_origen, pedido2)
    print(f"[VALIDADO] Pedido {pedido2.id} estado: {pedido2.estado}")
    try:
        facade.repartidor_manager.asignar_pedido_a_repartidor("R2", pedido2)
    except Exception:
        # Si R2 no existe por alguna razón, registrarlo y volver a intentar
        facade.registrar_repartidor("R2", 1)
        facade.repartidor_manager.asignar_pedido_a_repartidor("R2", pedido2)
    print(f"[ASIGNADO] Pedido {pedido2.id} estado: {pedido2.estado}, repartidor: {pedido2.repartidor_asignado}")

    # Mostrar destino(s) del segundo pedido también
    destinos2 = pedido2.destino if not isinstance(pedido2.destino, list) else pedido2.destino
    if isinstance(destinos2, dict):
        destinos2_list = [destinos2]
    else:
        destinos2_list = destinos2
    print(f"Destinos pedido {pedido2.id}:")
    for d in destinos2_list:
        print(f" - {d.get('direccion')} (destinatario: {d.get('nombre_destinatario')}, contacto: {d.get('medio_contacto')})")

    # Monitorizar ubicación del repartidor R1
    ubic = facade.obtener_ubicacion_repartidor("R1")
    print(f"Ubicación R1: {ubic}")

    # Listar repartidores disponibles
    disponibles = facade.listar_repartidores_disponibles()
    print(f"Repartidores disponibles: {[r.id for r in disponibles]}")

    # Simular transición a 'En ruta' y 'Entregado'
    pedido2.marcar_en_ruta()
    print(f"Pedido {pedido2.id} nuevo estado: {pedido2.estado}")
    pedido2.entregar()
    print(f"Pedido {pedido2.id} nuevo estado: {pedido2.estado}")

    # Definir una ruta basada en origen y destino(s) del pedido 123 y asignarla a R1
    waypoints = []
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

    # Ajuste dinámico: añadir un waypoint
    facade.ajustar_ruta("ruta-1", add_waypoint={"lat":40.2,"lon":-3.2})
    print(f"Waypoints actuales: {ruta.waypoints}")

    # MONITORIZACIÓN Y TRACKING: visualizar estados, registrar eventos y notificar
    estado_123 = facade.obtener_estado_pedido("123")
    print(f"Estado actual pedido 123: {estado_123}")

    eventos_123 = facade.eventos_de_pedido("123")
    print(f"Eventos para pedido 123 (últimos {len(eventos_123)}):")
    for e in eventos_123:
        print(e)