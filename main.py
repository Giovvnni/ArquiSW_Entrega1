import sys
import os
# Asegura que el directorio actual esté en el path para imports locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from factories.PedidoFactory import PedidoFactory
from factories.RepartidorFactory import RepartidorFactory
from decorators.PedidoDecorator import PedidoPrioritario
from facades.LogisticaFacade import LogisticaFacade

# Ejemplo de uso: flujo mínimo que crea, valida y asigna un pedido
if __name__ == "__main__":
    # Crear una fachada para gestionar la logística. La fachada orquesta fábricas y asignaciones.
    facade = LogisticaFacade(PedidoFactory, RepartidorFactory)

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

    # Crear y asignar un pedido (la fachada valida y asigna)
    pedido = facade.crear_y_asignar_pedido(pedido_data, repartidor_data)
    print(f"Pedido {pedido.id} estado: {pedido.estado}, repartidor: {pedido.repartidor_asignado}")

    # Ejemplo adicional: pedido desde 'telefono' (mismo flujo, validación por canal)
    pedido_data_tel = pedido_data.copy()
    pedido_data_tel["id"] = "124"
    pedido_data_tel["canal_origen"] = "telefono"

    repartidor_data2 = {"id": "R2", "capacidad": 1}
    pedido2 = facade.crear_y_asignar_pedido(pedido_data_tel, repartidor_data2)
    print(f"Pedido {pedido2.id} estado: {pedido2.estado}, repartidor: {pedido2.repartidor_asignado}")

    # Simular transición a 'En ruta' y 'Entregado'
    pedido2.marcar_en_ruta()
    print(f"Pedido {pedido2.id} nuevo estado: {pedido2.estado}")
    pedido2.entregar()
    print(f"Pedido {pedido2.id} nuevo estado: {pedido2.estado}")