import requests

def registrar_hlr(input_imsi):
    imsi = str(input_imsi)
    url = f"http://192.168.100.31:8080/registrar_hlr_cliente?imsi={imsi}"
    response = requests.post(url)
    return response.text

input_imsi = input("Ingrese el IMSI: ")
response = registrar_hlr(input_imsi)
print(response)
