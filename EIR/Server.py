from flask import Flask, request, jsonify
import pyodbc
import hashlib

app = Flask(__name__)

def obtener_cadena_irrepetible(semilla):
    hasher = hashlib.sha256()
    semilla_str = str(semilla)
    semilla_bytes = semilla_str.encode('utf-8')
    hasher.update(semilla_bytes)
    cadena_irrepetible = hasher.hexdigest()[:20]

    return cadena_irrepetible

def conectar_eir():
    server = 'DESKTOP-4UD8TQM\CONTROL'
    database = 'EIR'
    username = 'sa'
    password = '1234'

    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    return conn, cursor

def cerrar_base_datos(conn):
    conn.close()

def guardar_datos_eir(imei, estado):
    conn, cursor = conectar_eir()

    cursor.execute('''
        INSERT INTO IDENTIDAD (IMEI, ESTADO)
        VALUES (?, ?)
    ''', (imei, estado))

    conn.commit()
    cerrar_base_datos(conn)

def obtener_estado_eir(imei):
    conn, cursor = conectar_eir()

    cursor.execute('SELECT ESTADO FROM IDENTIDAD WHERE IMEI = ?', imei)
    row = cursor.fetchone()

    cerrar_base_datos(conn)

    if row:
        return row.ESTADO
    else:
        return "Dispositivo no encontrado"

def conectar_auc():
    server = 'DESKTOP-4UD8TQM\CONTROL'
    database = 'AUC'
    username = 'sa'
    password = '1234'

    local_conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    local_conn = pyodbc.connect(local_conn_str)
    local_cursor = local_conn.cursor()

    return local_conn, local_cursor

def guardar_datos_auc(imsi, ki):
    rand = obtener_cadena_irrepetible(ki)
    local_conn, local_cursor = conectar_auc()

    local_cursor.execute('''
        INSERT INTO SIM_AUTH (IMSI, KI, RAND)
        VALUES (?, ?, ?)
    ''', (imsi, ki, rand))

    local_conn.commit()

    cerrar_base_datos(local_conn)

    return "Datos recibidos y almacenados en la base de datos local."

@app.route('/guardar_eir', methods=['POST'])
def api_guardar():
    data = request.get_json()
    imei = data.get('imei')
    estado = data.get('estado')

    guardar_datos_eir(imei, estado)
    return jsonify({"message": "Datos guardados correctamente."})

@app.route('/leer_eir/<imei>', methods=['GET'])
def api_leer(imei):
    estado = obtener_estado_eir(imei)
    return jsonify({"estado": estado})

@app.route('/guardar_auc', methods=['POST'])
def api_guardar():
    data = request.get_json()
    imsi = data.get('imsi')
    ki = data.get('ki')

    guardar_datos_auc(imsi, ki)
    return jsonify({"message": "Datos guardados correctamente."})

@app.route('/leer_auc/<imsi>', methods=['GET'])
def api_leer(imsi):
    local_conn, local_cursor = conectar_auc()

    local_cursor.execute('SELECT KI, RAND FROM SIM_AUTH WHERE IMSI = ?', imsi)
    row = local_cursor.fetchone()
    rand_rec = obtener_cadena_irrepetible(int(row.KI))
    flag = row.RAND == rand_rec

    cerrar_base_datos(local_conn)

    if flag:
        return "Autenticación exitosa"
    else:
        return f"Dispositivo no encontrado, \n{row.RAND}\n{row.KI}\n{rand_rec}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)