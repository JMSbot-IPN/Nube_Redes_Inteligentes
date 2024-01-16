from flask import Flask, render_template, jsonify, request
import requests
from faker import Faker

fake = Faker()
app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/registrar')
def registrar():
    return render_template('registrar.html')

@app.route('/buscar')
def buscar():
    return render_template('buscar.html')

@app.route('/registrar_cliente', methods=['GET', 'POST'])
def registrar_hlr():
    if request.method == 'POST':
        imsi = request.form.get('imsi')
        url = f"http://192.168.100.31:8080/registrar?imsi={imsi}"
        response = requests.post(url)
        if response.status_code == 200:
            return render_template('result.html', response=response.text)
    return render_template('error.html')

@app.route('/buscar_cliente', methods=['GET', 'POST'])
def buscar_hlr():
    if request.method == 'POST':
        imsi = request.form.get('imsi')
        url = f"http://192.168.100.31:8080//buscar?imsi={imsi}"
        response = requests.get(url)
        if response.status_code == 200:
            return render_template('result.html', response=response.text)
        else:
            return render_template('sin_conexion.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
