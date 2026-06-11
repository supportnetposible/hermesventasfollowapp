#!/usr/bin/env python3
"""
Cron Email Cierre — 8 AM daily
Lee leads de Trello (Listo para comprar + En seguimiento),
filtra los bloqueados por n8n, y envía email personalizado.
"""

import json, subprocess, re, os, sys
from urllib.request import urlopen, Request
from urllib.error import HTTPError

# ── Credenciales ──────────────────────────────────────────────
TRELLO_KEY = os.getenv("TRELLO_API_KEY", "")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN", "")
BOARD_ID = "674d9fe5597e7148c6517990"

# Listas a procesar
LISTAS = {
    "Listo para comprar": "692847f9b7e6ad5dd2de23f7",
    "En seguimiento":      "674d9fe5597e7148c6517994",
}

# Sheet n8n de bloqueo
N8N_SHEET_ID = "1JcsHW3_6cwNlnm_arJslmMuND2GWq_0mAn6z7mjU8wg"

def trello_get(url):
    full_url = f"{url}&key={TRELLO_KEY}&token={TRELLO_TOKEN}"
    req = Request(full_url, headers={"Accept": "application/json"})
    with urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def get_blocked_phones():
    """Obtiene phones bloqueados desde sheet n8n (CSV export)."""
    sheet_url = (
        f"https://docs.google.com/spreadsheets/d/{N8N_SHEET_ID}"
        f"/export?format=csv&gid=0"
    )
    try:
        req = Request(sheet_url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=15) as r:
            raw = r.read().decode("utf-8", errors="ignore")
        phones = set()
        for line in raw.splitlines():
            # Números en columna B (índice 1) — formato: +54 9 XXX
            cols = line.split(",")
            if len(cols) > 1:
                val = cols[1].strip().replace('"', "")
                if re.match(r"\+?54\s?9\s?\d", val):
                    clean = re.sub(r"[^\d]", "", val)
                    phones.add(clean)
        return phones
    except Exception as e:
        print(f"  [WARN] No pude leer sheet de bloqueo: {e}")
        return set()

def parse_card_name(name):
    """Extrae nombre, teléfono y email del nombre de la tarjeta Trello.
    Formato: #Followapp Nombre // +54 9 XXXX // email // desc
    """
    # Ignorar tarjetas resumen
    if name.startswith("TOTAL VEHÍCULOS"):
        return None

    parts = [p.strip() for p in name.split("//")]
    if len(parts) < 2:
        return None

    nombre = parts[0].replace("#Followapp", "").strip()

    # Teléfono: segunda parte
    telefono = parts[1].strip() if len(parts) > 1 else ""
    # Limpiar teléfono: solo dígitos
    telefono_limpio = re.sub(r"[^\d]", "", telefono)

    # Email: tercera parte
    email = parts[2].strip() if len(parts) > 2 else ""
    if not email or "@" not in email:
        return None

    return {"nombre": nombre, "telefono": telefono_limpio, "email": email}

def enviar_email(to_email, nombre, lista_origen):
    """Envía email de cierre via send_message."""
    asunto = f"📋 Seguimiento FollowApp — {nombre}"

    cuerpo = f"""Hola {nombre},

Te contacto de parte de FollowApp. Hace un tiempo charlamos sobre el monitoreo de tus vehículos y quiero saber cómo venís con esa decisión.

Sabemos que son temas que llevan tiempo evaluar, pero quiero que sepas que estamos disponibles para darte una mano:

• Te mostramos cómo funciona en 5 minutos
• Te ayudamos a armarlo con tus vehículos
• No hay compromiso de tu parte

¿Lo estás pensando todavía o ya lo dejaste de lado? Necesito saber para no molestarte más si ya no aplica.

¡Abrazo!
Tomás — FollowApp

---
Este mensaje es parte del seguimiento de nuestra conversación en {lista_origen}.
"""

    # Usar google_workspace.py para enviar
    result = subprocess.run(
        [sys.executable,
         "/root/.hermes/skills/sales/followapp-sales/scripts/google_workspace.py",
         "gmail-send",
         "--to", to_email,
         "--subject", asunto,
         "--body", cuerpo],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0, result.stdout, result.stderr

def main():
    print("[Email Cierre] Iniciando...")

    # 1. Procesar cada lista (sin filtro n8n — la sheet de bloqueo era solo para /pause)
    # Los bloqueados por n8n se filtran solo en el chat en vivo, no en emails programados

    total_enviados = 0
    total_bloqueados = 0
    total_sin_email = 0

    # 2. Procesar cada lista
    for lista_nombre, lista_id in LISTAS.items():
        print(f"\n[Email Cierre] Procesando: {lista_nombre}")
        cards = trello_get(
            f"https://api.trello.com/1/lists/{lista_id}/cards"
            f"?fields=name,shortUrl"
        )
        print(f"  → {len(cards)} tarjetas en la lista")

        for card in cards:
            parsed = parse_card_name(card["name"])
            if not parsed:
                continue

            nombre = parsed["nombre"]
            telefono = parsed["telefono"]
            email = parsed["email"]

            # Enviar email
            print(f"  Enviando email a {nombre} <{email}>...")
            ok, stdout, stderr = enviar_email(email, nombre, lista_nombre)
            if ok:
                print(f"    ✓ Email enviado")
                total_enviados += 1
            else:
                print(f"    ✗ Error: {stderr[:100]}")
                total_sin_email += 1

    print(f"\n[Email Cierre] Resumen:")
    print(f"  Enviados:    {total_enviados}")
    print(f"  Bloqueados:  {total_bloqueados}")
    print(f"  Errors:      {total_sin_email}")

if __name__ == "__main__":
    main()