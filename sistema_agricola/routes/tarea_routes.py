from flask import Blueprint, request, jsonify
from models.tarea_model import (
    get_all_tareas, get_tarea_by_id, get_tareas_by_cultivo,
    create_tarea, update_tarea, update_estado_tarea,
    delete_tarea, get_tareas_pendientes, get_recomendaciones_automaticas
)

tarea_bp = Blueprint("tareas", __name__)

@tarea_bp.route("/", methods=["GET"])
def listar_tareas():
    tareas = get_all_tareas()
    return jsonify({"success": True, "data": tareas}), 200

@tarea_bp.route("/pendientes", methods=["GET"])
def tareas_pendientes():
    tareas = get_tareas_pendientes()
    return jsonify({"success": True, "data": tareas}), 200

@tarea_bp.route("/recomendaciones", methods=["GET"])
def recomendaciones():
    recs = get_recomendaciones_automaticas()
    return jsonify({"success": True, "data": recs}), 200

@tarea_bp.route("/cultivo/<int:cultivo_id>", methods=["GET"])
def tareas_por_cultivo(cultivo_id):
    tareas = get_tareas_by_cultivo(cultivo_id)
    return jsonify({"success": True, "data": tareas}), 200

@tarea_bp.route("/<int:id>", methods=["GET"])
def obtener_tarea(id):
    tarea = get_tarea_by_id(id)
    if not tarea:
        return jsonify({"success": False, "message": "Tarea no encontrada"}), 404
    return jsonify({"success": True, "data": tarea}), 200

@tarea_bp.route("/", methods=["POST"])
def crear_tarea():
    data = request.get_json()
    for campo in ["cultivo_id", "tipo_tarea", "fecha_programada"]:
        if campo not in data:
            return jsonify({"success": False, "message": f"Campo requerido: {campo}"}), 400
    new_id = create_tarea(data)
    return jsonify({"success": True, "message": "Tarea creada", "id": new_id}), 201

@tarea_bp.route("/<int:id>", methods=["PUT"])
def actualizar_tarea(id):
    data = request.get_json()
    affected = update_tarea(id, data)
    if affected == 0:
        return jsonify({"success": False, "message": "Tarea no encontrada"}), 404
    return jsonify({"success": True, "message": "Tarea actualizada"}), 200

@tarea_bp.route("/<int:id>/estado", methods=["PATCH"])
def cambiar_estado(id):
    data = request.get_json()
    estado = data.get("estado")
    if estado not in ["pendiente", "en proceso", "completada"]:
        return jsonify({"success": False, "message": "Estado inválido"}), 400
    affected = update_estado_tarea(id, estado)
    if affected == 0:
        return jsonify({"success": False, "message": "Tarea no encontrada"}), 404
    return jsonify({"success": True, "message": "Estado actualizado"}), 200

@tarea_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    affected = delete_tarea(id)
    if affected == 0:
        return jsonify({"success": False, "message": "Tarea no encontrada"}), 404
    return jsonify({"success": True, "message": "Tarea eliminada"}), 200