#!/usr/bin/env python3
"""
Webapp: Der Bienenladen – Exklusiver Händler von Honig-Kiste.de
Inklusive vollständigem Produktkatalog, interaktivem Honigautomaten-Konfigurator
und Zahlung über Mollie (Mollie API v2 + interaktiver Mollie Checkout Simulator).
"""

import json
import mimetypes
import os
import sqlite3
import urllib.parse
import uuid
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from catalog_data import (
    CONFIGURATOR_OPTIONS,
    DEALER_INFO,
    FAQ_ITEMS,
    PRODUCTS,
    RAL_COLORS,
)
from mollie_service import MOLLIE_METHODS, MollieService

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DB_PATH = BASE_DIR / "honigautomat.db"

mollie_service = MollieService()


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS configurations (
            config_code TEXT PRIMARY KEY,
            config_json TEXT NOT NULL,
            summary_title TEXT NOT NULL,
            total_eur REAL NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            order_number TEXT NOT NULL,
            customer_json TEXT NOT NULL,
            items_json TEXT NOT NULL,
            subtotal_eur REAL NOT NULL,
            shipping_eur REAL NOT NULL,
            total_eur REAL NOT NULL,
            vat_eur REAL NOT NULL,
            payment_method TEXT NOT NULL,
            payment_id TEXT NOT NULL,
            payment_status TEXT NOT NULL,
            payment_provider TEXT NOT NULL,
            checkout_url TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def calculate_configuration(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validiert eine Honigautomaten-Konfiguration und berechnet alle Einzelpositionen,
    Abmessungen, Gesamtgewicht, Fächeranzahl und Endpreis (inkl. MwSt.).
    """
    model_id = config.get("model_id", "automat-10")
    depth_id = str(config.get("depth_id", "240"))
    if depth_id not in ("180", "240"):
        depth_id = "240"

    base_models = {m["id"]: m for m in CONFIGURATOR_OPTIONS["base_models"]}
    base_model = base_models.get(model_id, base_models["automat-10"])

    ext_id = config.get("extension_id", "ext-0")
    extensions = {e["id"]: e for e in CONFIGURATOR_OPTIONS["extensions"]}
    extension = extensions.get(ext_id, extensions["ext-0"])

    door_id = config.get("door_design_id", "classic-bee")
    doors = {d["id"]: d for d in CONFIGURATOR_OPTIONS["door_designs"]}
    door = doors.get(door_id, doors["classic-bee"])

    ral_map = {c["code"]: c for c in RAL_COLORS}
    body_color_code = config.get("body_color", "RAL 1021")
    roof_color_code = config.get("roof_color", "RAL 9005")
    body_color = ral_map.get(body_color_code, ral_map["RAL 1021"])
    roof_color = ral_map.get(roof_color_code, ral_map["RAL 9005"])

    selected_payment_ids = config.get("payment_addons", [])
    if not isinstance(selected_payment_ids, list):
        selected_payment_ids = []

    selected_power_ids = config.get("power_addons", [])
    if not isinstance(selected_power_ids, list):
        selected_power_ids = []

    shipping_id = config.get("shipping_id", "pickup-bienenladen")
    shippings = {s["id"]: s for s in CONFIGURATOR_OPTIONS["shipping_options"]}
    shipping = shippings.get(shipping_id, shippings["pickup-bienenladen"])

    custom_engraving_text = str(config.get("custom_engraving_text", "")).strip()[:60]
    sms_phone_number = str(config.get("sms_phone_number", "")).strip()[:30]
    customer_notes = str(config.get("customer_notes", "")).strip()[:300]

    line_items: List[Dict[str, Any]] = []

    base_price = float(base_model["prices_by_depth"][depth_id])
    line_items.append(
        {
            "label": f"{base_model['name']} – {depth_id} mm Fachtiefe",
            "detail": f"Serienmäßig mit 5-Kanal-Münzprüfer (0,10 €–2,00 €), Zahlenfeld, 230V-Netzteil, 12V Powersafe & Gen. 3 Web-Konfiguration ({base_model['dimensions']})",
            "price": round(base_price, 2),
        }
    )

    ext_price = float(extension["prices_by_depth"][depth_id])
    if extension["count"] > 0:
        line_items.append(
            {
                "label": f"{extension['name']} ({depth_id} mm Fachtiefe)",
                "detail": "Komplett montiert inkl. Master-Slave-Verbindungskabel, angesteuert über Hauptautomat",
                "price": round(ext_price, 2),
            }
        )

    line_items.append(
        {
            "label": f"Farbgestaltung: Gehäuse {body_color['name']} ({body_color['code']}) / Dach {roof_color['name']} ({roof_color['code']})",
            "detail": "Elo-verzinktes Stahlblech, 2-farbig hochwertig nach RAL pulverbeschichtet (ohne Aufpreis)",
            "price": 0.00,
        }
    )

    door_detail = door["description"]
    if door["id"] == "custom-logo" and custom_engraving_text:
        door_detail += f" | Wunschgravur: „{custom_engraving_text}“"
    line_items.append(
        {
            "label": f"Acrylglastüren (5 mm): {door['name']}",
            "detail": door_detail,
            "price": round(float(door["price"]), 2),
        }
    )

    pay_map = {p["id"]: p for p in CONFIGURATOR_OPTIONS["payment_addons"]}
    for pid in selected_payment_ids:
        if pid in pay_map:
            addon = pay_map[pid]
            line_items.append(
                {
                    "label": addon["name"],
                    "detail": f"Art.-Nr. {addon['sku']} – {addon['description']}",
                    "price": round(float(addon["price"]), 2),
                }
            )

    pow_map = {p["id"]: p for p in CONFIGURATOR_OPTIONS["power_telemetry_addons"]}
    for pid in selected_power_ids:
        if pid in pow_map:
            addon = pow_map[pid]
            detail = f"Art.-Nr. {addon['sku']} – {addon['description']}"
            if pid == "sim-sms-modul" and sms_phone_number:
                detail += f" | Programmierte Ziel-Rufnummer: {sms_phone_number}"
            line_items.append(
                {
                    "label": addon["name"],
                    "detail": detail,
                    "price": round(float(addon["price"]), 2),
                }
            )

    selected_service_ids = config.get("service_addons", [])
    if not isinstance(selected_service_ids, list):
        selected_service_ids = []
    # Each service can be charged at most once per configured machine.
    for service in CONFIGURATOR_OPTIONS["service_addons"]:
        if service["id"] in selected_service_ids:
            line_items.append({
                "label": service["name"],
                "detail": service["description"],
                "price": round(float(service["price"]), 2),
            })

    subtotal = round(sum(item["price"] for item in line_items), 2)
    shipping_price = round(float(shipping["price"]), 2)
    total = round(subtotal + shipping_price, 2)
    vat_amount = round(total - (total / 1.20), 2)

    total_compartments = int(base_model["compartments"]) + int(extension["extra_compartments"])
    total_width_cm = round(
        (40.6 if base_model["compartments"] == 5 else (56.4 if base_model["compartments"] == 10 else 69.3))
        + (extension["count"] * 69.3),
        1,
    )
    total_weight_kg = round(float(base_model["weight_kg"]) + (extension["count"] * 38.0), 1)

    summary_title = (
        f"Honig-Kiste Automat ({total_compartments} Fächer, {depth_id} mm, "
        f"Gehäuse {body_color['code']} / Dach {roof_color['code']})"
    )

    return {
        "summary_title": summary_title,
        "base_model": base_model,
        "depth_id": depth_id,
        "extension": extension,
        "body_color": body_color,
        "roof_color": roof_color,
        "door": door,
        "custom_engraving_text": custom_engraving_text,
        "sms_phone_number": sms_phone_number,
        "customer_notes": customer_notes,
        "shipping": shipping,
        "total_compartments": total_compartments,
        "total_width_cm": total_width_cm,
        "height_cm": 93.1,
        "total_weight_kg": total_weight_kg,
        "line_items": line_items,
        "subtotal_eur": subtotal,
        "shipping_eur": shipping_price,
        "total_eur": total,
        "vat_eur": vat_amount,
    }


def render_mollie_simulator_html(order: Dict[str, Any]) -> str:
    """
    Rendert eine authentische, interaktive Mollie Hosted Checkout Seite
    für lokale Tests ohne externen API-Schlüssel.
    """
    payment_id = order["payment_id"]
    order_id = order["order_id"]
    order_number = order["order_number"]
    amount = f"{order['total_eur']:.2f}".replace(".", ",")
    method = order["payment_method"]
    customer = json.loads(order["customer_json"])
    method_labels = {m["id"]: m["name"] for m in MOLLIE_METHODS}
    method_name = method_labels.get(method, method.upper())

    eps_banks_html = ""
    if method == "eps":
        eps_banks_html = """
        <div class="field">
            <label>Wähle deine österreichische Bank (eps-Überweisung):</label>
            <select id="bank-select">
                <option value="erste">Erste Bank und Sparkassen (George)</option>
                <option value="raiffeisen">Raiffeisen Meine ELBA</option>
                <option value="bawag">BAWAG P.S.K.</option>
                <option value="bankaustria">UniCredit Bank Austria</option>
                <option value="volksbank">Volksbank Österreich</option>
                <option value="easybank">easybank</option>
            </select>
        </div>
        """
    elif method == "klarna":
        eps_banks_html = """
        <div class="field">
            <label>Klarna Zahlungsoption:</label>
            <select id="bank-select">
                <option value="invoice">Rechnung – Zahlbar innerhalb von 30 Tagen nach Lieferung</option>
                <option value="installments">Ratenkauf – 12 Monatsraten über Klarna</option>
                <option value="paynow">Sofort bezahlen per Lastschrift / Überweisung</option>
            </select>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Mollie Checkout – {order_number} | Der Bienenladen</title>
    <style>
        :root {{
            --bg: #f4f6f9;
            --card: #ffffff;
            --text: #111827;
            --muted: #6b7280;
            --accent: #0077ff;
            --success: #059669;
            --honey: #f59e0b;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }}
        .checkout-shell {{
            width: 100%;
            max-width: 540px;
            background: var(--card);
            border-radius: 20px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.4);
            overflow: hidden;
        }}
        .merchant-bar {{
            background: #141619;
            color: #fff;
            padding: 20px 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 3px solid #f6b600;
        }}
        .merchant-brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .merchant-badge {{
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: #f6b600;
            color: #141619;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }}
        .mollie-pill {{
            background: rgba(255,255,255,0.12);
            padding: 5px 12px;
            border-radius: 999px;
            font-size: 12px;
            letter-spacing: 0.04em;
        }}
        .content {{
            padding: 28px;
        }}
        .amount-box {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 18px 20px;
            margin-bottom: 22px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .amount-value {{
            font-size: 28px;
            font-weight: 800;
            color: #0f172a;
        }}
        .meta-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 20px;
            font-size: 13px;
        }}
        .meta-item {{
            background: #f9fafb;
            padding: 10px 12px;
            border-radius: 10px;
            border: 1px solid #e5e7eb;
        }}
        .meta-item span {{
            display: block;
            color: var(--muted);
            font-size: 11px;
            margin-bottom: 3px;
        }}
        .field {{
            margin-bottom: 20px;
        }}
        .field label {{
            display: block;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .field select {{
            width: 100%;
            padding: 12px 14px;
            border-radius: 10px;
            border: 1px solid #cbd5e1;
            font-size: 14px;
            background: #fff;
        }}
        .status-choices {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 16px;
        }}
        .btn {{
            border: none;
            border-radius: 12px;
            padding: 14px 18px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: transform 0.12s ease, opacity 0.12s ease;
        }}
        .btn:hover {{ transform: translateY(-1px); }}
        .btn-pay {{
            background: #059669;
            color: #fff;
            box-shadow: 0 6px 18px rgba(5, 150, 105, 0.3);
        }}
        .btn-open {{
            background: #eff6ff;
            color: #1d4ed8;
            border: 1px solid #bfdbfe;
        }}
        .btn-cancel {{
            background: #fef2f2;
            color: #b91c1c;
            border: 1px solid #fecaca;
        }}
        .footer-note {{
            margin-top: 22px;
            padding-top: 16px;
            border-top: 1px solid #e5e7eb;
            font-size: 12px;
            color: var(--muted);
            text-align: center;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div class="checkout-shell">
        <div class="merchant-bar">
            <div class="merchant-brand">
                <div class="merchant-badge">🐝</div>
                <div>
                    <div style="font-weight:700;font-size:15px;">Der Bienenladen × Honig-Kiste.de</div>
                    <div style="font-size:12px;color:#cbd5e1;">Offizieller Exklusiv-Händler Checkout</div>
                </div>
            </div>
            <div class="mollie-pill">mollie payment</div>
        </div>
        <div class="content">
            <div class="amount-box">
                <div>
                    <div style="font-size:12px;color:#64748b;font-weight:600;">GESAMTBETRAG INKL. MWST.</div>
                    <div style="font-size:13px;color:#334155;margin-top:2px;">Bestellung <strong>{order_number}</strong></div>
                </div>
                <div class="amount-value">{amount} €</div>
            </div>

            <div class="meta-grid">
                <div class="meta-item">
                    <span>Gewählte Zahlungsart</span>
                    <strong>{method_name}</strong>
                </div>
                <div class="meta-item">
                    <span>Mollie Transaktions-ID</span>
                    <strong><code>{payment_id}</code></strong>
                </div>
                <div class="meta-item">
                    <span>Kunde / Imkerei</span>
                    <strong>{customer.get("name", "")}</strong>
                </div>
                <div class="meta-item">
                    <span>E-Mail-Bestätigung</span>
                    <strong>{customer.get("email", "")}</strong>
                </div>
            </div>

            {eps_banks_html}

            <div style="font-size:13px;font-weight:600;color:#334155;margin-bottom:8px;">
                Zahlung autorisieren (Mollie Hosted Checkout):
            </div>
            <div class="status-choices">
                <button class="btn btn-pay" onclick="completePayment('paid')">
                    ✓ Zahlung von {amount} € jetzt erfolgreich autorisieren (paid)
                </button>
                <button class="btn btn-open" onclick="completePayment('open')">
                    ⏳ Zahlung als „Offen / Banküberweisung unterwegs“ markieren (open)
                </button>
                <button class="btn btn-cancel" onclick="completePayment('canceled')">
                    ✕ Zahlungsvorgang abbrechen (canceled)
                </button>
            </div>

            <div class="footer-note">
                🔒 Sichere 256-Bit-SSL-Abwicklung über die Mollie Payments Schnittstelle.<br/>
                Nach Abschluss ruft Mollie automatisch den Webhook <code>/api/mollie/webhook</code> auf und leitet dich zurück zum Bienenladen.
            </div>
        </div>
    </div>

    <script>
        async function completePayment(status) {{
            try {{
                await fetch('/api/mollie/webhook', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        id: '{payment_id}',
                        order_id: '{order_id}',
                        status: status
                    }})
                }});
            }} catch (e) {{
                console.error(e);
            }}
            window.location.href = '/?order={order_id}';
        }}
    </script>
</body>
</html>"""


class HonigautomatRequestHandler(BaseHTTPRequestHandler):
    server_version = "BienenladenHonigKiste/3.0"

    def _send_json(self, data: Any, status: int = 200) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _send_html(self, html: str, status: int = 200) -> None:
        raw = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_body_json(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        content_type = self.headers.get("Content-Type", "")
        if "application/x-www-form-urlencoded" in content_type:
            parsed = urllib.parse.parse_qs(raw)
            return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}

    def _base_url(self) -> str:
        host = self.headers.get("Host", "localhost:8000")
        proto = self.headers.get("X-Forwarded-Proto", "http")
        return f"{proto}://{host}"

    def do_GET(self) -> None:
        parsed = urllib.parse.urlsplit(self.path)
        path = parsed.path

        if path == "/api/catalog":
            self._send_json(
                {
                    "dealer": DEALER_INFO,
                    "products": PRODUCTS,
                    "configurator": CONFIGURATOR_OPTIONS,
                    "ral_colors": RAL_COLORS,
                    "mollie_methods": MOLLIE_METHODS,
                    "mollie_status": mollie_service.get_mode_info(),
                    "faq": FAQ_ITEMS,
                }
            )
            return

        if path == "/api/mollie/settings":
            self._send_json(mollie_service.get_mode_info())
            return

        if path.startswith("/api/configurator/"):
            code = path.split("/api/configurator/", 1)[1].strip()
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM configurations WHERE config_code = ?", (code,))
            row = cur.fetchone()
            conn.close()
            if not row:
                self._send_json({"error": "Konfiguration nicht gefunden."}, status=404)
                return
            cfg = json.loads(row["config_json"])
            self._send_json(
                {
                    "config_code": row["config_code"],
                    "config": cfg,
                    "calculation": calculate_configuration(cfg),
                    "created_at": row["created_at"],
                }
            )
            return

        if path == "/api/orders":
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders ORDER BY created_at DESC LIMIT 25")
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            for r in rows:
                r["customer"] = json.loads(r.pop("customer_json", "{}"))
                r["items"] = json.loads(r.pop("items_json", "[]"))
            self._send_json({"orders": rows})
            return

        if path.startswith("/api/orders/"):
            order_id = path.split("/api/orders/", 1)[1].strip()
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
            row = cur.fetchone()
            if not row:
                conn.close()
                self._send_json({"error": "Bestellung nicht gefunden."}, status=404)
                return

            order_dict = dict(row)
            # Wenn echte Mollie-Zahlung vorliegt, Status live aktualisieren
            remote = mollie_service.fetch_payment_status(order_dict["payment_id"])
            if remote and remote.get("status") and remote["status"] != order_dict["payment_status"]:
                new_status = remote["status"]
                now = datetime.utcnow().isoformat() + "Z"
                cur.execute(
                    "UPDATE orders SET payment_status = ?, updated_at = ? WHERE order_id = ?",
                    (new_status, now, order_id),
                )
                conn.commit()
                order_dict["payment_status"] = new_status
                order_dict["updated_at"] = now
            conn.close()

            order_dict["customer"] = json.loads(order_dict.pop("customer_json", "{}"))
            order_dict["items"] = json.loads(order_dict.pop("items_json", "[]"))
            self._send_json(order_dict)
            return

        if path.startswith("/mollie-checkout/"):
            payment_id = path.split("/mollie-checkout/", 1)[1].strip()
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders WHERE payment_id = ?", (payment_id,))
            row = cur.fetchone()
            conn.close()
            if not row:
                self._send_html("<h1>Zahlung nicht gefunden</h1>", status=404)
                return
            self._send_html(render_mollie_simulator_html(dict(row)))
            return

        # Statische Dateien aus /static ausliefern
        rel_path = "index.html" if path in ("/", "") else path.lstrip("/")
        file_path = (STATIC_DIR / rel_path).resolve()
        if not str(file_path).startswith(str(STATIC_DIR.resolve())) or not file_path.is_file():
            file_path = STATIC_DIR / "index.html"

        ctype, _ = mimetypes.guess_type(str(file_path))
        ctype = ctype or "application/octet-stream"
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{ctype}; charset=utf-8" if ctype.startswith("text/") or ctype == "application/javascript" else ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlsplit(self.path)
        path = parsed.path
        body = self._read_body_json()

        if path == "/api/configurator/calculate":
            calc = calculate_configuration(body)
            self._send_json(calc)
            return

        if path == "/api/configurator/save":
            calc = calculate_configuration(body)
            config_code = "BL-HK-" + uuid.uuid4().hex[:6].upper()
            now = datetime.utcnow().isoformat() + "Z"
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO configurations (config_code, config_json, summary_title, total_eur, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (config_code, json.dumps(body, ensure_ascii=False), calc["summary_title"], calc["total_eur"], now),
            )
            conn.commit()
            conn.close()
            self._send_json({"config_code": config_code, "calculation": calc, "created_at": now}, status=201)
            return

        if path == "/api/mollie/settings":
            api_key = str(body.get("api_key", "")).strip()
            mollie_service.set_api_key(api_key)
            self._send_json(mollie_service.get_mode_info())
            return

        if path == "/api/orders/checkout":
            customer = body.get("customer") or {}
            name = str(customer.get("name", "")).strip()
            email = str(customer.get("email", "")).strip()
            if not name or not email:
                self._send_json({"error": "Bitte gib deinen Namen und deine E-Mail-Adresse an."}, status=400)
                return

            payment_method = str(body.get("payment_method", "eps")).strip() or "eps"
            cart_items = body.get("items") or []
            if not cart_items:
                self._send_json({"error": "Der Warenkorb ist leer."}, status=400)
                return

            products_map = {p["id"]: p for p in PRODUCTS}
            normalized_items: List[Dict[str, Any]] = []
            subtotal_eur = 0.0
            shipping_eur = 0.0

            for raw_item in cart_items:
                item_type = raw_item.get("type", "product")
                qty = max(1, min(20, int(raw_item.get("quantity", 1) or 1)))
                if item_type == "custom_automat" and isinstance(raw_item.get("config"), dict):
                    calc = calculate_configuration(raw_item["config"])
                    unit_price = calc["subtotal_eur"]
                    item_ship = calc["shipping_eur"] * qty
                    line_total = round(unit_price * qty, 2)
                    subtotal_eur += line_total
                    shipping_eur += item_ship
                    normalized_items.append(
                        {
                            "type": "custom_automat",
                            "title": calc["summary_title"],
                            "quantity": qty,
                            "unit_price_eur": unit_price,
                            "shipping_eur": item_ship,
                            "line_total_eur": line_total,
                            "details": [li["label"] for li in calc["line_items"]],
                            "config": raw_item["config"],
                        }
                    )
                else:
                    pid = raw_item.get("product_id")
                    prod = products_map.get(pid)
                    if not prod:
                        continue
                    unit_price = float(prod["price"])
                    line_total = round(unit_price * qty, 2)
                    subtotal_eur += line_total
                    normalized_items.append(
                        {
                            "type": "product",
                            "product_id": prod["id"],
                            "sku": prod["sku"],
                            "title": prod["name"],
                            "quantity": qty,
                            "unit_price_eur": unit_price,
                            "shipping_eur": 0.0,
                            "line_total_eur": line_total,
                            "details": [prod["short_desc"]],
                        }
                    )

            if not normalized_items:
                self._send_json({"error": "Keine gültigen Positionen in der Bestellung."}, status=400)
                return

            subtotal_eur = round(subtotal_eur, 2)
            shipping_eur = round(shipping_eur, 2)
            total_eur = round(subtotal_eur + shipping_eur, 2)
            vat_eur = round(total_eur - (total_eur / 1.20), 2)

            order_id = uuid.uuid4().hex[:12]
            order_number = f"BL-{datetime.utcnow().strftime('%Y%m%d')}-{order_id[:4].upper()}"
            base_url = self._base_url()
            redirect_url = f"{base_url}/?order={order_id}"
            webhook_url = f"{base_url}/api/mollie/webhook"

            description = f"Der Bienenladen × Honig-Kiste.de | Bestellung {order_number}"

            try:
                payment_res = mollie_service.create_payment(
                    order_id=order_id,
                    amount_eur=total_eur,
                    description=description,
                    method=payment_method,
                    redirect_url=redirect_url,
                    webhook_url=webhook_url,
                    base_url=base_url,
                    metadata={"order_id": order_id, "order_number": order_number},
                )
            except Exception as exc:
                self._send_json({"error": str(exc)}, status=502)
                return

            now = datetime.utcnow().isoformat() + "Z"
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO orders (
                    order_id, order_number, customer_json, items_json,
                    subtotal_eur, shipping_eur, total_eur, vat_eur,
                    payment_method, payment_id, payment_status, payment_provider,
                    checkout_url, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    order_id,
                    order_number,
                    json.dumps(customer, ensure_ascii=False),
                    json.dumps(normalized_items, ensure_ascii=False),
                    subtotal_eur,
                    shipping_eur,
                    total_eur,
                    vat_eur,
                    payment_method,
                    payment_res["id"],
                    payment_res["status"],
                    payment_res["provider"],
                    payment_res["checkout_url"],
                    now,
                    now,
                ),
            )
            conn.commit()
            conn.close()

            self._send_json(
                {
                    "order_id": order_id,
                    "order_number": order_number,
                    "total_eur": total_eur,
                    "payment_id": payment_res["id"],
                    "payment_status": payment_res["status"],
                    "payment_provider": payment_res["provider"],
                    "checkout_url": payment_res["checkout_url"],
                },
                status=201,
            )
            return

        if path == "/api/mollie/webhook":
            payment_id = str(body.get("id", "")).strip()
            explicit_status = str(body.get("status", "")).strip()
            if not payment_id:
                self._send_json({"error": "Missing payment id"}, status=400)
                return

            new_status = explicit_status
            if not new_status:
                remote = mollie_service.fetch_payment_status(payment_id)
                if remote and remote.get("status"):
                    new_status = remote["status"]

            if new_status:
                now = datetime.utcnow().isoformat() + "Z"
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute(
                    "UPDATE orders SET payment_status = ?, updated_at = ? WHERE payment_id = ?",
                    (new_status, now, payment_id),
                )
                conn.commit()
                conn.close()

            self._send_json({"received": True, "payment_id": payment_id, "status": new_status or "unchanged"})
            return

        self._send_json({"error": "Unbekannter Endpunkt"}, status=404)


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    init_db()
    server = ThreadingHTTPServer((host, port), HonigautomatRequestHandler)
    print(f"🐝 Der Bienenladen × Honig-Kiste.de Webapp läuft auf http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    port_env = int(os.environ.get("PORT", "8000"))
    run_server(port=port_env)

