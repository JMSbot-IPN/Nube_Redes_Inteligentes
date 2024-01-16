import requests
from faker import Faker

fake = Faker()
imsi = fake.random_int(10000000000000000000, 99999999999999999999)
tmsi = fake.random_int(10000000000000000000, 99999999999999999999)
msisdn = fake.msisdn()
msrn = fake.random_int(10000000000000000000, 99999999999999999999)
lai = fake.random_int(10000000000000000000, 99999999999999999999)
categoria = fake.random_element(elements=('Gama_Alta', 'Gama_Media', 'Gama_Baja'))
param_serv_supl = fake.random_int(10000000000000000000, 99999999999999999999)
caract_tecnicas = fake.random_int(10000000000000000000, 99999999999999999999)

data_to_send = {
    "imsi": imsi,
    "tmsi": tmsi,
    "msisdn": msisdn,
    "msrn": msrn,
    "lai": lai,
    "categoria": categoria,
    "param_serv_supl": param_serv_supl,
    "caract_tecnicas": caract_tecnicas
}

url = "http://localhost:8080/registrar"

response = requests.post(url, json=data_to_send)

print(f"Respuesta del servidor: {response.text}")
