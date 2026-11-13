"""
Mollie Payments API v2 Service für Der Bienenladen × Honig-Kiste.de.
Unterstützt echte Mollie API v2 Aufrufe (test_... / live_...) sowie einen
interaktiven lokalen Mollie Hosted Checkout Simulator für sofortiges Testen.
"""

import os
import uuid
import time
import requests
from typing import Dict, Any, Optional

MOLLIE_API_BASE = "https://api.mollie.com/v2"

MOLLIE_METHODS = [
    {
        "id": "eps",
        "name": "eps-Überweisung (Österreich)",
        "badge": "Empfohlen für AT",
        "description": "Direkte und sichere Online-Überweisung über deine österreichische Hausbank."
    },
    {
        "id": "klarna",
        "name": "Klarna (Rechnung / Ratenkauf / Sofort)",
        "badge": "Flexibel finanzieren",
        "description": "Bezahlung auf Rechnung (30 Tage) oder bequeme Ratenzahlung für deinen Honigautomaten."
    },
    {
        "id": "creditcard",
        "name": "Kredit- & Debitkarte (Visa, Mastercard, Amex)",
        "badge": "Sofortbestätigung",
        "description": "3D-Secure geschützte Kartenzahlung über Mollie."
    },
    {
        "id": "paypal",
        "name": "PayPal",
        "badge": "Käuferschutz",
        "description": "Schnelle Zahlung über dein bestehendes PayPal-Konto."
    },
    {
        "id": "applepay",
        "name": "Apple Pay",
        "badge": "Express",
        "description": "Kontaktlose Ein-Klick-Zahlung mit Face ID / Touch ID."
    },
    {
        "id": "banktransfer",
        "name": "SEPA-Banküberweisung (Vorkasse via Mollie)",
        "badge": "Klassisch",
        "description": "Automatisch zugeordnete SEPA-Überweisung mit Käuferbenachrichtigung."
    }
]


class MollieService:
    def __init__(self) -> None:
        self.runtime_api_key: str = os.environ.get("MOLLIE_API_KEY", "").strip()

    def available_methods(self):
        if not self.is_live_or_test_key_configured():
            return [] if os.environ.get("APP_ENV") == "production" else MOLLIE_METHODS
        if getattr(self, "_methods_until", 0) > time.time():
            return self._methods_cache
        try:
            response = requests.get(f"{MOLLIE_API_BASE}/methods", headers={"Authorization": f"Bearer {self.get_api_key()}"}, params={"locale": "de_AT"}, timeout=8)
            response.raise_for_status()
            enabled = {m["id"] for m in response.json().get("_embedded", {}).get("methods", [])}
            self._methods_cache = [m for m in MOLLIE_METHODS if m["id"] in enabled and m["id"] in {"eps", "creditcard", "paypal", "banktransfer"}]
            self._methods_until = time.time() + 120
            return self._methods_cache
        except requests.RequestException:
            return []

    def get_api_key(self) -> str:
        return self.runtime_api_key or os.environ.get("MOLLIE_API_KEY", "").strip()

    def set_api_key(self, api_key: str) -> None:
        self.runtime_api_key = (api_key or "").strip()
        self._methods_until = 0

    def is_live_or_test_key_configured(self) -> bool:
        key = self.get_api_key()
        return key.startswith("test_") or key.startswith("live_")

    def get_mode_info(self) -> Dict[str, Any]:
        key = self.get_api_key()
        if key.startswith("live_"):
            return {"mode": "live", "label": "Mollie Live-API aktiv", "has_key": True, "masked_key": "••••••••"}
        if key.startswith("test_"):
            return {"mode": "test", "label": "Mollie Test-API aktiv", "has_key": True, "masked_key": "••••••••"}
        return {
            "mode": "sandbox_simulator",
            "label": "Integrierter Mollie Checkout-Simulator (Kein API-Key erforderlich – Test/Live-Key optional hinterlegbar)",
            "has_key": False,
            "masked_key": ""
        }

    def create_payment(
        self,
        order_id: str,
        amount_eur: float,
        description: str,
        method: Optional[str],
        redirect_url: str,
        webhook_url: str,
        base_url: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Erstellt eine Zahlung über die offizielle Mollie Payments API v2
        (`POST https://api.mollie.com/v2/payments`).
        Falls kein `test_`/`live_` API-Key hinterlegt ist, wird eine lokal
        simulierte Mollie-Zahlung erzeugt, die über `/mollie-checkout/<id>`
        interaktiv abgeschlossen werden kann.
        """
        api_key = self.get_api_key()
        if os.environ.get("APP_ENV") == "production" and not api_key.startswith("live_"):
            raise RuntimeError("Mollie Live-Zahlung ist noch nicht eingerichtet.")
        value_str = f"{amount_eur:.2f}"

        if api_key.startswith("test_") or api_key.startswith("live_"):
            payload: Dict[str, Any] = {
                "amount": {
                    "currency": "EUR",
                    "value": value_str
                },
                "description": description,
                "redirectUrl": redirect_url,
                "metadata": metadata,
                "locale": "de_AT",
            }
            # Webhook nur mitsenden, wenn öffentlich erreichbar (Mollie lehnt localhost-Webhooks ab)
            if webhook_url and not ("localhost" in webhook_url or "127.0.0.1" in webhook_url):
                payload["webhookUrl"] = webhook_url
            if method and method in {m["id"] for m in MOLLIE_METHODS}:
                payload["method"] = method

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            resp = requests.post(f"{MOLLIE_API_BASE}/payments", json=payload, headers=headers, timeout=15)
            if resp.status_code in (200, 201):
                data = resp.json()
                checkout_url = data.get("_links", {}).get("checkout", {}).get("href", redirect_url)
                return {
                    "id": data["id"],
                    "status": data.get("status", "open"),
                    "method": data.get("method") or method or "eps",
                    "amount": value_str,
                    "currency": "EUR",
                    "description": description,
                    "checkout_url": checkout_url,
                    "provider": "mollie_api_v2",
                    "raw": data,
                }
            else:
                # Falls API-Key ungültig oder Methode im Mollie-Profil noch nicht aktiviert, Fehlerdetail zurückgeben
                err_detail = resp.text
                raise RuntimeError(f"Mollie API Fehler ({resp.status_code}): {err_detail}")

        # Lokaler interaktiver Mollie Hosted Checkout Simulator
        sim_payment_id = f"tr_sim_{uuid.uuid4().hex[:10]}"
        checkout_url = f"{base_url.rstrip('/')}/mollie-checkout/{sim_payment_id}"
        return {
            "id": sim_payment_id,
            "status": "open",
            "method": method or "eps",
            "amount": value_str,
            "currency": "EUR",
            "description": description,
            "checkout_url": checkout_url,
            "provider": "mollie_simulator",
            "raw": {
                "resource": "payment",
                "id": sim_payment_id,
                "mode": "test",
                "amount": {"value": value_str, "currency": "EUR"},
                "description": description,
                "method": method or "eps",
                "status": "open",
                "metadata": metadata,
            }
        }

    def fetch_payment_status(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """Fragt den aktuellen Zahlungsstatus bei der echten Mollie API v2 ab."""
        api_key = self.get_api_key()
        if not (api_key.startswith("test_") or api_key.startswith("live_")):
            return None
        if payment_id.startswith("tr_sim_"):
            return None
        headers = {"Authorization": f"Bearer {api_key}"}
        resp = requests.get(f"{MOLLIE_API_BASE}/payments/{payment_id}", headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()

