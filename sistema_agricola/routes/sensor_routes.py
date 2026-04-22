from flask import Blueprint, request, jsonify
from models.sensor_model import (
    get_all_sensores, get_sensor_by_id, get_sensores_by_cultivo,
    create_sensor, update_sensor, delete_sensor
)

sensor_bp = Blueprint("sensores", __name__)

@sensor_bp.route("/", methods=["GET"])
def listar_sensores():
    sensores = get_all_sensores()
    return jsonify({"success": True, "data": sensores}), 200

@sensor_bp.route("/<int:id>", methods=["GET"])
def obtener_sensor(id):
    sensor = get_sensor_by_id(id)
    if not sensor:
        return jsonify({"success": False, "message": "Sensor no encontrado"}), 404
    return jsonify({"success": True, "data": sensor}), 200

@sensor_bp.route("/cultivo/<int:cultivo_id>", methods=["GET"])
def sensores_por_cultivo(cultivo_id):
    sensores = get_sensores_by_cultivo(cultivo_id)
    return jsonify({"success": True, "data": sensores}), 200

@sensor_bp.route("/", methods=["POST"])
def crear_sensor():
    data = request.get_json()
    for campo in ["cultivo_id", "tipo_sensor"]:
        if campo not in data:
            return jsonify({"success": False, "message": f"Campo requerido: {campo}"}), 400
    new_id = create_sensor(data)
    return jsonify({"success": True, "message": "Sensor creado", "id": new_id}), 201

@sensor_bp.route("/<int:id>", methods=["PUT"])
def actualizar_sensor(id):
    data = request.get_json()
    affected = update_sensor(id, data)
    if affected == 0:
        return jsonify({"success": False, "message": "Sensor no encontrado"}), 404
    return jsonify({"success": True, "message": "Sensor actualizado"}), 200

@sensor_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_sensor(id):
    affected = delete_sensor(id)
    if affected == 0:
        return jsonify({"success": False, "message": "Sensor no encontrado"}), 404
    return jsonify({"success": True, "message": "Sensor eliminado"}), 200