from flask import Blueprint, jsonify


def _serialize_pedido(pedido):
    return {
        "id": pedido.id,
        "estado": pedido.estado,
        "repartidor_asignado": pedido.repartidor_asignado,
        "origen": pedido.origen,
        "destino": pedido.destino,
        "tipo_entrega": pedido.tipo_entrega,
        "canal_origen": pedido.canal_origen,
    }


def create_tracking_bp(tracking_service):
    bp = Blueprint("tracking", __name__, url_prefix="/api/v1")

    @bp.get("/tracking/<pedido_id>")
    def obtener_estado(pedido_id):
        try:
            pedido = tracking_service.obtener_estado(pedido_id)
            return jsonify(_serialize_pedido(pedido)), 200
        except KeyError as e:
            return jsonify({"error": str(e)}), 404

    @bp.get("/tracking/<pedido_id>/notificaciones")
    def obtener_notificaciones(pedido_id):
        notificaciones = tracking_service.obtener_notificaciones(pedido_id)
        return jsonify(notificaciones), 200

    return bp
