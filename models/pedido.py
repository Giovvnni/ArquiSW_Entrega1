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

        # Si todo ok, marcar como validado
        self.estado = "Validado"
        return True

    def asignar(self, repartidor_id):
        # Sólo se asignan pedidos validados
        if self.estado != "Validado":
            raise ValueError("El pedido debe estar validado antes de asignarse")
        self.repartidor_asignado = repartidor_id
        self.estado = "Asignado"

    def marcar_en_ruta(self):
        # Cambia estado a 'En ruta' sólo desde 'Asignado'
        if self.estado != "Asignado":
            raise ValueError("Solo un pedido asignado puede pasar a 'En ruta'")
        self.estado = "En ruta"

    def entregar(self):
        # La entrega es el estado terminal del flujo operativo
        if self.estado != "En ruta":
            raise ValueError("Solo un pedido 'En ruta' puede entregarse")
        self.estado = "Entregado"

    def cancelar(self):
        # Un pedido entregado no puede cancelarse; cualquier otro estado sí
        if self.estado == "Entregado":
            raise ValueError("Un pedido entregado no puede cancelarse")
        self.estado = "Cancelado"
