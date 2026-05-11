class PedidoRepository:
    def __init__(self, pedido_manager):
        self._manager = pedido_manager

    def guardar(self, pedido):
        try:
            self._manager.registrar(pedido)
        except ValueError:
            pass  # ya registrado, sin efecto

    def obtener(self, pedido_id):
        return self._manager.obtener(pedido_id)

    def listar(self):
        return self._manager.listar()
