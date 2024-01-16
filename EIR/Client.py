import requests
import random
from faker import Faker

fake = Faker()

host = 'http://192.168.100.30:8080'  # Cambia la URL según tu configuración
guardar_endpoint = '/guardar_eir'
leer_endpoint = '/leer_eir'

opcion = input("Ingrese 'Escribir' o 'Leer': ")

if opcion == 'Escribir':
    imei = fake.random_int(100000000000000, 999999999999999)
    estado = random.choice(['Blanco', 'Gris', 'Negro'])

    data_to_send = {
        "imei": imei,
        "estado": estado
    }

    response = requests.post(f"{host}{guardar_endpoint}", json=data_to_send)
else:
    imei = input("Ingrese IMEI para leer el estado: ")

    response = requests.get(f"{host}{leer_endpoint}/{imei}")

print(f"Respuesta del servidor: {response.text}")
