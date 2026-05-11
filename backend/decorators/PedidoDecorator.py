"""Decoradores para `Pedido`.

Permiten añadir comportamiento (por ejemplo prioridad) sin tocar la clase base.
"""


class PedidoDecorator:
    def __init__(self, pedido):
        # Envuelve una instancia de Pedido y delega llamadas por defecto
        self._pedido = pedido

    def validar(self):
        return self._pedido.validar()


class PedidoPrioritario(PedidoDecorator):
    def validar(self):
        # Ejemplo simple: registrar que es prioritario antes de validar
        print("Validando pedido prioritario...")
        return super().validar()