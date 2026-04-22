from database.connection import get_connection
from datetime import datetime

def get_all_tareas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.*, c.nombre as cultivo_nombre
        FROM tarea_agricola t
        JOIN cultivo c ON t.cultivo_id = c.id
        ORDER BY t.fecha_programada ASC
    """)
    result = cursor.fetchall()
    for r in result:
        if r.get('fecha_programada'):
            r['fecha_programada'] = str(r['fecha_programada'])
    conn.close()
    return result

def get_tareas_by_cultivo(cultivo_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.*, c.nombre as cultivo_nombre
        FROM tarea_agricola t
        JOIN cultivo c ON t.cultivo_id = c.id
        WHERE t.cultivo_id = %s
        ORDER BY t.fecha_programada ASC
    """, (cultivo_id,))
    result = cursor.fetchall()
    for r in result:
        if r.get('fecha_programada'):
            r['fecha_programada'] = str(r['fecha_programada'])
    conn.close()
    return result

def get_tarea_by_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.*, c.nombre as cultivo_nombre
        FROM tarea_agricola t
        JOIN cultivo c ON t.cultivo_id = c.id
        WHERE t.id = %s
    """, (id,))
    result = cursor.fetchone()
    if result and result.get('fecha_programada'):
        result['fecha_programada'] = str(result['fecha_programada'])
    conn.close()
    return result

def create_tarea(data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO tarea_agricola (cultivo_id, tipo_tarea, descripcion, fecha_programada, estado)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        data["cultivo_id"],
        data["tipo_tarea"],
        data.get("descripcion", ""),
        data["fecha_programada"],
        data.get("estado", "pendiente")
    )
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_tarea(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE tarea_agricola
        SET cultivo_id = %s, tipo_tarea = %s, descripcion = %s,
            fecha_programada = %s, estado = %s
        WHERE id = %s
    """
    values = (
        data["cultivo_id"],
        data["tipo_tarea"],
        data.get("descripcion", ""),
        data["fecha_programada"],
        data.get("estado", "pendiente"),
        id
    )
    cursor.execute(sql, values)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

def update_estado_tarea(id, estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarea_agricola SET estado = %s WHERE id = %s", (estado, id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

def delete_tarea(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarea_agricola WHERE id = %s", (id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

def get_tareas_pendientes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.*, c.nombre as cultivo_nombre
        FROM tarea_agricola t
        JOIN cultivo c ON t.cultivo_id = c.id
        WHERE t.estado != 'completada'
        ORDER BY t.fecha_programada ASC
    """)
    result = cursor.fetchall()
    for r in result:
        if r.get('fecha_programada'):
            r['fecha_programada'] = str(r['fecha_programada'])
    conn.close()
    return result

def get_recomendaciones_automaticas():
    """Genera tareas recomendadas basadas en lecturas críticas/alerta"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            l.id as lectura_id,
            l.valor,
            l.estado_alerta,
            s.tipo_sensor,
            s.ubicacion,
            c.id as cultivo_id,
            c.nombre as cultivo_nombre
        FROM lectura_sensor l
        JOIN sensor_agricola s ON l.sensor_id = s.id
        JOIN cultivo c ON s.cultivo_id = c.id
        WHERE l.estado_alerta IN ('alerta', 'critico')
        ORDER BY l.fecha_hora DESC
        LIMIT 20
    """)
    lecturas = cursor.fetchall()
    conn.close()

    recomendaciones = []
    vistos = set()

    for l in lecturas:
        clave = f"{l['cultivo_id']}-{l['tipo_sensor']}"
        if clave in vistos:
            continue
        vistos.add(clave)

        tipo = l['tipo_sensor'].lower()
        rec = None

        if 'humedad' in tipo:
            if l['estado_alerta'] == 'critico':
                rec = {
                    "cultivo_id": l['cultivo_id'],
                    "cultivo_nombre": l['cultivo_nombre'],
                    "tipo_tarea": "Riego",
                    "descripcion": f"Humedad crítica ({l['valor']}) en {l['ubicacion']}. Se recomienda riego urgente.",
                    "prioridad": "alta",
                    "icono": "water_drop",
                    "color": "red"
                }
            else:
                rec = {
                    "cultivo_id": l['cultivo_id'],
                    "cultivo_nombre": l['cultivo_nombre'],
                    "tipo_tarea": "Riego",
                    "descripcion": f"Humedad baja ({l['valor']}) en {l['ubicacion']}. Programar riego preventivo.",
                    "prioridad": "media",
                    "icono": "water_drop",
                    "color": "yellow"
                }
        elif 'ph' in tipo:
            rec = {
                "cultivo_id": l['cultivo_id'],
                "cultivo_nombre": l['cultivo_nombre'],
                "tipo_tarea": "Fertilización",
                "descripcion": f"pH fuera de rango ({l['valor']}) en {l['ubicacion']}. Aplicar corrector de pH.",
                "prioridad": "alta" if l['estado_alerta'] == 'critico' else "media",
                "icono": "science",
                "color": "red" if l['estado_alerta'] == 'critico' else "yellow"
            }
        elif 'temperatura' in tipo:
            rec = {
                "cultivo_id": l['cultivo_id'],
                "cultivo_nombre": l['cultivo_nombre'],
                "tipo_tarea": "Inspección",
                "descripcion": f"Temperatura anormal ({l['valor']}) en {l['ubicacion']}. Revisar condiciones del cultivo.",
                "prioridad": "media",
                "icono": "thermostat",
                "color": "yellow"
            }
        elif 'agua' in tipo:
            rec = {
                "cultivo_id": l['cultivo_id'],
                "cultivo_nombre": l['cultivo_nombre'],
                "tipo_tarea": "Riego",
                "descripcion": f"Nivel de agua crítico ({l['valor']}) en {l['ubicacion']}. Ajustar sistema de riego.",
                "prioridad": "alta",
                "icono": "water",
                "color": "red"
            }

        if rec:
            recomendaciones.append(rec)

    return recomendaciones