

NAMED_TOOLS = {

    # Indian-market ERP and accounting (Cat A/B/C boundary)
    "tallyprime with production": (6.5, "TallyPrime with manufacturing module"),
    "tally prime with production": (6.5, "TallyPrime with manufacturing module"),
    "tally prime production":     (6.5, "TallyPrime with manufacturing module"),
    "tally erp 9":                (2.0, "Tally ERP 9 financial-only (A/B boundary)"),
    "tally prime":                (2.0, "Tally Prime financial-only (A/B boundary)"),
    "tally":                      (2.0, "Tally accounting (A/B boundary)"),
    "busy":                       (3.5, "Busy accounting software (Level B)"),
    "marg":                       (3.5, "Marg accounting software (Level B)"),
    "vyapar":                     (3.5, "Vyapar accounting (Level B)"),
    "focus erp":                  (6.5, "Focus ERP Indian mid-market (Level C)"),
    "wings erp":                  (6.5, "Wings ERP Indian mid-market (Level C)"),
    "ramco erp":                  (6.5, "Ramco ERP Indian mid-market (Level C)"),
    "ramco":                      (6.5, "Ramco ERP (Level C)"),
    "gofrugal":                   (5.0, "GoFrugal ERP (B-C boundary)"),
    "odoo":                       (6.5, "Odoo ERP open-source (Level C)"),
    "sap business one":           (6.5, "SAP B1 SME ERP (Level C)"),
    "sap b1":                     (6.5, "SAP B1 SME ERP (Level C)"),
    "sap b one":                  (6.5, "SAP B1 SME ERP (Level C)"),
    "sap s/4hana":                (7.5, "SAP S/4HANA enterprise ERP (C-D boundary)"),
    "s/4hana":                    (7.5, "SAP S/4HANA enterprise ERP (C-D boundary)"),
    "microsoft dynamics":         (6.5, "Microsoft Dynamics ERP (Level C)"),
    "ms dynamics":                (6.5, "Microsoft Dynamics ERP (Level C)"),
    "netsuite":                   (6.5, "NetSuite ERP (Level C)"),

    # Quality Management Systems
    "qmax":                       (6.5, "Qmax dedicated QMS (Level C)"),
    "mastercontrol":              (6.5, "MasterControl QMS (Level C)"),
    "etq":                        (6.5, "ETQ QMS (Level C)"),
    "intelex":                    (6.5, "Intelex cloud QMS (Level C)"),
    "isotracker":                 (6.5, "ISOTracker QMS (Level C)"),
    "iso tracker":                (6.5, "ISOTracker QMS (Level C)"),
    "excel qms":                  (3.5, "Excel-based QMS template (Level B)"),

    # Statistical / Six Sigma analytics software
    "minitab":                    (7.5, "Minitab statistical software (C-D)"),
    "jmp":                        (7.5, "JMP statistical software (C-D)"),
    "spss":                       (7.5, "SPSS statistical software (C-D)"),

    # Production tracking / SCADA / MES
    "wonderware":                 (9.5, "Wonderware SCADA (Level D)"),
    "aveva":                      (9.5, "AVEVA SCADA platform (Level D)"),
    "ignition scada":             (9.5, "Ignition SCADA/MES (Level D)"),
    "ignition":                   (9.5, "Ignition SCADA/MES (Level D)"),
    "aveva edge":                 (9.5, "Aveva Edge SCADA (Level D)"),
    "tulip":                      (8.0, "Tulip manufacturing apps (C-D)"),
    "oee software":               (6.5, "Dedicated OEE software (Level C)"),
    "oee dashboard":              (6.5, "Automated OEE dashboard (Level C)"),
    "mes":                        (7.5, "Manufacturing Execution System (C-D)"),
    "manufacturing execution":    (7.5, "MES written out (C-D)"),
    "cmms":                       (6.0, "Computerised Maintenance Mgmt (Level C)"),

    # Analytics, BI, cloud
    "power bi":                   (8.0, "Power BI dashboards (C-D)"),
    "tableau":                    (8.0, "Tableau analytics (C-D)"),
    "qlik":                       (8.0, "Qlik analytics (C-D)"),
    "looker studio":              (6.5, "Google Looker Studio dashboard (Level C)"),
    "looker":                     (6.5, "Looker dashboard (Level C)"),
    "google workspace":           (4.0, "Google Workspace productivity (Level B)"),
    "microsoft 365":              (4.0, "Microsoft 365 productivity (Level B)"),
    "ms 365":                     (4.0, "Microsoft 365 productivity (Level B)"),
    "office 365":                 (4.0, "Office 365 productivity (Level B)"),

    # Communication tools (low score - not production data)
    "whatsapp business":          (2.5, "WhatsApp Business comms (Level B - comms only)"),
    "whatsapp":                   (2.5, "WhatsApp comms (Level B - comms only)"),
    "telegram":                   (2.5, "Telegram groups comms (Level B)"),
    "ms teams":                   (2.5, "MS Teams comms (Level B)"),
    "microsoft teams":            (2.5, "MS Teams comms (Level B)"),
    "slack":                      (2.5, "Slack comms (Level B)"),

    # CAD / CAM engineering
    "autocad":                    (3.5, "AutoCAD design software (Level B for quality)"),
    "solidworks":                 (3.5, "SolidWorks design software (Level B for quality)"),
    "creo":                       (3.5, "Creo design software (Level B for quality)"),
    "catia":                      (4.5, "CATIA advanced design (B-C boundary)"),
    "cam software":               (3.5, "CAM/CNC programming software (Level B)"),
    "cad/cam":                    (3.5, "CAD/CAM combined (Level B)"),
    "cad cam":                    (3.5, "CAD/CAM combined (Level B)"),
}

CAPABILITY_KEYWORDS = {
    # Tier D signals
    "iiot":                  (9.5, "IIoT keyword - Level D"),
    "iot":                   (9.5, "IoT keyword - Level D"),
    "sensor":                (9.5, "Sensor keyword - Level D"),
    "real-time monitoring":  (9.5, "Real-time monitoring - Level D"),
    "real time monitoring":  (9.5, "Real-time monitoring - Level D"),

    # Tier C-D signals
    "cloud":                 (8.0, "Cloud-based - C/D boundary"),
    "automated dashboard":   (8.0, "Automated dashboard - C/D"),
    "live data":             (8.0, "Live data feed - C/D"),
    "live dashboard":        (8.0, "Live dashboard - C/D"),

    # Tier C signals
    "erp":                   (6.5, "ERP keyword - Level C"),
    "production tracking":   (6.5, "Production tracking - Level C"),
    "production system":     (6.5, "Production system - Level C"),

    # Tier B signals
    "excel":                 (3.5, "Excel - Level B"),
    "spreadsheet":           (3.5, "Spreadsheet - Level B"),
    "google sheets":         (3.5, "Google Sheets - Level B"),
    "google form":           (3.5, "Google Forms data capture - Level B"),

    # Tier B (comms only)
    "mobile app":            (2.5, "Mobile app comms - Level B comms"),

    # Tier A signals
    "paper":                 (0.0, "Paper records - Level A"),
    "manual":                (0.0, "Manual records - Level A"),
    "register":              (0.0, "Paper register - Level A"),
    "logbook":               (0.0, "Logbook - Level A"),
    "log book":              (0.0, "Log book - Level A"),
}


def classify_one_entry(raw_text):
    
    text = raw_text.strip().lower()
    if not text:
        return (0.0, "Empty entry")

   
    best_score = -1.0
    best_keyword = None
    best_notes = None
    for keyword, (score, notes) in NAMED_TOOLS.items():
        if keyword in text:
            if score > best_score:
                best_score = score
                best_keyword = keyword
                best_notes = notes

    if best_keyword is not None:
        return (best_score, "Matched named tool '" + best_keyword + "': " + best_notes)

    # 2. Capability-keyword fallback (highest score wins)
    best_score = -1.0
    best_keyword = None
    best_notes = None
    for keyword, (score, notes) in CAPABILITY_KEYWORDS.items():
        if keyword in text:
            if score > best_score:
                best_score = score
                best_keyword = keyword
                best_notes = notes

    if best_keyword is not None:
        return (best_score, "Capability keyword '" + best_keyword + "': " + best_notes)

    # 3. Default
    return (0.0, "FLAG: unrecognised entry '" + raw_text + "' - reviewer to assess")


def score_digital_other(raw_text):
   
    if not raw_text or not raw_text.strip():
        return (0.0, [])

    # Split the raw text on commas and semicolons
    text_with_commas = raw_text.replace(";", ",")
    entries = []
    for chunk in text_with_commas.split(","):
        chunk = chunk.strip()
        if chunk:
            entries.append(chunk)

    breakdown = []
    max_score = 0.0

    for entry in entries:
        score, notes = classify_one_entry(entry)
        breakdown.append({
            "entry":             entry,
            "capability_score":  score,
            "notes":             notes,
        })
        if score > max_score:
            max_score = score

    return (max_score, breakdown)


def _t(name, raw_text, expected_score):
    score, _ = score_digital_other(raw_text)
    status = "PASS" if abs(score - expected_score) <= 0.01 else "FAIL"
    print(f"  [{status}] {name}: '{raw_text}' -> {score:.1f} (expected {expected_score})")


def _run_tests():
    print("Running Digital Other-field classifier tests...\n")

    # Empty / default
    _t("Empty",                   "",                              0.0)
    _t("Unknown",                 "XYZ proprietary thing",         0.0)

    # Indian ERPs
    _t("TallyPrime with prod",    "TallyPrime with production module", 6.5)
    _t("Tally financial-only",    "Tally Prime",                   2.0)
    _t("Ramco ERP",               "Ramco ERP",                     6.5)
    _t("Odoo",                    "Odoo ERP",                      6.5)
    _t("SAP B1",                  "SAP Business One",              6.5)
    _t("Busy accounting",         "Busy",                          3.5)
    _t("GoFrugal",                "GoFrugal ERP",                  5.0)

    # QMS
    _t("MasterControl",           "MasterControl QMS",             6.5)
    _t("Intelex",                 "Intelex",                       6.5)

    # Stats software
    _t("Minitab",                 "Minitab",                       7.5)
    _t("SPSS",                    "SPSS for capability studies",   7.5)

    # SCADA / MES
    _t("Wonderware",              "Wonderware",                    9.5)
    _t("Ignition SCADA",          "Ignition SCADA",                9.5)
    _t("Tulip",                   "Tulip manufacturing apps",      8.0)
    _t("MES",                     "MES system",                    7.5)

    # BI / cloud
    _t("Power BI",                "Power BI",                      8.0)
    _t("Tableau",                 "Tableau",                       8.0)
    _t("Looker",                  "Google Looker Studio",          6.5)

    # Comms tools
    _t("WhatsApp",                "WhatsApp Business",             2.5)
    _t("Telegram",                "Telegram groups",               2.5)

    # CAD
    _t("AutoCAD",                 "AutoCAD",                       3.5)
    _t("CATIA",                   "CATIA",                         4.5)

    # Capability keywords (free text)
    _t("IoT keyword",             "we have IoT sensors on CNC",    9.5)
    _t("cloud keyword",           "cloud-based live production dashboard", 8.0)
    _t("ERP keyword fallback",    "in-house developed production system",  6.5)
    _t("Excel keyword",           "we track in Excel and Google Forms",    3.5)
    _t("paper keyword",           "paper-based production register",       0.0)

    # Multiple tools - max wins
    _t("Tableau + WhatsApp",      "Tableau and WhatsApp",          8.0)
    _t("Power BI, Excel, Tally",  "Power BI, Excel, Tally Prime",  8.0)

    print("\nDone.")


if __name__ == "__main__":
    _run_tests()
