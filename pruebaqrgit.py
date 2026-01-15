from flask import Flask, redirect, request, jsonify, Response
import requests
from requests.auth import HTTPDigestAuth
import urllib3

# ====== CONFIG ======
HIK_PROTO = "https"
HIK_IP    = "192.168.107.6"
USER      = "admin"
PWD       = "HVKM853@UYT"
TIMEOUT   = 10
VERIFY_TLS = False  # self-signed -> False

# (Opcional) suprime warnings SSL si VERIFY_TLS=False
if not VERIFY_TLS:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

def hik_url(path):
    return f"{HIK_PROTO}://{HIK_IP}{path}"

def passthrough(resp):
    return Response(resp.content, status=resp.status_code,
        headers={"Content-Type": resp.headers.get("Content-Type","application/json")})

@app.route("/qr")
def generar_qr():
    data = request.args.get("data")

    if not data or not data.isdigit():
        return "Código inválido", 400

    A = 937
    B = 12891
    
    original = int(data)

    ofuscado = (original * A) + B

    # # Redirigir al generador de QR con el número ofuscado
    # qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={ofuscado}"
    # return redirect(qr_url)

    # Generar QR con el número ofuscado
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={ofuscado}"

    # Descargar la imagen del QR
    qr_response = requests.get(qr_url)

    # Devolver la imagen directamente (SIN redirect, SIN HTML)
    return Response(qr_response.content, content_type="image/png")

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(host="0.0.0.0", port=5000)


