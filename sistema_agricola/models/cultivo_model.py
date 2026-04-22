from database.connection import get_connection
from datetime import datetime

def formatear_fecha(fecha):
    if not fecha:
        return fecha
    try:
        # Si viene en formato HTTP date
        if 'GMT' in str(fecha):
            return datetime.strptime(fecha, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')
        # Si ya viene como date object
        if hasattr(fecha, 'strftime'):
            return fecha.strftime('%Y-%m-%d')
        return str(fecha)[:10]
    except:
        return str(fecha)[:10]

def get_all_cultivos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cultivo")
    result = cursor.fetchall()
    conn.close()
    return result

def get_cultivo_by_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cultivo WHERE id = %s", (id,))
    result = cursor.fetchone()
    # Convertir fecha a string ISO para que Angular la reciba bien
    if result and result.get('fecha_siembra'):
        result['fecha_siembra'] = str(result['fecha_siembra'])
    conn.close()
    return result

def create_cultivo(data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO cultivo (nombre, tipo, area_hectareas, fecha_siembra, estado)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        data["nombre"],
        data["tipo"],
        data["area_hectareas"],
        formatear_fecha(data["fecha_siembra"]),
        data.get("estado", "activo")
    )
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_cultivo(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE cultivo
        SET nombre = %s, tipo = %s, area_hectareas = %s, fecha_siembra = %s, estado = %s
        WHERE id = %s
    """
    values = (
        data["nombre"],
        data["tipo"],
        data["area_hectareas"],
        formatear_fecha(data["fecha_siembra"]),
        data.get("estado", "activo"),
        id
    )
    cursor.execute(sql, values)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

def delete_cultivo(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cultivo WHERE id = %s", (id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected