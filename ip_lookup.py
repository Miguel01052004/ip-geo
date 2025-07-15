import json, sys
from pathlib import Path
import requests

API_URL = "http://ip-api.com/json/"
OUT_FILE = Path("ip_results.json")

def consultar_ip(ip: str) -> dict:
    try:
        r = requests.get(f"{API_URL}{ip}", timeout=5)
        data = r.json()
        if data["status"] != "success":
            raise ValueError(data.get("message", "Error desconocido"))
        return {
            "ip": data["query"],
            "pais": data["country"],
            "region": data["regionName"],
            "isp": data["isp"],
            "lat": data["lat"],
            "lon": data["lon"],
        }
    except Exception as e:
        print(f"❌  No se pudo consultar {ip}: {e}")
        return {}

def guardar(resultado: dict):
    resultados = []
    if OUT_FILE.exists():
        try:
            resultados = json.loads(OUT_FILE.read_text())
        except json.JSONDecodeError:
            pass
    resultados.append(resultado)
    OUT_FILE.write_text(json.dumps(resultados, indent=2, ensure_ascii=False))

def main():
    print("Escribe una IP pública (o 'exit' para salir):")
    while True:
        ip = input(">> ").strip()
        if ip.lower() == "exit":
            print("Programa finalizado.")
            break
        if not ip:
            continue
        res = consultar_ip(ip)
        if res:
            print(f"🌎  {res['ip']:15}  {res['pais']}, {res['region']}  |  ISP: {res['isp']}  |  ({res['lat']}, {res['lon']})")
            guardar(res)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
