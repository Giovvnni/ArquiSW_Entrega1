# PedidoDecorator

class PedidoDecorator:
    def __init__(self, pedido):
        self._pedido = pedido

    def validar(self):
        return self._pedido.validar()

class PedidoPrioritario(PedidoDecorator):
    def validar(self):
        print("Validando pedido prioritario...")
        return super().validar()