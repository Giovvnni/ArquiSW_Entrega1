from factories.PedidoFactory import PedidoFactory
from validators.channel_validators import ChannelValidator


class PedidoService:
    def __init__(self, facade, pedido_repo):
        self._facade = facade
        self._repo = pedido_repo

    def crear_pedido(self, data):
        pedido = PedidoFactory.crear_pedido(**data)
        self._repo.guardar(pedido)
        return pedido

    def validar_pedido(self, pedido_id):
        pedido = self._repo.obtener(pedido_id)
        if not pedido:
            raise KeyError("Pedido no encontrado")
        ChannelValidator.validate(pedido.canal_origen, pedido)
        pedido.flush_events()
        return pedido

    def actualizar_estado(self, pedido_id, nuevo_estado):
        pedido = self._repo.obtener(pedido_id)
        if not pedido:
            raise KeyError("Pedido no encontrado")
        if nuevo_estado == "Validado":
            ChannelValidator.validate(pedido.canal_origen, pedido)
        elif nuevo_estado == "Cancelado":
            pedido.cancelar()
        else:
            raise ValueError(f"Estado '{nuevo_estado}' no es accionable por este endpoint")
        pedido.flush_events()
        return pedido

    def obtener_pedido(self, pedido_id):
        pedido = self._repo.obtener(pedido_id)
        if not pedido:
            raise KeyError("Pedido no encontrado")
        return pedido
