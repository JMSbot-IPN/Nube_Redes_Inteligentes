import requests
import random
from faker import Faker

fake = Faker()

host = 'http://192.168.100.30:8080'
guardar_endpoint = '/guardar_auc'
leer_endpoint = '/leer_auc'

opcion = input("Ingrese 'Escribir' o 'Leer': ")

if opcion == 'Escribir':
    imsi = fake.random_int(100000000000000, 999999999999999)
    ki = fake.random_int(100000000000000, 999999999999999)

    data_to_send = {
        "imsi": imsi,
        "ki": ki
    }

    response = requests.post(f"{host}{guardar_endpoint}", json=data_to_send)
else:
    imsi = input("Ingrese IMSI para leer el estado: ")

    response = requests.get(f"{host}{leer_endpoint}/{imsi}")

print(f"Respuesta del servidor: {response.text}")