import hashlib
from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

def obtener_cadena_irrepetible(semilla):
    hasher = hashlib.sha256()
    semilla_str = str(semilla)
    semilla_bytes = semilla_str.encode('utf-8')
    hasher.update(semilla_bytes)
    cadena_irrepetible = hasher.hexdigest()[:20]

    return cadena_irrepetible

def conectar_base_local():
    server = 'DESKTOP-4UD8TQM\CONTROL'
    database = 'AUC'
    username = 'sa'
    password = '1234'

    local_conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    local_conn = pyodbc.connect(local_conn_str)
    local_cursor = local_conn.cursor()

    return local_conn, local_cursor

def cerrar_base_datos(local_conn):
    local_conn.close()

def guardar_datos_auc(imsi, ki):
    rand = obtener_cadena_irrepetible(ki)
    local_conn, local_cursor = conectar_base_local()

    local_cursor.execute('''
        INSERT INTO SIM_AUTH (IMSI, KI, RAND)
        VALUES (?, ?, ?)
    ''', (imsi, ki, rand))

    local_conn.commit()

    cerrar_base_datos(local_conn)

    return "Datos recibidos y almacenados en la base de datos local."

@app.route('/guardar_auc', methods=['POST'])
def api_guardar():
    data = request.get_json()
    imsi = data.get('imsi')
    ki = data.get('ki')

    guardar_datos_auc(imsi, ki)
    return jsonify({"message": "Datos guardados correctamente."})

@app.route('/leer_auc/<imsi>', methods=['GET'])
def api_leer(imsi):
    local_conn, local_cursor = conectar_base_local()

    local_cursor.execute('SELECT KI, RAND FROM SIM_AUTH WHERE IMSI = ?', imsi)
    row = local_cursor.fetchone()
    rand_rec = obtener_cadena_irrepetible(int(row.KI))
    flag = row.RAND == rand_rec

    cerrar_base_datos(local_conn)

    if flag:
        return "Autenticación exitosa", 200
    else:
        return f"Dispositivo no encontrado, \n{row.RAND}\n{row.KI}\n{rand_rec}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
