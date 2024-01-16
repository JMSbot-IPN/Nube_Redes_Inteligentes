from flask import Flask, request
import pyodbc

app = Flask(__name__)

def conectar_base_local():
    server = 'DESKTOP-1SRCFQT\Chuy'
    database = 'EIR'
    username = 'sa'
    password = '1234'

    local_conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    local_conn = pyodbc.connect(local_conn_str)
    local_cursor = local_conn.cursor()

    return local_conn, local_cursor

def cerrar_base_local(local_conn):
    local_conn.close()

def registrar_datos(data):
    data_list = data.split(',')

    local_conn, local_cursor = conectar_base_local()

    local_cursor.execute('''
        INSERT INTO INFO_REQ_HLR (IMSI, TMSI, MSISDN, MSRN, LAI, CATEGORIA, PARAM_SERV_SUPL, CARACT_TECNICAS)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(data_list))

    local_conn.commit()

    cerrar_base_local(local_conn)

    return "Datos recibidos y almacenados en la base de datos local."

@app.route('/registrar_vlr', methods=['POST'])
def api_registrar():
    data = request.data.decode('utf-8')
    response = registrar_datos(data)
    return response

@app.route('/buscar_vlr', methods=['GET'])
def api_buscar():
    imsi = request.args.get('imsi')
    local_conn, local_cursor = conectar_base_local()

    local_cursor.execute('''
        SELECT * FROM INFO_REQ_HLR WHERE IMSI = ?
    ''', (imsi))

    data = local_cursor.fetchall()

    cerrar_base_local(local_conn)

    return str(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)