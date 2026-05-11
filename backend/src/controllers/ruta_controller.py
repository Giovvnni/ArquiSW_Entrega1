from flask import Blueprint, request, jsonify


def _serialize(ruta):
    return {
        "id": ruta.id,
        "estado": ruta.estado,
        "waypoints": ruta.waypoints,
        "current_index": ruta.current_index,
        "assigned_repartidor": ruta.assigned_repartidor,
        "last_reached": ruta.last_reached,
        "metadata": ruta.metadata,
    }


def create_ruta_bp(ruta_service):
    bp = Blueprint("rutas", __name__, url_prefix="/api/v1")

    @bp.post("/rutas")
    def definir_ruta():
        data = request.get_json(force=True, silent=True) or {}
        try:
            ruta = ruta_service.definir_ruta(data)
            return jsonify(_serialize(ruta)), 201
        except (TypeError, ValueError, RuntimeError) as e:
            return jsonify({"error": str(e)}), 400

    @bp.put("/rutas/<ruta_id>/avanzar")
    def avanzar_waypoint(ruta_id):
        try:
            ruta = ruta_service.avanzar_waypoint(ruta_id)
            return jsonify(_serialize(ruta)), 200
        except KeyError as e:
            return jsonify({"error": str(e)}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @bp.get("/rutas/<ruta_id>")
    def obtener_ruta(ruta_id):
        try:
            ruta = ruta_service.obtener_ruta(ruta_id)
            return jsonify(_serialize(ruta)), 200
        except KeyError as e:
            return jsonify({"error": str(e)}), 404

    return bp
