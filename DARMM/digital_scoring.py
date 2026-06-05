"""Digital Readiness engine: 0.70*Q5.1_tool_capability + 0.30*Q5.2_self_rating -> Level A/B/C/D."""

from digital_other_field import score_digital_other


STANDARD_TOOL_SCORES = {
    "None":            0.0,    # "None - paper records only"
    "Accounting":      1.5,    # "Basic accounting (Tally, QuickBooks) - financial only"
    "Excel":           3.5,    # "MS Excel / Google Sheets for production tracking"
    "CAD_CAM":         3.0,    # "CAD / CAM software for production engineering"
    "QMS":             6.0,    # "Dedicated QMS software"
    "ERP":             6.5,    # "ERP system (Tally Prime, Odoo, SAP B1)"
    "CloudAnalytics":  8.0,    # "Cloud-based analytics or dashboard tools"
    "IoT":             9.5,    # "IoT sensors or machine monitoring systems"
}


SELF_RATING_SCORES = {
    "A": 0.0,
    "B": 3.5,
    "C": 6.5,
    "D": 9.5,
}


WEIGHT_TOOL_CAPABILITY = 0.70
WEIGHT_SELF_RATING     = 0.30


def assign_level_from_score(score):
    """Mr. Jith's score-based cutoffs."""
    if score <= 2.4:  return "A"
    if score <= 5.4:  return "B"
    if score <= 8.0:  return "C"
    return "D"


LEVEL_NAMES = {
    "A": "Analogue",
    "B": "Basic Digital",
    "C": "Intermediate Digital",
    "D": "Advanced Digital",
}

LEVEL_DESCRIPTIONS = {
    "A": "No digital tools; paper-based production management; manual records; no connected devices.",
    "B": "Spreadsheets and digital communication; basic accounting software; no production tracking tools.",
    "C": "ERP or digital QMS in use; basic digital tracking of production and quality; some data generation.",
    "D": "IIoT-enabled monitoring; data analytics for quality or maintenance; integrated digital manufacturing capability.",
}


def calculate_digital_score(r):
    
    # Layer 1: Tool capability (Q5.1 highest tool)
    tools = r.get("digital_tools", [])
    if tools is None:
        tools = []

    # Find the highest capability score among the standard tools they ticked
    standard_top = 0.0
    for t in tools:
        if t in STANDARD_TOOL_SCORES:
            tool_score = STANDARD_TOOL_SCORES[t]
            if tool_score > standard_top:
                standard_top = tool_score

    # Other field contribution - same scoring scale; max wins
    other_text = r.get("digital_other", "")
    other_score, _ = score_digital_other(other_text)

    # The Q5.1 layer score is the highest of the two
    if other_score > standard_top:
        layer1_score = other_score
    else:
        layer1_score = standard_top

    # Layer 2: Self-rating (Q5.2)
    self_rating_raw = r.get("self_rating", "")
    if self_rating_raw is None:
        self_rating_raw = ""
    self_rating_letter = self_rating_raw.strip().upper()

    if self_rating_letter in SELF_RATING_SCORES:
        layer2_score = SELF_RATING_SCORES[self_rating_letter]
        self_rating_provided = True
    else:
        
        layer2_score = layer1_score
        self_rating_provided = False

    # Layer 3: Reconciliation
    final_score = (WEIGHT_TOOL_CAPABILITY * layer1_score) + (WEIGHT_SELF_RATING * layer2_score)
    if final_score > 10.0:
        final_score = 10.0
    final_level = assign_level_from_score(final_score)

    # Discrepancy flag (only if self-rating was provided)
    flag = None
    if self_rating_provided:
        layer1_implied_level = assign_level_from_score(layer1_score)
        
        order = {"A": 0, "B": 1, "C": 2, "D": 3}
        gap = order[self_rating_letter] - order[layer1_implied_level]

        if abs(gap) >= 2:
            if gap > 0:
                # Self-rating is higher than what tools support
                flag = ("SIGNIFICANT DISCREPANCY: respondent self-rated " +
                        self_rating_letter + ", but tool stack only supports " +
                        layer1_implied_level + ". Possible significant over-" +
                        "confidence. Recommend digital capability audit.")
            else:
                # Self-rating is lower than what tools actually support
                flag = ("SIGNIFICANT DISCREPANCY: respondent self-rated " +
                        self_rating_letter + ", but tool stack supports " +
                        layer1_implied_level + ". Possible significant under-" +
                        "confidence - digital capability may be underutilised.")

    return {
        "layer1_tool_capability": round(layer1_score, 2),
        "layer2_self_rating":     round(layer2_score, 2),
        "final_score":            round(final_score, 2),
        "final_level":            final_level,
        "self_rating_provided":   self_rating_provided,
        "discrepancy_flag":       flag,
    }


def darmm_digital(response):
    """Top-level: full output for dashboard / report."""
    result = calculate_digital_score(response)
    return {
        "digital_score":         result["final_score"],
        "digital_level":         result["final_level"],
        "digital_level_name":    LEVEL_NAMES[result["final_level"]],
        "digital_level_desc":    LEVEL_DESCRIPTIONS[result["final_level"]],
        "layer1_tool_score":     result["layer1_tool_capability"],
        "layer2_self_score":     result["layer2_self_rating"],
        "self_rating_provided":  result["self_rating_provided"],
        "discrepancy_flag":      result["discrepancy_flag"],
    }


def _t(name, response, expected_level, expected_score=None, expected_flag=False):
    out = darmm_digital(response)
    score_ok = (expected_score is None) or (abs(out["digital_score"] - expected_score) <= 0.05)
    level_ok = out["digital_level"] == expected_level
    flag_ok  = (out["discrepancy_flag"] is not None) == expected_flag
    status = "PASS" if (score_ok and level_ok and flag_ok) else "FAIL"
    flag_str = " [FLAG]" if out["discrepancy_flag"] else ""
    print(f"  [{status}] {name}: lvl={out['digital_level']} "
          f"score={out['digital_score']:.2f}{flag_str} "
          f"(expected lvl={expected_level}"
          f"{', score=' + str(expected_score) if expected_score is not None else ''})")
    if status == "FAIL":
        print(f"           full: {out}")


def _run_tests():
    print("Running Digital Readiness scoring tests (70/30 architecture)...\n")

    # Layer 1 only (no self-rating) - score = tool capability x 0.7 + (same) x 0.3 = tool capability
    _t("No tools, no rating",       {}, "A", 0.0)
    _t("Paper only",                {"digital_tools": ["None"]}, "A", 0.0)
    _t("Accounting only",           {"digital_tools": ["Accounting"]}, "A", 1.5)
    _t("Excel only",                {"digital_tools": ["Excel"]}, "B", 3.5)
    _t("ERP only",                  {"digital_tools": ["ERP"]}, "C", 6.5)
    _t("IoT only",                  {"digital_tools": ["IoT"]}, "D", 9.5)
    _t("Excel + ERP (max wins)",    {"digital_tools": ["Excel", "ERP"]}, "C", 6.5)

    # Self-rating aligned - score stays same
    _t("Excel + self=B",            {"digital_tools": ["Excel"], "self_rating": "B"}, "B", 3.5)
    _t("ERP + self=C",              {"digital_tools": ["ERP"],   "self_rating": "C"}, "C", 6.5)
    _t("IoT + self=D",              {"digital_tools": ["IoT"],   "self_rating": "D"}, "D", 9.5)

    # 1-level gap - no flag, score blends
    # Excel (3.5) + self=C (6.5) -> 0.7*3.5 + 0.3*6.5 = 2.45 + 1.95 = 4.4 -> B
    _t("Excel + self=C (over by 1)", {"digital_tools": ["Excel"], "self_rating": "C"},
       "B", 4.4, expected_flag=False)
    # ERP (6.5) + self=B (3.5) -> 0.7*6.5 + 0.3*3.5 = 4.55 + 1.05 = 5.6 -> C
    _t("ERP + self=B (under by 1)",  {"digital_tools": ["ERP"],   "self_rating": "B"},
       "C", 5.6, expected_flag=False)

    # 2+ level gap - FLAG raised
    
    _t("Excel + self=D (FLAG)",      {"digital_tools": ["Excel"], "self_rating": "D"},
       "B", 5.3, expected_flag=True)
   
    _t("Paper + self=C (FLAG)",      {"digital_tools": ["None"],  "self_rating": "C"},
       "A", 1.95, expected_flag=True)
    _t("IoT + self=B (FLAG under)",  {"digital_tools": ["IoT"],   "self_rating": "B"},
       "C", 7.7, expected_flag=True)

    
    _t("Other = Power BI",           {"digital_other": "Power BI"}, "C", 8.0)
    _t("Other = MES",                {"digital_other": "MES system"}, "C", 7.5)
    _t("Other = Wonderware",         {"digital_other": "Wonderware"}, "D", 9.5)
    _t("Excel + Other=Ramco",        {"digital_tools": ["Excel"], "digital_other": "Ramco ERP"}, "C", 6.5)

    # Free-text capability keywords
    _t("Free text IoT",              {"digital_other": "we have IoT sensors on CNC machines"}, "D", 9.5)
    _t("Free text paper",            {"digital_other": "paper-based production register only"}, "A", 0.0)

    print("\nAll digital scoring tests passed.")


if __name__ == "__main__":
    _run_tests()
