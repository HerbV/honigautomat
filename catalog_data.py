"""
Vollständige Produkt- und Konfigurationsdaten von Honig-Kiste.de
für den exklusiven Händler: Der Bienenladen.
"""

DEALER_INFO = {
    "name": "Der Bienenladen",
    "tagline": "Exklusiver General- & Fachhändler von Honig-Kiste.de",
    "subtitle": "24/7 Selbstbedienungs-Honigautomaten (Generation 3), Automaten-Zubehör & Erweiterungen",
    "address": "Pachmayrstraße 57, 4040 Linz (Imkereizentrum) & Online-Direktvertrieb (DE / AT / EU)",
    "phone": "+43 (0) 732 / 73 20 70",
    "email": "automaten@bienenladen.at",
    "manufacturer": {
        "name": "Honig-Kiste.de – Oliver Pattay",
        "location": "Fort I, 1, 46487 Wesel am Niederrhein, Deutschland",
        "email": "info@honig-kiste.de",
        "website": "https://www.honig-kiste.de",
        "story": (
            "Entwickelt aus der Praxis für die Praxis: Hobbyimker Oliver Pattay aus Wesel am Niederrhein "
            "und Programmierer Matthias (beehappyyoubee) haben den Honigautomaten geschaffen, um Imkern "
            "einen sicheren, wetterfest geschützten und stromsparenden 24/7-Direktverkauf ohne Personalaufwand "
            "zu ermöglichen. Ab Februar 2026 ist die 3. Generation mit integrierter Web-Konfiguration verfügbar."
        ),
    },
    "highlights": [
        {
            "title": "Generation 3 (Web-Interface)",
            "desc": "Komfortable Programmierung von Preisen, Fächern und Parametern direkt per Webbrowser oder am Tastenfeld.",
            "icon": "wifi"
        },
        {
            "title": "12V Powersafe & Solarfähig",
            "desc": "Extrem sparsamer 12V-DC-Betrieb mit Powersafe-Modus – wahlweise über 230V-Netzteil, 12V-Akku-Satz oder Solarpanel.",
            "icon": "sun"
        },
        {
            "title": "Modular bis 45 Fächer",
            "desc": "Starte mit 5, 10 oder 15 Fächern und erweitere das System jederzeit um bis zu zwei 15er-Slave-Schränke.",
            "icon": "grid"
        },
        {
            "title": "Bargeld & Bargeldlos",
            "desc": "Serienmäßig mit 5-Kanal-Münzprüfer (0,10 € – 2,00 €), optional mit NV10USB+ Geldscheinleser, myPOS Sigma oder Nayax ONYX.",
            "icon": "credit-card"
        },
        {
            "title": "Wunschfarbe ohne Aufpreis",
            "desc": "Pulverbeschichtetes, elo-verzinktes Stahlblech in Klassik-Rapsgelb, Sondereditionen oder deiner individuellen RAL-Farbe.",
            "icon": "palette"
        },
        {
            "title": "Exklusiv im Bienenladen",
            "desc": "Persönliche Fachberatung, Konfiguration nach Maß, sichere Zahlung über Mollie (EPS, Klarna, Karte, PayPal) & Support.",
            "icon": "shield"
        }
    ]
}

RAL_COLORS = [
    {"code": "RAL 1021", "name": "Rapsgelb (Klassiker)", "hex": "#F6B600"},
    {"code": "RAL 1005", "name": "Honiggelb", "hex": "#C89F04"},
    {"code": "RAL 1015", "name": "Hellelfenbein", "hex": "#E6D2B5"},
    {"code": "RAL 9005", "name": "Tiefschwarz (Standard Dach)", "hex": "#141619"},
    {"code": "RAL 7016", "name": "Anthrazitgrau", "hex": "#383E42"},
    {"code": "RAL 7035", "name": "Lichtgrau", "hex": "#CBD0CC"},
    {"code": "EDELSTAHL", "name": "Edelstahl gebürstet (Sonderedition)", "hex": "#B7BFC4"},
    {"code": "RAL 6005", "name": "Moosgrün", "hex": "#114232"},
    {"code": "RAL 6009", "name": "Tannengrün", "hex": "#27352A"},
    {"code": "RAL 6018", "name": "Gelbgrün (Alpenwiese)", "hex": "#57A639"},
    {"code": "RAL 8017", "name": "Schokoladenbraun", "hex": "#442F29"},
    {"code": "RAL 3000", "name": "Feuerrot", "hex": "#A72920"},
    {"code": "RAL 5010", "name": "Enzianblau", "hex": "#0E4C8A"},
    {"code": "RAL 9010", "name": "Reinweiß", "hex": "#F7F5EF"},
]

CONFIGURATOR_OPTIONS = {
    "base_models": [
        {
            "id": "automat-5",
            "compartments": 5,
            "columns": 1,
            "rows": 5,
            "name": "Honigautomat 5 Fächer (Gen. 3)",
            "subtitle": "Kompakter Wandautomat für den Einstieg (5 einzeln programmierbare Verkaufsfächer)",
            "dimensions": "93,1 cm (H) × 40,6 cm (B) inkl. Dachvorsprung",
            "door_size": "14,5 cm (H) × 14,4 cm (B) aus 5 mm Acrylglas",
            "weight_kg": 20.0,
            "shipping_weight_kg": 22.0,
            "prices_by_depth": {
                "180": 1049.00,
                "240": 1129.00
            },
            "image": "/images/products/product-0.png"
        },
        {
            "id": "automat-10",
            "compartments": 10,
            "columns": 2,
            "rows": 5,
            "name": "Honigautomat 10 Fächer (Gen. 3)",
            "subtitle": "Der beliebte Allrounder für vielfältige Honigsorten (10 einzeln wählbare Verkaufsfächer)",
            "dimensions": "93,1 cm (H) × 56,4 cm (B) inkl. Dachvorsprung",
            "door_size": "14,5 cm (H) × 14,4 cm (B) aus 5 mm Acrylglas",
            "weight_kg": 35.0,
            "shipping_weight_kg": 37.0,
            "prices_by_depth": {
                "180": 1349.00,
                "240": 1449.00
            },
            "image": "/images/products/product-3.png"
        },
        {
            "id": "automat-15",
            "compartments": 15,
            "columns": 3,
            "rows": 5,
            "name": "Honigautomat 15 Fächer (Gen. 3)",
            "subtitle": "Maximale Kapazität im Hauptgerät für stark frequentierte Standorte (15 Verkaufsfächer)",
            "dimensions": "93,1 cm (H) × 69,3 cm (B) inkl. Dachvorsprung",
            "door_size": "14,5 cm (H) × 14,4 cm (B) aus 5 mm Acrylglas",
            "weight_kg": 40.0,
            "shipping_weight_kg": 44.0,
            "prices_by_depth": {
                "180": 1649.00,
                "240": 1819.00
            },
            "image": "/images/products/product-5.png"
        }
    ],
    "depths": [
        {
            "id": "180",
            "name": "180 mm Fachtiefe",
            "badge": "Standard für Honiggläser",
            "description": "Optimal für alle gängigen 250g und 500g Honiggläser (DIB-Glas, Twist-Off), Propolis-Tinkturen, Bienenwachskerzen und Kosmetik."
        },
        {
            "id": "240",
            "name": "240 mm Fachtiefe (250 mm nutzbar)",
            "badge": "Für große Gebinde & 10er Eierkartons",
            "description": "Extra tiefe Ausführung – bietet Platz für mehrere Gläser hintereinander, Geschenksets, Met-Flaschen oder 10er Eierkartons."
        }
    ],
    "extensions": [
        {
            "id": "ext-0",
            "count": 0,
            "extra_compartments": 0,
            "name": "Keine Erweiterung (Nur Hauptautomat)",
            "description": "Kann dank Generation-3-Steuerung auch jederzeit später nachgerüstet werden.",
            "prices_by_depth": {"180": 0.0, "240": 0.0}
        },
        {
            "id": "ext-1",
            "count": 1,
            "extra_compartments": 15,
            "name": "+ 1× Erweiterungsschrank (15 zusätzliche Fächer)",
            "description": "Wird direkt über das Verbindungskabel vom Tastenfeld des Hauptautomaten mitgesteuert (Maße: 93,1 × 69,3 cm).",
            "prices_by_depth": {"180": 1509.00, "240": 1599.00}
        },
        {
            "id": "ext-2",
            "count": 2,
            "extra_compartments": 30,
            "name": "+ 2× Erweiterungsschrank (30 zusätzliche Fächer)",
            "description": "Maximale Ausbaustufe mit zwei 15er-Slave-Schränken für bis zu 45 einzeln ansteuerbare Verkaufsfächer.",
            "prices_by_depth": {"180": 3018.00, "240": 3198.00}
        }
    ],
    "door_designs": [
        {
            "id": "classic-bee",
            "name": "Klassisch: Gravur Biene & Fachnummern",
            "description": "5 mm Acrylglastüren mit edler Lasergravur einer Honigbiene sowie gut lesbarer Fachnummerierung.",
            "price": 0.00
        },
        {
            "id": "numbers-only",
            "name": "Minimalistisch: Kein Motiv, nur Fachnummern",
            "description": "Freie Sicht auf deine Produkte – 5 mm Acrylglastüren ausschließlich mit klarer Fachnummerierung.",
            "price": 0.00
        },
        {
            "id": "custom-logo",
            "name": "Individuell: Eigenes Imkerei-Motiv & Fachnummern",
            "description": "Lasergravur deines eigenen Imkerei-Logos oder Schriftzugs auf jeder Acrylglastür inklusive Fachnummern.",
            "price": 0.00
        }
    ],
    "payment_addons": [
        {
            "id": "nv10-bill",
            "name": "NV10USB+ Geldscheinleser inkl. Frontblende",
            "sku": "HK-70",
            "price": 269.00,
            "category": "cash",
            "description": "Akzeptiert 5 €, 10 €, 20 € Banknoten zuverlässig. Komplett montiert inkl. Frontblende und Kabelsatz."
        },
        {
            "id": "mypos-sigma",
            "name": "myPOS Sigma Bargeldlos-Terminal (ohne monatl. Grundgebühr)",
            "sku": "HK-125",
            "price": 549.00,
            "category": "cashless",
            "description": "5,0\" HD-Touchscreen, NFC (Apple Pay, Google Pay, Girocard, Kreditkarte), inkl. 4G-SIM-Karte – keine monatliche Grundgebühr!"
        },
        {
            "id": "nayax-onyx",
            "name": "Nayax ONYX Kontaktlos-Terminal",
            "sku": "HK-71",
            "price": 625.32,
            "category": "cashless",
            "description": "Industrieführendes NFC-/Kartenterminal inkl. Telemetrie & Fernüberwachung (separate Vertragsbindung mit Nayax erforderlich)."
        }
    ],
    "power_telemetry_addons": [
        {
            "id": "akku-satz",
            "name": "12V Akku-Satz (2× 5200 mAh + 230V Ladegerät)",
            "sku": "HK-82",
            "price": 125.00,
            "description": "Für autarken Betrieb ohne Steckdose (z.B. am Bienenstand oder mit Solarpanel). Mit integrierter Füllstandsanzeige."
        },
        {
            "id": "sim-sms-modul",
            "name": "SIM SMS Telemetriemodul (ab Werk verbaut & programmiert)",
            "sku": "HK-96",
            "price": 89.50,
            "description": "Sendet automatisch eine SMS an deine Wunsch-Rufnummer, sobald nur noch 3 Fächer befüllt sind, und wertet SMS-Zahlungsinfos aus."
        }
    ],
    "shipping_options": [
        {
            "id": "pickup-bienenladen",
            "name": "Abholung im Bienenladen",
            "description": "Kostenlose Abholung im Bienenladen Linz. Inbetriebnahme und Einschulung sind separat buchbar.",
            "price": 0.00
        },
        {
            "id": "de-palette",
            "name": "Deutschland – Kartonverpackung auf Palette",
            "description": "Sicher verpackt im Spezialkarton auf Palette (Speditionsversand frei Bordsteinkante).",
            "price": 0.00
        },
        {
            "id": "eu-eur-palette",
            "name": "Österreich & EU – EUR-Palette mit 2 Bohrschablonen & 2 Spanngurten",
            "description": "Transportgesichert auf Original EUR-Palette inkl. 2 praktischer Bohrschablonen für die sofortige Wandmontage.",
            "price": 14.28
        },
        {
            "id": "intl-einweg",
            "name": "Andere Länder – Kartonverpackung auf Einweg-Palette",
            "description": "Exportverpackung auf Einweg-Palette für den internationalen Versand.",
            "price": 11.90
        }
    ]
}

PRODUCTS = [
    # --- HONIGAUTOMATEN ---
    {
        "id": "hk-auto-5-180-raps",
        "sku": "HK-124",
        "name": "Honigautomat 5 Fächer – Rapsgelb / Schwarz (180 mm Fachtiefe)",
        "category": "automaten",
        "category_label": "Honigautomaten (Gen. 3)",
        "price": 1049.00,
        "delivery_time": "5 – 6 Wochen",
        "badge": "Kompakt-Klassiker",
        "image": "/images/products/product-0.png",
        "short_desc": "Komplett montierter 5-Fächer-Honigautomat der 3. Generation (ab 2026 mit Web-Konfiguration) in Rapsgelb mit schwarzem Dach.",
        "specs": {
            "Fächeranzahl": "5 einzeln programmierbare Fächer",
            "Fachtiefe": "180 mm (ideal für DIB- & Imkergläser)",
            "Abmessungen (H × B)": "93,1 cm × 40,6 cm (mit Dachvorsprung)",
            "Türgröße (H × B)": "14,5 cm × 14,4 cm (5 mm Acrylglas mit Bienengravur)",
            "Münzprüfer": "Inklusive für 0,10 €, 0,20 €, 0,50 €, 1,00 € & 2,00 €",
            "Stromversorgung": "12V DC mit Powersafe (inkl. 230V-Netzteil, Batterie/Solar möglich)",
            "Gewicht": "20,0 kg (Versandgewicht 22,0 kg)",
            "Material": "Elo-verzinktes Stahlblech, 2-farbig RAL pulverbeschichtet"
        },
        "configurator_preset": {"model": "automat-5", "depth": "180", "body_color": "RAL 1021", "roof_color": "RAL 9005"}
    },
    {
        "id": "hk-auto-5-240-raps",
        "sku": "HK-90",
        "name": "Honigautomat 5 Fächer – Rapsgelb / Schwarz (240 mm Fachtiefe)",
        "category": "automaten",
        "category_label": "Honigautomaten (Gen. 3)",
        "price": 1129.00,
        "delivery_time": "5 – 6 Wochen",
        "badge": "Tiefe Fächer",
        "image": "/images/products/product-1.png",
        "short_desc": "5-Fächer-Honigautomat mit extra tiefen 240-mm-Fächern (nutzbar bis 250 mm – auch passend für 10er Eierkartons) und Web-Interface.",
        "specs": {
            "Fächeranzahl": "5 einzeln programmierbare Fächer",
            "Fachtiefe": "240 mm / 250 mm (auch für 10er Eierkartons geeignet)",
            "Abmessungen (H × B)": "93,1 cm × 40,6 cm (mit Dachvorsprung)",
            "Türgröße (H × B)": "14,5 cm × 14,4 cm (5 mm Acrylglas mit Bienengravur)",
            "Münzprüfer": "Inklusive für 0,10 €, 0,20 €, 0,50 €, 1,00 € & 2,00 €",
            "Stromversorgung": "12V DC mit Powersafe (inkl. 230V-Netzteil, Batterie/Solar möglich)",
            "Gewicht": "22,0 kg"
        },
        "configurator_preset": {"model": "automat-5", "depth": "240", "body_color": "RAL 1021", "roof_color": "RAL 9005"}
    },
    {
        "id": "hk-auto-10-180-raps",
        "sku": "HK-120",
        "name": "Honigautomat 10 Fächer – Rapsgelb / Schwarz (180 mm Fachtiefe)",
        "category": "automaten",
        "category_label": "Honigautomaten (Gen. 3)",
        "price": 1349.00,
        "delivery_time": "4 – 9 Werktage",
        "badge": "Bestseller",
        "image": "/images/products/product-2.png",
        "short_desc": "Der beliebte 10-Fächer-Automat für bis zu 10 verschiedene Honigsorten oder Imkereiprodukte. Sofort einsatzbereit montiert.",
        "specs": {
            "Fächeranzahl": "10 einzeln programmierbare Fächer",
            "Fachtiefe": "180 mm",
            "Abmessungen (H × B)": "93,1 cm × 56,4 cm (mit Dachvorsprung)",
            "Türgröße (H × B)": "14,5 cm × 14,4 cm (5 mm Acrylglas)",
            "Münzprüfer": "Inklusive für 0,10 €, 0,20 €, 0,50 €, 1,00 € & 2,00 €",
            "Stromversorgung": "12V DC mit Powersafe (inkl. 230V-Steckernetzteil)",
            "Gewicht": "33,0 kg (Versandgewicht 35,0 kg)"
        },
        "configurator_preset": {"model": "automat-10", "depth": "180", "body_color": "RAL 1021", "roof_color": "RAL 9005"}
    },
    {
        "id": "hk-auto-10-240-raps",
        "sku": "HK-95",
        "name": "Honigautomat 10 Fächer – Rapsgelb / Schwarz (240 mm Fachtiefe)",
        "category": "automaten",
        "category_label": "Honigautomaten (Gen. 3)",
        "price": 1449.00,
        "delivery_time": "4 – 9 Werktage",
        "badge": "Sofort lieferbar",
        "image": "/images/products/product-3.png",
        "short_desc": "10-Fächer-Automat mit großer 240-mm-Fachtiefe für Honig-Doppelpacks, Geschenksets oder 10er Eierkartons.",
        "specs": {
            "Fächeranzahl": "10 einzeln programmierbare Fächer",
            "Fachtiefe": "240 mm (nutzbar bis 250 mm, passend für 10er Eierkartons)",
            "Abmessungen (H × B)": "93,1 cm × 56,4 cm (mit Dachvorsprung)",
            "Türgröße (H × B)": "14,5 cm × 14,4 cm (5 mm Acrylglas)",
            "Münzprüfer": "Inklusive für 0,10 €, 0,20 €, 0,50 €, 1,00 € & 2,00 €",
            "Stromversorgung": "12V DC mit Powersafe (inkl. 230V-Steckernetzteil)",
            "Gewicht": "35,0 kg (Versandgewicht 37,0 kg)"
        },
        "configurator_preset": {"model": "automat-10", "depth": "240", "body_color": "RAL 1021", "roof_color": "RAL 9005"}
    },
    {
        "id": "hk-auto-15-180-raps",
        "sku": "HK-83",
        "name": "Honigautomat 15 Fächer – Rapsgelb / Schwarz (180 mm Fachtiefe)",
        "category": "automaten",
        "category_label": "Honigautomaten (Gen. 3)",
        "price": 1649.00,
        "delivery_time": "5 – 6 Wochen",
        "badge": "Großes Sortiment",
        "image": "/images/products/product-4.png",
        "short_desc": "15-Fächer-Hauptautomat der 3. Generation mit Web-Konfiguration, Zahlenfeld und 5-Kanal-Münzprüfer.",
        "specs": {
            "Fächeranzahl": "15 einzeln programmierbare Fächer",
            "Fachtiefe": "180 mm",
            "Abmessungen (H × B)": "93,1 cm × 69,3 cm (mit Dachvorsprung)",
            "Türgröße (H × B)": "14,5 cm × 14,4 cm (5 mm Acrylglas)",
            "Erweiterbarkeit": "Bis zu 2× 15-Fächer-Erweiterungen (= 45 Fächer gesamt)",
            "Gewicht": "38,0 kg (Versandgewicht 42,0 kg)"
        },
        "configurator_preset": {"model": "automat-15", "depth": "180", "body_color": "RAL 1021", "roof_color": "RAL 9005"}
    },
    {
        "id": "hk-auto-15-240-raps",
        "sku": "HK-100",
        "name": "Honigautomat 15 Fächer – Rapsgelb / Schwarz (240 mm Fachtiefe)",
        "category": "automaten",
        "category_label": "Honigautomaten (Gen. 3)",
        "price": 1819.00,
        "delivery_time": "5 – 6 Wochen",
        "badge": "Top-Modell",
        "image": "/images/products/product-5.png",
        "short_desc": "Das Flaggschiff mit 15 extra tiefen Fächern (240 mm) – wahlweise in Rapsgelb/Schwarz oder freier RAL-Kundenwunschfarbe ohne Aufpreis.",
        "specs": {
            "Fächeranzahl": "15 einzeln programmierbare Fächer",
            "Fachtiefe": "240 mm (passend auch für 10er Eierkartons)",
            "Abmessungen (H × B)": "93,1 cm × 69,3 cm (mit Dachvorsprung)",
            "Türgröße (H × B)": "14,5 cm × 14,4 cm (5 mm Acrylglas)",
            "Erweiterbarkeit": "Bis zu 2× 15-Fächer-Erweiterungen (= 45 Fächer gesamt)",
            "Gewicht": "40,0 kg (Versandgewicht 44,0 kg)"
        },
        "configurator_preset": {"model": "automat-15", "depth": "240", "body_color": "RAL 1021", "roof_color": "RAL 9005"}
    },
    # --- SONDEREDITIONEN ---
    {
        "id": "hk-sonder-15-anthrazit",
        "sku": "HK-168",
        "name": "Sonderedition: Honigautomat 15 Fächer – Gehäuse ANTHRAZIT / Dach Schwarz (180 mm)",
        "category": "sonderedition",
        "category_label": "Sondereditionen & Erweiterungen",
        "price": 1649.00,
        "delivery_time": "4 – 9 Werktage",
        "badge": "Sonderedition Anthrazit",
        "image": "",
        "image_note": "Originalfoto dieser Farbvariante folgt.",
        "short_desc": "Edle Design-Sonderedition in modernem Anthrazitgrau mit schwarzem Dach, 15 Fächern (180 mm) und Generation-3-Elektronik.",
        "specs": {
            "Fächeranzahl": "15 Fächer",
            "Fachtiefe": "180 mm",
            "Gehäusefarbe": "Anthrazit (pulverbeschichtet)",
            "Dachfarbe": "Schwarz",
            "Abmessungen (H × B)": "93,1 cm × 69,3 cm"
        },
        "configurator_preset": {"model": "automat-15", "depth": "180", "body_color": "RAL 7016", "roof_color": "RAL 9005"}
    },
    {
        "id": "hk-sonder-15-edelstahl",
        "sku": "HK-169",
        "name": "Sonderedition: Honigautomat 15 Fächer – Gehäuse EDELSTAHL / Dach Schwarz (180 mm)",
        "category": "sonderedition",
        "category_label": "Sondereditionen & Erweiterungen",
        "price": 1649.00,
        "delivery_time": "4 – 9 Werktage",
        "badge": "Sonderedition Edelstahl",
        "image": "",
        "image_note": "Originalfoto dieser Farbvariante folgt.",
        "short_desc": "Hochwertige Edelstahl-Ausführung mit schwarzem Dach, 15 Fächern (180 mm), Zahlenfeld und Münzprüfer.",
        "specs": {
            "Fächeranzahl": "15 Fächer",
            "Fachtiefe": "180 mm",
            "Gehäuse": "Edelstahl-Ausführung",
            "Dachfarbe": "Schwarz",
            "Abmessungen (H × B)": "93,1 cm × 69,3 cm"
        },
        "configurator_preset": {"model": "automat-15", "depth": "180", "body_color": "EDELSTAHL", "roof_color": "RAL 9005"}
    },
    {
        "id": "hk-sonder-15-grau",
        "sku": "HK-167",
        "name": "Sonderedition: Honigautomat 15 Fächer – Gehäuse GRAU / Dach Schwarz (180 mm)",
        "category": "sonderedition",
        "category_label": "Sondereditionen & Erweiterungen",
        "price": 1649.00,
        "delivery_time": "4 – 9 Werktage",
        "badge": "Sonderedition Grau",
        "image": "",
        "image_note": "Originalfoto dieser Farbvariante folgt.",
        "short_desc": "Dezente Sonderedition mit grauem Gehäuse und schwarzem Dach für moderne Hausfassaden und Hofläden.",
        "specs": {
            "Fächeranzahl": "15 Fächer",
            "Fachtiefe": "180 mm",
            "Gehäusefarbe": "Grau",
            "Dachfarbe": "Schwarz",
            "Abmessungen (H × B)": "93,1 cm × 69,3 cm"
        },
        "configurator_preset": {"model": "automat-15", "depth": "180", "body_color": "RAL 7035", "roof_color": "RAL 9005"}
    },
    {
        "id": "hk-erw-15-180",
        "sku": "HK-130",
        "name": "Erweiterung mit 15 Fächern für Honigautomat (180 mm Fachtiefe – Rapsgelb oder Wunschfarbe)",
        "category": "sonderedition",
        "category_label": "Sondereditionen & Erweiterungen",
        "price": 1509.00,
        "delivery_time": "5 – 6 Wochen",
        "badge": "Modul-Erweiterung",
        "image": "/images/products/product-19.png",
        "short_desc": "Slave-Erweiterungsschrank mit 15 zusätzlichen Fächern (180 mm) für den 5er-, 10er- oder 15er-Hauptautomaten der 3. Generation.",
        "specs": {
            "Zusatzfächer": "+ 15 einzeln programmierbare Fächer",
            "Fachtiefe": "180 mm",
            "Abmessungen (H × B)": "93,1 cm × 69,3 cm",
            "Steuerung": "Über Tastenfeld & Münz-/Kartenleser des Hauptautomaten (inkl. Verbindungskabel)",
            "Max. Ausbau": "Bis zu 2 Erweiterungen pro Hauptautomat (max. 45 Fächer)"
        }
    },
    {
        "id": "hk-erw-15-240",
        "sku": "HK-131",
        "name": "Erweiterung mit 15 Fächern für Honigautomat (240 mm Fachtiefe – Rapsgelb oder Wunschfarbe)",
        "category": "sonderedition",
        "category_label": "Sondereditionen & Erweiterungen",
        "price": 1599.00,
        "delivery_time": "5 – 6 Wochen",
        "badge": "Tiefe Erweiterung",
        "image": "/images/products/product-20.png",
        "short_desc": "Slave-Erweiterungsschrank mit 15 tiefen Fächern (240 mm, auch für 10er Eierkartons) inkl. Verbindungskabel zum Hauptautomaten.",
        "specs": {
            "Zusatzfächer": "+ 15 einzeln programmierbare Fächer",
            "Fachtiefe": "240 mm (passend auch für 10er Eierkartons)",
            "Abmessungen (H × B)": "93,1 cm × 69,3 cm",
            "Steuerung": "Über Hauptautomat (Generation 3)"
        }
    },
    # --- OPTIONALES ZUBEHÖR & BEZAHLSYSTEME ---
    {
        "id": "hk-zub-nv10",
        "sku": "HK-70",
        "name": "NV10USB+ Geldscheinleser inkl. Frontblende",
        "category": "zubehoer",
        "category_label": "Bezahlsysteme & Automaten-Zubehör",
        "price": 269.00,
        "delivery_time": "Sofort verfügbar",
        "badge": "Banknoten-Akzeptanz",
        "image": "/images/products/product-9.webp",
        "short_desc": "Validiert Banknoten zuverlässig. Direkt passend für alle Honig-Kiste Automaten inkl. Frontblende, Kabelsatz und Montagematerial.",
        "specs": {
            "Hersteller": "Innovative Technology Ltd (NV10USB+)",
            "Lieferumfang": "Geldscheinleser, Frontblende, Anschlusskabel & Montagematerial",
            "Gewicht": "2,0 kg"
        }
    },
    {
        "id": "hk-zub-mypos",
        "sku": "HK-125",
        "name": "myPOS Sigma Terminal Bargeldlos (inkl. 4G SIM, ohne Grundgebühr)",
        "category": "zubehoer",
        "category_label": "Bezahlsysteme & Automaten-Zubehör",
        "price": 549.00,
        "delivery_time": "Sofort verfügbar",
        "badge": "Keine Monatsgebühr!",
        "image": "/images/products/product-18.webp",
        "short_desc": "Modernes Bargeldlos-Terminal mit 5,0\" HD-Multi-Touchscreen, Kontaktlos-/NFC-, Chip- & Magnetkartenleser sowie integrierter 4G-SIM-Karte ohne monatliche Grundgebühr.",
        "specs": {
            "Display": "5,0\" kapazitiver HD-Touchscreen (1280 × 720)",
            "Zahlungsarten": "NFC Kontaktlos (Apple Pay, Google Pay), Chipkarte, Magnetstreifen",
            "Konnektivität": "4G LTE (SIM-Karte inklusive), WLAN, Bluetooth, LAN",
            "Fixkosten": "Keine monatliche Grundgebühr (nur transaktionsabhängige Provision)",
            "Gewicht": "0,60 kg"
        }
    },
    {
        "id": "hk-zub-nayax",
        "sku": "HK-71",
        "name": "Nayax ONYX Terminal Bargeldlos",
        "category": "zubehoer",
        "category_label": "Bezahlsysteme & Automaten-Zubehör",
        "price": 625.32,
        "delivery_time": "Sofort verfügbar",
        "badge": "Profi-Telemetrie",
        "image": "/images/products/product-11.webp",
        "short_desc": "Kontaktloses Bezahlsystem von Nayax inkl. Kabel und Montagematerial für Honig-Kiste Automaten (Vertrag mit Nayax erforderlich, USt-IdNr. benötigt).",
        "specs": {
            "Hersteller": "Nayax GmbH",
            "Lieferumfang": "Nayax ONYX Terminal, Anschlusskabel & Montagematerial",
            "Hinweis": "Separater Servicevertrag mit Nayax (Einrichtungs-/Monatsgebühr + Provision, USt-IdNr. erforderlich)",
            "Gewicht": "2,0 kg"
        }
    },
    {
        "id": "hk-zub-akku",
        "sku": "HK-82",
        "name": "Akku-Satz 12V (2× 5200 mAh mit Füllstandsanzeige + Ladegerät)",
        "category": "zubehoer",
        "category_label": "Bezahlsysteme & Automaten-Zubehör",
        "price": 125.00,
        "delivery_time": "Sofort verfügbar",
        "badge": "Autark-Betrieb",
        "image": "/images/products/product-12.jpg",
        "short_desc": "Komplettset für den netzunabhängigen Batteriebetrieb dank Powersafe-Funktion: 2× 12V 5200 mAh Akkus (1× Betrieb, 1× Wechselakku) inkl. Ladegerät.",
        "specs": {
            "Lieferumfang": "2× Akku 12V 5200 mAh mit LED-Füllstandsanzeige, 1× Ladegerät 230V, 1× Anschlusskabel mit Stecker",
            "Gewicht": "1,0 kg"
        }
    },
    {
        "id": "hk-zub-sim-abwerk",
        "sku": "HK-96",
        "name": "SIM SMS Telemetriemodul (Einbau ab Werk)",
        "category": "zubehoer",
        "category_label": "Bezahlsysteme & Automaten-Zubehör",
        "price": 89.50,
        "delivery_time": "Sofort verfügbar",
        "badge": "Leerstand-SMS",
        "image": "/images/products/product-13.jpg",
        "short_desc": "Sendet automatisch eine SMS an deine hinterlegte Mobilfunknummer, sobald nur noch 3 Fächer im Automaten befüllt sind. Kann zudem SMS-Zahlungsinformationen auswerten.",
        "specs": {
            "Funktion": "SMS-Benachrichtigung bei ≤ 3 vollen Fächern + SMS-Zahlungsauswertung",
            "Voraussetzung": "Standard-SIM-Karte mit SMS-Funktion (deaktivierte PIN-Abfrage)",
            "Montage": "Wird bei Mitbestellung eines Automaten fertig verbaut und auf deine Rufnummer programmiert"
        }
    },
    {
        "id": "hk-zub-sim-kit",
        "sku": "HK-97",
        "name": "SIM SMS Telemetriemodul mit Arduino (Nachrüst-Kit)",
        "category": "zubehoer",
        "category_label": "Bezahlsysteme & Automaten-Zubehör",
        "price": 112.00,
        "delivery_time": "Sofort verfügbar",
        "badge": "Nachrüst-Set",
        "image": "/images/products/product-14.jpg",
        "short_desc": "Komplettes Nachrüst-Kit inklusive Arduino-Steuerung für bestehende Automaten zur SMS-Leerstandsmeldung (≤ 3 Fächer).",
        "specs": {
            "Einsatzbereich": "Nachrüstung für Bestandsautomaten",
            "Gewicht": "0,30 kg"
        }
    },
    # --- DIY BAUSÄTZE ---
    {
        "id": "hk-diy-5-master",
        "sku": "BS-43",
        "name": "DIY-Bausatz für 5 Fächer (Generation 3 – mit Webbrowser-Konfiguration)",
        "category": "bausaetze",
        "category_label": "DIY-Bausätze (Eigenbau)",
        "price": 289.00,
        "delivery_time": "ca. 3 Wochen",
        "badge": "Eigenbau Gen. 3",
        "image": "/images/products/product-15.jpg",
        "short_desc": "Kompletter Elektronik- & Verriegelungsbausatz der 3. Generation für den Eigenbau eines Honigautomaten (erweiterbar bis 45 Fächer!).",
        "specs": {
            "Hauptplatine": "1× Platine bestückt mit allen Bauteilen & ESP (Programmierung am Gerät oder per Webbrowser)",
            "Anschlussplatinen": "1× Platine für 5 Schlösser (30 cm Kabel) + 1× Platine für Taster/Display/Münzprüfer/Kartenterminal",
            "Schlösser & Taster": "5× Magnetschlösser (2 m Kabel), 1× Start-Taster LED (1 m), 2× Auswahltaster (1 m)",
            "Bedienung & Münzen": "1× Keypad-Display (1 m Kabel) + elektronischer Münzprüfer (0,20 €, 0,50 €, 1 €, 2 €)",
            "Betriebsspannung": "12V DC mit Powersafe-Funktion für Batterie-/Solarbetrieb (ohne Gehäuse & Netzteil)"
        }
    },
    {
        "id": "hk-diy-5-ext",
        "sku": "BS-44",
        "name": "Bausatz Erweiterung um 5 Fächer (5× Magnetschlösser + Platine)",
        "category": "bausaetze",
        "category_label": "DIY-Bausätze (Eigenbau)",
        "price": 99.00,
        "delivery_time": "ca. 3 Wochen",
        "badge": "+5 Türen",
        "image": "/images/products/product-16.jpg",
        "short_desc": "Erweitert den 5-Fächer-Grundbausatz um je 5 weitere Türen (bis zu 15 Türen auf dem Master-Board).",
        "specs": {
            "Lieferumfang": "5× Magnetschlösser mit 2 m Kabel + 1× Anschlussplatine für 5 Schlösser mit 30 cm Kabel",
            "Kompatibilität": "Bis zu 15 Türen pro Master- oder Slave-Board"
        }
    },
    {
        "id": "hk-diy-slave",
        "sku": "BS-45",
        "name": "Bausatz Erweiterung Slave Board (Generation 3 – für bis zu 45 Türen)",
        "category": "bausaetze",
        "category_label": "DIY-Bausätze (Eigenbau)",
        "price": 99.50,
        "delivery_time": "ca. 3 Wochen",
        "badge": "Bis 45 Fächer",
        "image": "/images/products/product-17.jpg",
        "short_desc": "Slave-Board zur Ansteuerung von bis zu 15 weiteren Türen (max. 2 Slave-Boards an einem Master-Board = 45 Fächer).",
        "specs": {
            "Lieferumfang": "1× Slave Board (Gen. 3) + 1× Verbindungskabel Master zu Slave (2 m)",
            "Maximalausbau": "2 Slave-Boards pro Master = 45 einzeln steuerbare Fächer"
        }
    },
    # --- BEECONN BIENENSTOCKWAAGEN ---
    # --- CAADEX LAGERN & ABFÜLLEN ---
]

FAQ_ITEMS = [
    {
        "q": "Was ist neu bei der 3. Generation der Honig-Kiste Automaten (ab 2026)?",
        "a": "Ab Februar 2026 werden alle Automaten in der 3. Generation ausgeliefert. Das Highlight ist die integrierte Web-Konfiguration: Du kannst Fachpreise, Einstellungen und Parameter bequem per Smartphone, Tablet oder Laptop im Webbrowser vornehmen – zusätzlich zur gewohnten Bedienung über das Zahlenfeld."
    },
    {
        "q": "Welche Fachtiefe benötige ich: 180 mm oder 240 mm?",
        "a": "Die 180-mm-Fachtiefe reicht für alle gängigen 250g- und 500g-Honiggläser (z. B. DIB-Glas, Österreichisches Imkerglas, Twist-Off) sowie Propolis und Kerzen vollkommen aus. Wenn du zusätzlich 10er-Eierkartons, Doppelpacks hintereinander oder größere Geschenkkörbe verkaufen möchtest, empfehlen wir die 240-mm-Fachtiefe (ca. 250 mm nutzbare Tiefe)."
    },
    {
        "q": "Kann ich den Automaten ohne 230V-Steckdose am Bienenstand betreiben?",
        "a": "Ja! Alle Automaten arbeiten intern mit 12V DC und verfügen über eine speziell entwickelte Powersafe-Energiesparfunktion. Mit dem optionalen 12V-Akku-Satz (inkl. Wechselakku & Ladegerät) oder einem 12V-Solarpanel lässt sich der Automat komplett autark betreiben."
    },
    {
        "q": "Wie funktioniert die Zahlung am Automaten und über den Bienenladen?",
        "a": "Am Automaten selbst ist serienmäßig ein 5-Kanal-Münzprüfer (0,10 € bis 2,00 €) verbaut. Optional kannst du im Konfigurator den NV10USB+ Geldscheinleser sowie ein bargeldloses Kartenterminal (myPOS Sigma ohne monatliche Grundgebühr oder Nayax ONYX) direkt mitbestellen. deinen Einkauf hier im Bienenladen bezahlst du sicher online über Mollie (EPS, Klarna, Kreditkarte, PayPal, Apple Pay oder SEPA)."
    },
    {
        "q": "Kostet eine individuelle RAL-Wunschfarbe Aufpreis?",
        "a": "Nein! Neben dem beliebten Klassiker (Gehäuse Rapsgelb RAL 1021 / Dach Schwarz RAL 9005) und den Sondereditionen (Anthrazit, Edelstahl, Grau) fertigen wir deinen Automaten ohne Aufpreis in deiner persönlichen RAL-Classic-Wunschfarbe für Gehäuse und Dach."
    }
]



# Convert source gross prices (19%) to Bienenladen gross prices (20%),
# preserving net prices. Round each unit price to cents.
from decimal import Decimal, ROUND_HALF_UP
VAT_RATE = Decimal("0.20")

def _austrian_gross(amount):
    return float((Decimal(str(amount)) / Decimal("1.19") * Decimal("1.20"))
                 .quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

def _convert_catalog_prices(value):
    if isinstance(value, list):
        for item in value:
            _convert_catalog_prices(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            if key == "price" and isinstance(item, (int, float)):
                value[key] = _austrian_gross(item)
            elif key == "prices_by_depth":
                value[key] = {depth: _austrian_gross(price) for depth, price in item.items()}
            else:
                _convert_catalog_prices(item)

_convert_catalog_prices(PRODUCTS)
_convert_catalog_prices(CONFIGURATOR_OPTIONS)
DEALER_INFO["vat_rate"] = float(VAT_RATE)

# Local services are already priced including 20% Austrian VAT.
# Add them after converting the manufacturer's 19% gross product prices.
CONFIGURATOR_OPTIONS["service_addons"] = [
    {
        "id": "inbetriebnahme-einschulung",
        "name": "Inbetriebnahme und Einschulung (im Bienenladen)",
        "price": 120.00,
        "description": "Inbetriebnahme und persönliche Einschulung im Bienenladen nach Terminvereinbarung."
    }
]
