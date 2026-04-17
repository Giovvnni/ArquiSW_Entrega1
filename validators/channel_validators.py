"""Registro simple de validadores por canal.

Permite extender la validación por canal sin tocar la entidad `Pedido`.
La implementación por defecto delega en `pedido.validar()`.
"""

from typing import Callable


class ChannelValidator:
    _registry = {}

    @classmethod
    def register(cls, canal: str, fn: Callable):
        cls._registry[canal] = fn

    @classmethod
    def validate(cls, canal: str, pedido):
        # Busca validador específico por canal, si no existe usa el validador genérico
        fn = cls._registry.get(canal)
        if fn:
            return fn(pedido)
        # Por defecto, reutiliza la validación del propio pedido
        return pedido.validar()


# Registraciones por defecto: pueden extenderse desde fuera
def _default_validator(pedido):
    return pedido.validar()


ChannelValidator.register("web", _default_validator)
ChannelValidator.register("mobile", _default_validator)
ChannelValidator.register("api", _default_validator)
ChannelValidator.register("telefono", _default_validator)
