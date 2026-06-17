
OTHER_CAP = 2.0

OTHER_FIELD_LOOKUP = {
    # Q3.2 Lean - Category A (legitimate Lean tools)
    "tpm":                 ("A", 1.0, None, "Total Productive Maintenance"),
    "total productive":    ("A", 1.0, None, "TPM written in full"),
    "smed":                ("A", 1.0, None, "Single Minute Exchange of Die"),
    "single minute":       ("A", 1.0, None, "SMED written in full"),
    "a3":                  ("A", 1.0, None, "A3 problem solving"),
    "gemba":               ("A", 1.0, None, "Gemba walk - management observation"),
    "oee":                 ("A", 1.0, None, "Overall Equipment Effectiveness tracking"),
    "heijunka":            ("A", 1.2, None, "Production levelling - advanced, L4 signal"),
    "jidoka":              ("A", 1.0, None, "Build-in quality / autonomation"),
    "hoshin":              ("A", 1.2, None, "Hoshin Kanri policy deployment - L4-L5 signal"),
    "andon":               ("A", 1.0, None, "Real-time visual alert system"),
    "milk run":            ("A", 1.0, None, "Structured internal logistics"),

    # Q3.2 Lean - Category B 
    "6s":                  ("B", 0.0, "5S",                          "Re-wording of 5S with safety element"),
    "workplace organisation": ("B", 0.0, "5S",                       "Re-wording of 5S"),
    "workplace organization": ("B", 0.0, "5S",                       "Re-wording of 5S"),
    
    
    "housekeeping":        ("D", 0.3, None, "Basic cleaning discipline, not 5S unless zones/colour coding mentioned"),
    "error proof":         ("B", 0.0, "PokayYoke",                   "Re-wording of Poka-Yoke"),
    "error-proof":         ("B", 0.0, "PokayYoke",                   "Re-wording of Poka-Yoke"),
    "mistake proof":       ("B", 0.0, "PokayYoke",                   "Re-wording of Poka-Yoke"),
    "fool proof":          ("B", 0.0, "PokayYoke",                   "Re-wording of Poka-Yoke"),
    "pokayoke":            ("B", 0.0, "PokayYoke",                   "Spelling variant of Poka-Yoke"),
    "poka yoke":           ("B", 0.0, "PokayYoke",                   "Spelling variant of Poka-Yoke"),
    "pull system":         ("B", 0.0, "Kanban",                      "Re-wording of Kanban"),
    "pull production":     ("B", 0.0, "Kanban",                      "Re-wording of Kanban"),
    "ci event":            ("B", 0.0, "Kaizen",                      "Continuous Improvement = Kaizen"),
    "continuous improvement": ("B", 0.0, "Kaizen",                   "Continuous Improvement = Kaizen"),
    "improvement workshop": ("B", 0.0, "Kaizen",                     "Kaizen event"),
    "sop":                 ("B", 0.0, "StandardWork",                "SOP = Standard Work"),
    "standard operating":  ("B", 0.0, "StandardWork",                "SOP = Standard Work"),
    "work instruction":    ("B", 0.0, "StandardWork",                "Standard Work documentation"),
    "process map":         ("B", 0.0, "VSM",                         "Process mapping = VSM"),
    "flow map":            ("B", 0.0, "VSM",                         "Flow mapping = VSM"),
    "value stream":        ("B", 0.0, "VSM",                         "VSM written in full"),
    "shadow board":        ("B", 0.0, "VisualManagement",            "Component of Visual Management"),
    "visual control":      ("B", 0.0, "VisualManagement",            "Component of Visual Management"),
    "visual factory":      ("B", 0.0, "VisualManagement",            "Component of Visual Management"),

    # Q3.2 Lean - Category C (quality systems)
    "iso 9001":            ("C", 0.6, None, "Quality management standard, not Lean tool"),
    "iso9001":             ("C", 0.6, None, "Quality management standard, not Lean tool"),
    "iatf":                ("C", 0.8, None, "Automotive QMS - more LSS overlap"),
    "ts 16949":            ("C", 0.8, None, "Predecessor of IATF 16949"),
    "as9100":              ("C", 0.8, None, "Aerospace QMS - high process discipline"),
    "ppap":                ("C", 0.7, None, "Part qualification, automotive OEM context"),
    "apqp":                ("C", 0.7, None, "Quality planning framework"),
    "8d":                  ("C", 0.7, None, "Reactive structured problem solving"),
    "eight discipline":    ("C", 0.7, None, "8D Report written in full"),
    "capa":                ("C", 0.6, None, "Corrective/Preventive Action - QMS element"),
    "corrective and preventive": ("C", 0.6, None, "CAPA written in full"),
    "qcdm":                ("C", 0.5, None, "Indian OEM supplier KPI framework"),
    "qcds":                ("C", 0.5, None, "Indian OEM supplier KPI framework"),

    # Q3.2 Lean - Category D (good practice, not Lean)
    "daily meeting":       ("D", 0.3, None, "Communication tool, not Lean"),
    "morning meeting":     ("D", 0.3, None, "Communication tool, not Lean"),
    "cleaning schedule":   ("D", 0.3, None, "Prerequisite for 5S but not 5S itself"),
    "inspection checklist": ("D", 0.3, None, "End-of-line inspection, traditional"),
    "quality checklist":   ("D", 0.3, None, "End-of-line inspection, traditional"),
    "preventive maintenance": ("D", 0.3, None, "Good practice but not TPM"),
    "production planning": ("D", 0.3, None, "Basic scheduling, not Heijunka"),
    "inventory management": ("D", 0.3, None, "Stock tracking, not Kanban"),
    "safety training":     ("D", 0.3, None, "Legal requirement, not Lean"),

    # Q3.4 Six Sigma - Category A (legitimate SS tools)
    "sipoc":               ("A", 0.8, None, "Define-phase scoping tool, L3 signal"),
    "pareto":              ("A", 0.8, None, "Data-based prioritisation"),
    "run chart":           ("A", 0.6, None, "Simpler than SPC, basic trend analysis"),
    "doe":                 ("A", 1.2, None, "Design of Experiments, L4-L5 signal"),
    "design of experiment": ("A", 1.2, None, "DOE written in full"),
    "msa":                 ("A", 1.0, None, "Measurement System Analysis, L4"),
    "gauge r&r":           ("A", 1.0, None, "Gauge Repeatability and Reproducibility, L4"),
    "gage r&r":            ("A", 1.0, None, "Gauge R&R spelling variant"),
    "hypothesis test":     ("A", 1.0, None, "Statistical inference, L4"),
    "t-test":              ("A", 1.0, None, "Statistical inference, L4"),
    "anova":               ("A", 1.0, None, "Analysis of Variance, L4"),
    "regression":          ("A", 1.0, None, "Statistical modelling, L4-L5"),
    "dmadv":               ("A", 1.2, None, "Design for Six Sigma, L5 signal"),
    "dfss":                ("A", 1.2, None, "Design for Six Sigma, L5 signal"),
    "voc":                 ("A", 0.8, None, "Voice of Customer, Define-phase input"),
    "voice of customer":   ("A", 0.8, None, "VOC written in full"),
    "qfd":                 ("A", 1.2, None, "Quality Function Deployment, L4-L5"),
    "house of quality":    ("A", 1.2, None, "QFD primary tool"),

    # Q3.4 Six Sigma - Category B (re-wordings - map to standard)
    "fishbone":            ("B", 0.0, "RCA",         "Fishbone = Ishikawa = RCA"),
    "ishikawa":            ("B", 0.0, "RCA",         "Ishikawa = RCA"),
    "cause and effect":    ("B", 0.0, "RCA",         "Cause-effect diagram = RCA"),
    "cause-and-effect":    ("B", 0.0, "RCA",         "Cause-effect diagram = RCA"),
    "5 why":               ("B", 0.0, "RCA",         "5 Whys = RCA (already listed)"),
    "5 whys":              ("B", 0.0, "RCA",         "5 Whys = RCA (already listed)"),
    "why-why":             ("B", 0.0, "RCA",         "Why-why analysis = RCA"),
    "statistical control": ("B", 0.0, "SPC",         "Statistical Process Control"),
    "control chart":       ("B", 0.0, "SPC",         "Control charts = SPC"),
    "control limit":       ("B", 0.0, "SPC",         "Control limits = SPC"),
    "process control":     ("B", 0.0, "SPC",         "Process Control = SPC"),
    "cpk":                 ("B", 0.0, "Cpk",         "Process Capability Index"),
    "cp ":                 ("B", 0.0, "Cpk",         "Capability index Cp"),
    "capability index":    ("B", 0.0, "Cpk",         "Cp/Cpk capability index"),
    "process capability":  ("B", 0.0, "Cpk",         "Process Capability = Cpk"),
    "sigma level":         ("B", 0.0, "Cpk",         "Sigma level calculation"),
    "pfmea":               ("B", 0.0, "FMEA",        "Process FMEA = FMEA"),
    "process fmea":        ("B", 0.0, "FMEA",        "Process FMEA = FMEA"),
    "failure mode":        ("B", 0.0, "FMEA",        "Failure Mode Effects = FMEA"),
    "risk analysis":       ("B", 0.0, "FMEA",        "Risk analysis in process context = FMEA"),

    # Q3.4 Six Sigma - Category C (adjacent methods)
    "pdca":                ("C", 0.6, None, "Improvement cycle, broader than SS, L2-L3"),
    "plan-do-check":       ("C", 0.6, None, "PDCA written in full"),
    "deming":              ("C", 0.6, None, "Deming cycle = PDCA"),
    "control plan":        ("C", 0.6, None, "Required by IATF 16949, links to SPC"),
    "minitab":             ("C", 0.7, None, "Statistical software implies SS tool usage"),
    "clair":               ("C", 0.5, None, "Indian automotive complaint tracking"),
    "arena":               ("C", 1.0, None, "Simulation software, L4-L5 practice"),
    "simul8":              ("C", 1.0, None, "Simulation software, L4-L5 practice"),

    # Both questions - Category D and E
    "excel":               ("D", 0.3, None, "Excel alone does not indicate SS analysis"),
    "sap":                 ("D", 0.3, None, "ERP module - data capture, not analysis"),
    "erp":                 ("D", 0.3, None, "ERP - data capture, not analysis"),
    "our own system":      ("E", 0.3, None, "FLAG: too vague - reviewer to assess"),

    "our own":             ("E", 0.3, None, "FLAG: 'our own' phrasing - reviewer to assess"),
    "not formal":          ("E", 0.3, None, "FLAG: respondent distinguishes from formal tool"),
    "internal procedure":  ("E", 0.3, None, "FLAG: too vague - reviewer to assess"),
    "internal process":    ("E", 0.3, None, "FLAG: too vague - reviewer to assess"),
    "company procedure":   ("E", 0.3, None, "FLAG: too vague - reviewer to assess"),
    "internal qc":         ("E", 0.3, None, "FLAG: too vague - reviewer to assess"),
}



def classify_one_entry(raw_text):
    
    text = raw_text.strip().lower()
    if not text:
        return ("E", 0.0, None, "Empty entry")

    best_length = 0
    best_match = None
    for keyword, (cat, weight, maps_to, notes) in OTHER_FIELD_LOOKUP.items():
        if keyword in text:
            if len(keyword) > best_length:
                best_length = len(keyword)
                best_match = (keyword, cat, weight, maps_to, notes)

    if best_match is not None:
        keyword, cat, weight, maps_to, notes = best_match
        return (cat, weight, maps_to, "Matched '" + keyword + "': " + notes)

    # No keyword matched - flag for human review
    return ("E", 0.3, None, "FLAG: unrecognised entry '" + raw_text + "' - reviewer to assess")



def score_other_field(raw_text, already_ticked_tools=None):
    
    if not raw_text or not raw_text.strip():
        return (0.0, [])

    # Default the already-ticked list to empty if the caller didn't pass one
    if already_ticked_tools is None:
        already_ticked_tools = []
    already_ticked = set(already_ticked_tools)

    
    text_with_commas = raw_text.replace(";", ",")
    entries = []
    for chunk in text_with_commas.split(","):
        chunk = chunk.strip()
        if chunk:
            entries.append(chunk)

    breakdown = []
    raw_total = 0.0

    for entry in entries:
        cat, weight, maps_to, notes = classify_one_entry(entry)

        actual_weight = weight
        if cat == "B":
            if maps_to in already_ticked:
                actual_weight = 0.0
                notes += " | already ticked, no double-count"
            else:
                actual_weight = 1.0
                notes += " | tool not ticked, crediting as standard"

        breakdown.append({
            "entry": entry,
            "category": cat,
            "weight": actual_weight,
            "maps_to": maps_to,
            "notes": notes,
        })
        raw_total += actual_weight

    # Apply the hard cap (Principle 2)
    capped_total = min(raw_total, OTHER_CAP)
    if raw_total > OTHER_CAP:
        breakdown.append({
            "entry": "[CAP APPLIED]",
            "category": "-",
            "weight": -(raw_total - OTHER_CAP),
            "maps_to": None,
            "notes": f"Raw total {raw_total:.1f} capped at {OTHER_CAP}",
        })

    return (capped_total, breakdown)



def _t(name, raw_text, already_ticked, expected_score):
    score, breakdown = score_other_field(raw_text, already_ticked)
    status = "PASS" if abs(score - expected_score) < 0.01 else "FAIL"
    print(f"  [{status}] {name}: '{raw_text}' -> {score:.1f} (expected {expected_score})")
    if status == "FAIL":
        for b in breakdown:
            print(f"           {b}")


def _run_tests():
    print("Running Other-field classifier tests...\n")

    _t("Empty box",            "",                          [], 0.0)
    _t("Single Cat A (TPM)",   "TPM",                       [], 1.0)
    _t("Advanced Cat A (DOE)", "DOE",                       [], 1.2)
    _t("Cat B already ticked", "Pokayoke",                  ["PokayYoke"], 0.0)
    _t("Cat B NOT ticked",     "Error-proofing",            [], 1.0)
    _t("Cat C (ISO 9001)",     "ISO 9001",                  [], 0.6)
    _t("Cat D (cleaning)",     "Cleaning schedule",         [], 0.3)
    _t("Cat E (our system)",   "Our own system",            [], 0.3)
    _t("Unknown -> Cat E",     "XYZ proprietary tool",      [], 0.3)
    _t("Multiple tools",       "TPM, SMED, A3",             [], 2.0)  # 3.0 capped at 2.0
    _t("Cap kicks in",         "TPM, SMED, A3, Heijunka",   [], 2.0)  # 4.2 capped at 2.0
    _t("Mixed cats (no split)", "ISO 9001 and daily meeting",[], 0.3)
    _t("Variant spelling",     "poka yoke",                 [], 1.0)  # not ticked

    print("\nDone.")


if __name__ == "__main__":
    _run_tests()
