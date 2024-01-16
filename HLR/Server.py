from flask import Flask, request
import requests
import random
from faker import Faker
import pyodbc
from time import sleep

app = Flask(__name__)
fake = Faker()

def conectar_base_local_hlr():
    server = 'DESKTOP-BDK7KBA\REGISTROS'
    database = 'HLR'
    username = 'sa'
    password = '1234'

    local_conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    local_conn = pyodbc.connect(local_conn_str)
    local_cursor = local_conn.cursor()

    return local_conn, local_cursor

def conectar_base_local_vlr():
    server = 'DESKTOP-BDK7KBA\REGISTROS'
    database = 'VLR'
    username = 'sa'
    password = '1234'

    local_conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    local_conn = pyodbc.connect(local_conn_str)
    local_cursor = local_conn.cursor()

    return local_conn, local_cursor

def cerrar_base_local(local_conn):
    local_conn.close()

def registrar_datos_hlr(data):
    data_list = data.split(',')

    local_conn, local_cursor = conectar_base_local_hlr()

    local_cursor.execute('''
        INSERT INTO DATOS_DISP (IMSI, TMSI, MSISDN, MSRN, LAI, CATEGORIA, PARAM_SERV_SUPL, CARACT_TECNICAS, MNC, KI, IMEI)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(data_list))

    local_conn.commit()

    cerrar_base_local(local_conn)

    return "Datos recibidos y almacenados en la base de datos local."

def registrar_datos_vlr(data):
    data_list = data.split(',')

    local_conn, local_cursor = conectar_base_local_vlr()

    local_cursor.execute('''
        INSERT INTO INFO_REQ_HLR (IMSI, TMSI, MSISDN, MSRN, LAI, CATEGORIA, PARAM_SERV_SUPL, CARACT_TECNICAS)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(data_list))

    local_conn.commit()

    cerrar_base_local(local_conn)

def registrar_datos_eir(imei):
    imei = imei
    estado = random.choice(['Blanco', 'Gris', 'Negro'])
    data_to_send = {
        "imei": imei,
        "estado": estado
    }

    requests.post("http://192.168.100.30:8080/guardar_eir", json=data_to_send)

def leer_datos_eir(imei):

    requests.get(f"http://192.168.100.30:8080/leer_eir/{imei}")

def registrar_datos_auc(imsi, ki):
    
    data_to_send = {
        "imsi": imsi,
        "ki": ki
    }

    requests.post("http://192.168.100.30:8080/guardar_auc", json=data_to_send)

def leer_datos_auc(imsi):
    response = requests.get(f"http://192.168.100.30:8080/leer_auc/{imsi}")
    if response.status_code == 200:
        return "Success"
    else:
        return "Fail"

def leer_compañia(imsi):
    local_conn, local_cursor = conectar_base_local_hlr()
    local_cursor.execute('''
        SELECT * FROM DATOS_DISP WHERE IMSI = ? AND MNC = '020'
    ''', (imsi))

    data = local_cursor.fetchall()
    print(data)

    cerrar_base_local(local_conn)

    if data:
        return "Success"
    else:
        return "Fail"
    


def buscar_conexion(imsi):

    return

@app.route('/registrar', methods=['POST'])
def api_registrar():
    imsi = request.args.get('imsi')
    tmsi = fake.random_int(10000000, 99999999)
    msisdn = fake.random_int(10000000, 99999999)
    msrn = fake.random_int(10000000, 99999999)
    lai = fake.random_int(10000000, 99999999)
    categoria = fake.random_element(elements=('Alta', 'Media', 'Baja'))
    param_serv_supl = fake.random_int(10000000, 99999999)
    caract_tecnicas = fake.random_int(10000000, 99999999)
    mnc = fake.random_element(elements=('020', '03', '050', '090', '140'))
    ki = fake.random_int(10000000, 99999999)
    imei = fake.random_int(10000000, 99999999)
    data_hlr = f"{imsi},{tmsi},{msisdn},{msrn},{lai},{categoria},{param_serv_supl},{caract_tecnicas},{mnc},{ki},{imei}"
    data_vlr = f"{imsi},{tmsi},{msisdn},{msrn},{lai},{categoria},{param_serv_supl},{caract_tecnicas}"
    


    response = registrar_datos_hlr(data_hlr)
    registrar_datos_vlr(data_vlr)
    registrar_datos_eir(imei)
    registrar_datos_auc(imsi, ki)

    return response

@app.route('/buscar', methods=['GET'])
def api_buscar():
    imsi = request.args.get('imsi')
    compañia = leer_compañia(imsi)
    datos = leer_datos_auc(imsi)
    if compañia == "Success":
        if datos == "Success":
            return "Acceso concedido", 200
    else:
        return "Acceso denegado", 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
