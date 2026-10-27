from http.server import BaseHTTPRequestHandler
import json
import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        overpass_query = """
        [out:json][timeout:25];
        (
          node["highway"="traffic_signals"](-23.56, -46.66, -23.54, -46.64);
          way["highway"~"primary|secondary"](-23.56, -46.66, -23.54, -46.64);
        );
        out body;
        >;
        out skel qt;
        """

        headers = {
            "User-Agent": "DashboardTransitoVercel/1.0 (suporte@skydatasolution.com)"
        }

        try:
            response = requests.post(
                OVERPASS_URL, 
                data={'data': overpass_query}, 
                headers=headers, 
                timeout=20
            )
            osm_data = response.json()

            elements = osm_data.get("elements", [])
            semaforos = [e for e in elements if e.get("type") == "node"]
            vias = [e for e in elements if e.get("type") == "way"]

            incidentes = [
                {
                    "id": "INC-8812",
                    "tipo": "Semáforo Apagado",
                    "local": "Av. Rebouças x Rua Oscar Freire",
                    "impacto": "ALTO",
                    "status": "EM_ATENDIMENTO"
                },
                {
                    "id": "INC-8813",
                    "tipo": "Lentidão Excessiva",
                    "local": "Av. Paulista (Sentido Consolação)",
                    "impacto": "MÉDIO",
                    "status": "MONITORANDO"
                }
            ]

            payload = {
                "updatedAt": response.headers.get("Date"),
                "status": "online",
                "summary": {
                    "totalSemaforosMapeados": len(semaforos),
                    "totalViasPrincipais": len(vias),
                    "totalIncidentesAtivos": len(incidentes),
                    "origem": "OpenStreetMap / Overpass API"
                },
                "incidentes": incidentes,
                "nodes": semaforos[:50]
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(payload, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            err_msg = {"error": "Falha ao consultar Overpass API", "details": str(e)}
            self.wfile.write(json.dumps(err_msg, ensure_ascii=False).encode('utf-8'))
