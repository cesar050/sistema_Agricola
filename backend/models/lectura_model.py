from database.connection import get_connection

def get_all_lecturas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT l.*, s.tipo_sensor, s.ubicacion
        FROM lectura_sensor l
        JOIN sensor_agricola s ON l.sensor_id = s.id
    """)
    result = cursor.fetchall()
    conn.close()
    return result

def get_lectura_by_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT l.*, s.tipo_sensor, s.ubicacion
        FROM lectura_sensor l
        JOIN sensor_agricola s ON l.sensor_id = s.id
        WHERE l.id = %s
    """, (id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_lecturas_by_sensor(sensor_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lectura_sensor WHERE sensor_id = %s ORDER BY fecha_hora DESC", (sensor_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def create_lectura(data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO lectura_sensor (sensor_id, valor, estado_alerta)
        VALUES (%s, %s, %s)
    """
    values = (
        data["sensor_id"],
        data["valor"],
        data.get("estado_alerta", "normal")
    )
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_lectura(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE lectura_sensor
        SET sensor_id = %s, valor = %s, estado_alerta = %s
        WHERE id = %s
    """
    values = (
        data["sensor_id"],
        data["valor"],
        data.get("estado_alerta", "normal"),
        id
    )
    cursor.execute(sql, values)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

def delete_lectura(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lectura_sensor WHERE id = %s", (id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected