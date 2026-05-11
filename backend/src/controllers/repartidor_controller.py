from flask import Blueprint, request, jsonify


def _serialize(repartidor):
    return {
        "id": repartidor.id,
        "capacidad": repartidor.capacidad,
        "disponible": repartidor.disponible,
        "asignados": repartidor.asignados,
        "ubicacion": repartidor.ubicacion,
        "current_route": repartidor.current_route,
    }


def create_repartidor_bp(repartidor_service):
    bp = Blueprint("repartidores", __name__, url_prefix="/api/v1")

    @bp.post("/repartidores")
    def registrar_repartidor():
        data = request.get_json(force=True, silent=True) or {}
        try:
            repartidor = repartidor_service.registrar(data)
            return jsonify(_serialize(repartidor)), 201
        except (TypeError, ValueError) as e:
            return jsonify({"error": str(e)}), 400

    @bp.get("/repartidores/<repartidor_id>")
    def obtener_repartidor(repartidor_id):
        try:
            repartidor = repartidor_service.obtener_repartidor(repartidor_id)
            return jsonify(_serialize(repartidor)), 200
        except KeyError as e:
            return jsonify({"error": str(e)}), 404

    return bp
