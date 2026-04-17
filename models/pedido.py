from interfaces import IPedido


class Pedido(IPedido):
    """Entidad Pedido: encapsula los datos y la lógica mínima del ciclo de vida.

    Las validaciones siguen las reglas de negocio: origen/destino, tipo de entrega,
    información logística e identificación mínima.
    """
    ESTADOS = (
        "Creado",
        "Validado",
        "Pendiente de asignación",
        "Asignado",
        "En ruta",
        "Intento fallido",
        "Reprogramado",
        "Entregado",
        "Cancelado",
    )

    def __init__(self, id, origen, destino, tipo_entrega, canal_origen, tipo_carga, peso_volumen):
        self.id = id
        self.origen = origen
        self.destino = destino
        self.tipo_entrega = tipo_entrega
        self.canal_origen = canal_origen
        self.tipo_carga = tipo_carga
        self.peso_volumen = peso_volumen
        self.estado = "Creado"
        self.repartidor_asignado = None

        # Definición explícita de transiciones permitidas (máquina de estados)
        self._transiciones = {
            "Creado": ("Validado", "Cancelado"),
            "Validado": ("Pendiente de asignación", "Asignado", "Cancelado"),
            "Pendiente de asignación": ("Asignado", "Cancelado"),
            "Asignado": ("En ruta", "Reprogramado", "Cancelado"),
            "En ruta": ("Entregado", "Intento fallido", "Cancelado"),
            "Intento fallido": ("Reprogramado", "En ruta", "Cancelado"),
            "Reprogramado": ("Pendiente de asignación", "Asignado", "Cancelado"),
            "Entregado": tuple(),
            "Cancelado": tuple(),
        }

    def validar(self):
        # Verifica que exista información del punto de origen y que sea coherente
        if not (self.origen and isinstance(self.origen, dict)):
            raise ValueError("Origen incompleto o inválido")
        if not self.origen.get("direccion") or not self.origen.get("id_punto_origen"):
            raise ValueError("Origen incompleto: falta dirección o id_punto_origen")
        # Verifica datos del destinatario y medio de contacto
        if not (self.destino and isinstance(self.destino, dict)):
            raise ValueError("Destino incompleto o inválido")
        if not self.destino.get("direccion") or not self.destino.get("nombre_destinatario") or not self.destino.get("medio_contacto"):
            raise ValueError("Destino incompleto: falta dirección, nombre_destinatario o medio_contacto")
        if self.tipo_entrega not in ("normal", "express", "programada"):
            raise ValueError("Tipo de entrega inválido")
        if not self.tipo_carga or not self.peso_volumen:
            raise ValueError("Información logística incompleta")
        if not self.id or not self.canal_origen:
            raise ValueError("Identificación incompleta")
        # Comprobación sencilla de que la dirección es razonable
        if len(self.destino.get("direccion", "")) < 5:
            raise ValueError("Dirección no interpretable")

        # Si todo ok, marcar como validado usando la máquina de estados
        self._cambiar_estado("Validado")
        return True

    def asignar(self, repartidor_id):
        # Sólo se asignan pedidos validados
        if self.estado not in ("Validado", "Pendiente de asignación"):
            raise ValueError("El pedido debe estar validado o pendiente antes de asignarse")
        self.repartidor_asignado = repartidor_id
        self._cambiar_estado("Asignado")

    def marcar_en_ruta(self):
        # Cambia estado a 'En ruta' sólo desde 'Asignado'
        self._cambiar_estado("En ruta")

    def entregar(self):
        # La entrega es el estado terminal del flujo operativo
        self._cambiar_estado("Entregado")

    def cancelar(self):
        # Un pedido entregado no puede cancelarse; cualquier otro estado sí
        self._cambiar_estado("Cancelado")

    def _cambiar_estado(self, nuevo_estado):
        # Comprueba que la transición está permitida según la máquina de estados
        actuales_permitidos = self._transiciones.get(self.estado, tuple())
        if nuevo_estado == self.estado:
            return
        if nuevo_estado not in actuales_permitidos:
            raise ValueError(f"Transición no permitida: {self.estado} -> {nuevo_estado}")
        # Restricción adicional: no permitir cancelar un pedido entregado
        if self.estado == "Entregado" and nuevo_estado == "Cancelado":
            raise ValueError("Un pedido entregado no puede cancelarse")
        self.estado = nuevo_estado
