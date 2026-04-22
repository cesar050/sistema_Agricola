from flask import Blueprint, request, jsonify
from models.cultivo_model import (
    get_all_cultivos, get_cultivo_by_id,
    create_cultivo, update_cultivo, delete_cultivo
)

cultivo_bp = Blueprint("cultivos", __name__)

@cultivo_bp.route("/", methods=["GET"])
def listar_cultivos():
    cultivos = get_all_cultivos()
    return jsonify({"success": True, "data": cultivos}), 200

@cultivo_bp.route("/<int:id>", methods=["GET"])
def obtener_cultivo(id):
    cultivo = get_cultivo_by_id(id)
    if not cultivo:
        return jsonify({"success": False, "message": "Cultivo no encontrado"}), 404
    return jsonify({"success": True, "data": cultivo}), 200

@cultivo_bp.route("/", methods=["POST"])
def crear_cultivo():
    data = request.get_json()
    campos = ["nombre", "tipo", "area_hectareas", "fecha_siembra"]
    for campo in campos:
        if campo not in data:
            return jsonify({"success": False, "message": f"Campo requerido: {campo}"}), 400
    new_id = create_cultivo(data)
    return jsonify({"success": True, "message": "Cultivo creado", "id": new_id}), 201

@cultivo_bp.route("/<int:id>", methods=["PUT"])
def actualizar_cultivo(id):
    data = request.get_json()
    affected = update_cultivo(id, data)
    if affected == 0:
        return jsonify({"success": False, "message": "Cultivo no encontrado"}), 404
    return jsonify({"success": True, "message": "Cultivo actualizado"}), 200

@cultivo_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_cultivo(id):
    affected = delete_cultivo(id)
    if affected == 0:
        return jsonify({"success": False, "message": "Cultivo no encontrado"}), 404
    return jsonify({"success": True, "message": "Cultivo eliminado"}), 200