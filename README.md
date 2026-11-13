# Honigautomaten-Shop · Der Bienenladen

Python-Webshop für Honigautomaten von Honig-Kiste, passendes Zubehör und die optionale Inbetriebnahme und Einschulung im Bienenladen in Linz.

## Lokal starten

Python 3.10 oder neuer:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PORT=8001 python3 app.py
```

Anschließend http://localhost:8001 öffnen. Port 8000 ist die Voreinstellung, wenn `PORT` nicht gesetzt ist. Der Server bindet an alle Netzwerkschnittstellen.

## Funktionen

- Modellvergleich und Konfigurator mit serverseitiger Preisberechnung
- Warenkorb im Browser und Bestellungen in SQLite
- Optionale Inbetriebnahme und Einschulung im Bienenladen: 120 € inkl. MwSt.
- Persönliche Beratung und Vorführung nach Terminvereinbarung
- Verweis auf honigautomaten.at mit Mitgliedertarifen
- Impressum, Datenschutz, lokale Produktbilder und Schriftarten

## Zahlung und Daten

Ohne `MOLLIE_API_KEY` verwendet der Shop einen lokalen Zahlungssimulator. Damit entstehen keine echten Zahlungen. Ein Mollie-Testschlüssel aktiviert die externe Test-API; ein Live-Schlüssel aktiviert echte Zahlungsanforderungen. Schlüssel ausschließlich über die Umgebung konfigurieren und niemals einchecken.

Beim ersten Start entsteht `honigautomat.db`. Sie enthält unter anderem Bestell- und Kundendaten und wird nicht versioniert. Für Tests ausschließlich fiktive Kundendaten verwenden.

Dies ist der lokale Entwicklungsstand. Vor einem öffentlichen Produktivbetrieb müssen insbesondere Serverbetrieb, Zugriffsschutz auf Verwaltungs- und Bestellendpunkte, Zahlungsintegration und Datenschutzangaben zur tatsächlichen Infrastruktur eingerichtet bzw. geprüft werden. Die aktuelle Anwendung enthält keine Benutzeranmeldung; Verwaltungs- und Bestellendpunkte daher nicht ungeschützt öffentlich bereitstellen.

## Inhalte und Assets

Produktdaten und Produktbilder: Honig-Kiste (https://honig-kiste.de). Betreiberangaben: Der Bienenladen / OÖ. Landesverband für Bienenzucht. Logo: vom Betreiber bereitgestellt. Diese Inhalte sind nicht durch eine allgemeine Open-Source-Lizenz dieses Repositorys freigegeben.

Manrope und Work Sans werden lokal eingebunden. Die jeweiligen SIL Open Font Licenses liegen unter `static/fonts/`.
