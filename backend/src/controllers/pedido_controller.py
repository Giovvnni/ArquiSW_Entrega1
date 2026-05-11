from flask import Blueprint, request, jsonify


def _serialize(pedido):
    return {
        "id": pedido.id,
        "estado": pedido.estado,
        "origen": pedido.origen,
        "destino": pedido.destino,
        "tipo_entrega": pedido.tipo_entrega,
        "canal_origen": pedido.canal_origen,
        "tipo_carga": pedido.tipo_carga,
        "peso_volumen": pedido.peso_volumen,
        "repartidor_asignado": pedido.repartidor_asignado,
    }


def create_pedido_bp(pedido_service, repartidor_service):
    bp = Blueprint("pedidos", __name__, url_prefix="/api/v1")

    @bp.post("/pedidos")
    def crear_pedido():
        data = request.get_json(force=True, silent=True) or {}
        try:
            pedido = pedido_service.crear_pedido(data)
            return jsonify(_serialize(pedido)), 201
        except (TypeError, ValueError) as e:
            return jsonify({"error": str(e)}), 400

    @bp.put("/pedidos/<pedido_id>/estado")
    def actualizar_estado(pedido_id):
        data = request.get_json(force=True, silent=True) or {}
        nuevo_estado = data.get("estado")
        if not nuevo_estado:
            return jsonify({"error": "Campo 'estado' requerido"}), 400
        try:
            pedido = pedido_service.actualizar_estado(pedido_id, nuevo_estado)
            return jsonify(_serialize(pedido)), 200
        except KeyError as e:
            return jsonify({"error": str(e)}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @bp.get("/pedidos/<pedido_id>")
    def obtener_pedido(pedido_id):
        try:
            pedido = pedido_service.obtener_pedido(pedido_id)
            return jsonify(_serialize(pedido)), 200
        except KeyError as e:
            return jsonify({"error": str(e)}), 404

    @bp.post("/pedidos/<pedido_id>/asignar")
    def asignar_pedido(pedido_id):
        data = request.get_json(force=True, silent=True) or {}
        repartidor_id = data.get("repartidor_id")
        if not repartidor_id:
            return jsonify({"error": "Campo 'repartidor_id' requerido"}), 400
        try:
            pedido = repartidor_service.asignar_pedido(pedido_id, repartidor_id)
            return jsonify(_serialize(pedido)), 200
        except KeyError as e:
            return jsonify({"error": str(e)}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    return bp
