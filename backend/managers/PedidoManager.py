"""Gestor de pedidos en memoria para facilitar consulta y monitoreo."""

from typing import Dict


class PedidoManager:
    def __init__(self):
        self._pedidos: Dict[str, object] = {}

    def registrar(self, pedido):
        if not pedido or not getattr(pedido, "id", None):
            raise ValueError("Pedido inválido")
        self._pedidos[pedido.id] = pedido

    def obtener(self, pedido_id):
        return self._pedidos.get(pedido_id)

    def listar(self):
        return list(self._pedidos.values())
