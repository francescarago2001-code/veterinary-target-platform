import csv
import http.server
import os
import socketserver
import smtplib
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import parse_qs

PORT = int(os.environ.get("PORT", 8000))
CANDIDATE_TO_EMAIL = os.environ.get("CANDIDATE_TO_EMAIL", "aetoscorporatefinance@gmail.com")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
CSV_FILE = Path(__file__).with_name("candidature.csv")
CSV_FIELDNAMES = [
    "nome_struttura",
    "anno_apertura",
    "regione",
    "provincia",
    "tipologia",
    "numero_sedi",
    "fatturato",
    "ebitda_margin",
    "capex",
    "ricavi",
    "numero_veterinari",
    "veterinari_dipendenti",
    "veterinari_partita_iva",
    "veterinari_cococo",
    "veterinari_altro",
    "ricavi_fondatore",
    "turnover",
    "staff_cost",
    "h24",
    "diagnostica",
    "diagnostica_altro",
    "superficie",
    "immobile",
    "pazienti_annui",
    "nuovi_pazienti",
    "referral",
    "interesse",
    "permanenza",
    "nome",
    "cognome",
    "email",
    "telefono",
]


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/home.html"
        return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_data = self.rfile.read(content_length) if content_length else b""

        form_values = parse_qs(raw_data.decode("utf-8"), keep_blank_values=True)
        payload = {
            key: ", ".join(values) if len(values) > 1 else values[0] if values else ""
            for key, values in form_values.items()
        }

        save_candidature(payload)
        send_candidate_email(payload)

        self.send_response(303)
        self.send_header("Location", "/grazie.html")
        self.end_headers()


def save_candidature(payload):
    file_exists = CSV_FILE.exists()

    with CSV_FILE.open("a", newline="", encoding="utf-8") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=CSV_FIELDNAMES)
        if not file_exists:
            writer.writeheader()

        row = {field: payload.get(field, "") for field in CSV_FIELDNAMES}
        writer.writerow(row)


def send_candidate_email(payload):
    if not SMTP_USER or not SMTP_PASSWORD:
        return False

    email = EmailMessage()
    email["Subject"] = "Nuova candidatura ricevuta"
    email["From"] = SMTP_USER
    email["To"] = CANDIDATE_TO_EMAIL

    body_lines = ["Nuova candidatura ricevuta.", ""]
    for field in CSV_FIELDNAMES:
        value = payload.get(field, "")
        if value:
            body_lines.append(f"{field}: {value}")

    email.set_content("\n".join(body_lines))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(email)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHandler) as server:
        print(f"Sito attivo su http://localhost:{PORT}")
        server.serve_forever()
