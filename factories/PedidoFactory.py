from models.pedido import Pedido
from interfaces import IPedidoFactory


class PedidoFactory(IPedidoFactory):
    """Factory Method para crear instancias de `Pedido`.

    Centraliza la creación para poder cambiar la construcción en un solo lugar.
    """

    @staticmethod
    def crear_pedido(id, origen, destino, tipo_entrega, canal_origen, tipo_carga, peso_volumen, canal_detalle=None):
        # Normalizar canal_detalle según el canal de creación
        cd = canal_detalle or {}
        if canal_origen == "telefono":
            # Preferir el número proporcionado en canal_detalle, si no existe usar destino.medio_contacto
            if not cd.get("telefono_origen"):
                if isinstance(destino, dict):
                    telefono = destino.get("medio_contacto")
                    if telefono:
                        cd["telefono_origen"] = telefono
        elif canal_origen == "web":
            cd.setdefault("ip", None)
            cd.setdefault("user_agent", None)
        elif canal_origen == "api":
            cd.setdefault("api_key", None)
        elif canal_origen == "mobile":
            cd.setdefault("device_id", None)

        return Pedido(id, origen, destino, tipo_entrega, canal_origen, tipo_carga, peso_volumen, cd)