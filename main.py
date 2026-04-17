import sys
import os
# Asegura que el directorio actual esté en el path para imports locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from factories.PedidoFactory import PedidoFactory
from factories.RepartidorFactory import RepartidorFactory
from factories.RouteFactory import RouteFactory
from decorators.PedidoDecorator import PedidoPrioritario
from facades.LogisticaFacade import LogisticaFacade

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

    # Crear y asignar un pedido (la fachada valida y asigna)
    pedido = facade.crear_y_asignar_pedido(pedido_data, repartidor_data)
    print(f"Pedido {pedido.id} estado: {pedido.estado}, repartidor: {pedido.repartidor_asignado}")

    # Ejemplo adicional: pedido desde 'telefono' (mismo flujo, validación por canal)
    pedido_data_tel = pedido_data.copy()
    pedido_data_tel["id"] = "124"
    pedido_data_tel["canal_origen"] = "telefono"

    repartidor_data2 = {"id": "R2", "capacidad": 1}
    # Registrar R2 y asignar
    facade.registrar_repartidor("R2", 1)
    pedido2 = facade.crear_y_asignar_pedido(pedido_data_tel, repartidor_data2)
    print(f"Pedido {pedido2.id} estado: {pedido2.estado}, repartidor: {pedido2.repartidor_asignado}")

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

    # Definir una ruta y asignarla a R1
    ruta = facade.definir_ruta("ruta-1", waypoints=[{"lat":40.0,"lon":-3.0},{"lat":40.1,"lon":-3.1}])
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