from database.connection import get_connection

def get_all_sensores():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*, c.nombre AS cultivo_nombre
        FROM sensor_agricola s
        JOIN cultivo c ON s.cultivo_id = c.id
    """)
    result = cursor.fetchall()
    conn.close()
    return result

def get_sensor_by_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*, c.nombre AS cultivo_nombre
        FROM sensor_agricola s
        JOIN cultivo c ON s.cultivo_id = c.id
        WHERE s.id = %s
    """, (id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_sensores_by_cultivo(cultivo_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sensor_agricola WHERE cultivo_id = %s", (cultivo_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def create_sensor(data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO sensor_agricola (cultivo_id, tipo_sensor, ubicacion)
        VALUES (%s, %s, %s)
    """
    values = (
        data["cultivo_id"],
        data["tipo_sensor"],
        data.get("ubicacion", None)
    )
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_sensor(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE sensor_agricola
        SET cultivo_id = %s, tipo_sensor = %s, ubicacion = %s
        WHERE id = %s
    """
    values = (
        data["cultivo_id"],
        data["tipo_sensor"],
        data.get("ubicacion", None),
        id
    )
    cursor.execute(sql, values)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

def delete_sensor(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sensor_agricola WHERE id = %s", (id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected