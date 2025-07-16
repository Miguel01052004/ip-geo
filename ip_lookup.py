import requests
import json

def consultar_ip(ip):
    url = f"http://ip-api.com/json/{ip}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return {
            "IP": ip,
            "País": datos.get("country"),
            "Región": datos.get("regionName"),
            "ISP": datos.get("isp"),
            "Latitud": datos.get("lat"),
            "Longitud": datos.get("lon")
        }
    else:
        return {"IP": ip, "Error": "No se pudo consultar"}

resultados = []

while True:
    ip = input("Introduce una IP pública (o escribe 'exit' para salir): ")
    if ip.lower() == "exit":
        break
    resultado = consultar_ip(ip)
    print(resultado)
    resultados.append(resultado)

with open("resultados.json", "w") as archivo:
    json.dump(resultados, archivo, indent=4)

print("Resultados guardados en resultados.json")

