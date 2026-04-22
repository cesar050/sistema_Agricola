from flask import Blueprint, request, jsonify
from models.lectura_model import (
    get_all_lecturas, get_lectura_by_id, get_lecturas_by_sensor,
    create_lectura, update_lectura, delete_lectura
)

lectura_bp = Blueprint("lecturas", __name__)

@lectura_bp.route("/", methods=["GET"])
def listar_lecturas():
    lecturas = get_all_lecturas()
    return jsonify({"success": True, "data": lecturas}), 200

@lectura_bp.route("/<int:id>", methods=["GET"])
def obtener_lectura(id):
    lectura = get_lectura_by_id(id)
    if not lectura:
        return jsonify({"success": False, "message": "Lectura no encontrada"}), 404
    return jsonify({"success": True, "data": lectura}), 200

@lectura_bp.route("/sensor/<int:sensor_id>", methods=["GET"])
def lecturas_por_sensor(sensor_id):
    lecturas = get_lecturas_by_sensor(sensor_id)
    return jsonify({"success": True, "data": lecturas}), 200

@lectura_bp.route("/", methods=["POST"])
def crear_lectura():
    data = request.get_json()
    for campo in ["sensor_id", "valor"]:
        if campo not in data:
            return jsonify({"success": False, "message": f"Campo requerido: {campo}"}), 400
    new_id = create_lectura(data)
    return jsonify({"success": True, "message": "Lectura registrada", "id": new_id}), 201

@lectura_bp.route("/<int:id>", methods=["PUT"])
def actualizar_lectura(id):
    data = request.get_json()
    affected = update_lectura(id, data)
    if affected == 0:
        return jsonify({"success": False, "message": "Lectura no encontrada"}), 404
    return jsonify({"success": True, "message": "Lectura actualizada"}), 200

@lectura_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_lectura(id):
    affected = delete_lectura(id)
    if affected == 0:
        return jsonify({"success": False, "message": "Lectura no encontrada"}), 404
    return jsonify({"success": True, "message": "Lectura eliminada"}), 200