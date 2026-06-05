"""LSS scoring engine: converts a survey response dict into a score (0-20+) and L1-L5 level."""

from lss_other_field import score_other_field


WEIGHTS = {
    "lean_awareness":       2,
    "ss_awareness":         1,
    "knowledge_level":      1,
    "lean_implemented":     1,
    "lean_tool":            1,
    "ss_implemented":       1,
    "ss_tool":              1,
    "real_motivation":      1,
    "real_benefit":         1,
}

LEAN_TOOL_KEYS = ["5S", "Kaizen", "VSM", "Kanban", "PokayYoke",
                  "VisualManagement", "StandardWork"]

SS_TOOL_KEYS = ["DMAIC", "SPC", "FMEA", "RCA", "Cpk"]


def calculate_lss_score(r):
    """Compute LSS score from a response dict. Returns integer 0..24."""
    A = (WEIGHTS["lean_awareness"] * int(r.get("lean_awareness", 0))
         + WEIGHTS["ss_awareness"] * int(r.get("ss_awareness", 0))
         + WEIGHTS["knowledge_level"] * int(r.get("knowledge_level", 1)))

    lean_tools = r.get("lean_tools", [])
    B_std = WEIGHTS["lean_implemented"] * int(r.get("lean_implemented", 0))
    for tool in lean_tools:
        if tool in LEAN_TOOL_KEYS:
            B_std += WEIGHTS["lean_tool"]

    lean_other_score, _ = score_other_field(
        r.get("lean_other", ""),
        already_ticked_tools=lean_tools,
    )
    B = B_std + lean_other_score

    ss_tools = r.get("ss_tools", [])
    C_std = WEIGHTS["ss_implemented"] * int(r.get("ss_implemented", 0))
    for tool in ss_tools:
        if tool in SS_TOOL_KEYS:
            C_std += WEIGHTS["ss_tool"]

    ss_other_score, _ = score_other_field(
        r.get("ss_other", ""),
        already_ticked_tools=ss_tools,
    )
    C = C_std + ss_other_score

    D = 0
    mot = str(r.get("primary_motivation", "")).strip().lower()
    ben = str(r.get("benefits_observed", "")).strip().lower()
    if mot and mot != "not applicable":
        D += WEIGHTS["real_motivation"]
    if ben and ben != "not applicable":
        D += WEIGHTS["real_benefit"]

    return int(round(A + B + C + D))


def assign_lss_level(score):
    """Map score to (level_code, level_name). Cutoffs: L1<=2, L2<=9, L3<=13, L4<=17, L5>17."""
    if score <= 2:    return ("L1", "Unaware")
    elif score <= 9:  return ("L2", "Aware, Inactive")
    elif score <= 13: return ("L3", "Partially Adopting")
    elif score <= 17: return ("L4", "Structured Implementation")
    else:              return ("L5", "Integrated and Sustainable")


LSS_LEVEL_DESCRIPTIONS = {
    "L1": "No LSS knowledge; no formal quality procedures; reactive problem-solving only; no performance metrics tracked.",
    "L2": "Heard of LSS or 5S; interest expressed; no tools implemented; quality by inspection not prevention.",
    "L3": "1-2 Lean tools implemented (typically 5S); improvement localised and not sustained; basic measurement absent.",
    "L4": "Multiple tools deployed systematically; basic Six Sigma awareness; management-initiated projects; data collection begun.",
    "L5": "LSS embedded in operational culture; DMAIC routine; KPIs reviewed regularly; continuous improvement in management cadence.",
}


def darmm_lss(response):
    """Top-level: return score + level + breakdown for the dashboard."""
    score = calculate_lss_score(response)
    level, name = assign_lss_level(score)

    _, lean_breakdown = score_other_field(
        response.get("lean_other", ""),
        already_ticked_tools=response.get("lean_tools", []),
    )
    _, ss_breakdown = score_other_field(
        response.get("ss_other", ""),
        already_ticked_tools=response.get("ss_tools", []),
    )

    return {
        "lss_score":           score,
        "lss_level":           level,
        "lss_level_name":      name,
        "lss_level_desc":      LSS_LEVEL_DESCRIPTIONS[level],
        "lean_other_breakdown": lean_breakdown,
        "ss_other_breakdown":   ss_breakdown,
    }


def _test_all_minimum_yields_L1():
    r = {"knowledge_level": 1}
    out = darmm_lss(r)
    assert out["lss_score"] == 1, out
    assert out["lss_level"] == "L1", out
    print("  PASS  All-minimum response -> L1")


def _test_all_maximum_yields_L5():
    r = {
        "lean_awareness": 1, "ss_awareness": 1, "knowledge_level": 4,
        "lean_implemented": 1, "lean_tools": LEAN_TOOL_KEYS,
        "ss_implemented": 1, "ss_tools": SS_TOOL_KEYS,
        "primary_motivation": "Cost reduction",
        "benefits_observed":  "Reduced defects and rework",
    }
    out = darmm_lss(r)
    # Score = 7 + (1+7) + (1+5) + 2 = 23 -> L5
    assert out["lss_score"] == 23, out
    assert out["lss_level"] == "L5", out
    print("  PASS  All-maximum response -> L5")


def _test_aware_but_no_tools_yields_L2():
    r = {"lean_awareness": 1, "ss_awareness": 1, "knowledge_level": 2}
    out = darmm_lss(r)
    # Score = 2 + 1 + 2 = 5 -> L2
    assert out["lss_score"] == 5, out
    assert out["lss_level"] == "L2", out
    print("  PASS  Aware-only response -> L2")


def _test_5S_kaizen_user_yields_L3():
    r = {
        "lean_awareness": 1, "ss_awareness": 1, "knowledge_level": 3,
        "lean_implemented": 1, "lean_tools": ["5S", "Kaizen"],
        "primary_motivation": "Quality improvement",
        "benefits_observed":  "Reduced defects",
    }
    out = darmm_lss(r)
    assert out["lss_score"] == 11, out
    assert out["lss_level"] == "L3", out
    print("  PASS  5S+Kaizen adopter -> L3")


def _test_structured_six_sigma_yields_L4():
    r = {
        "lean_awareness": 1, "ss_awareness": 1, "knowledge_level": 3,
        "lean_implemented": 1, "lean_tools": ["5S", "Kaizen", "VSM"],
        "ss_implemented":   1, "ss_tools":   ["DMAIC", "SPC"],
        "primary_motivation": "OEM pressure",
        "benefits_observed":  "Lower costs",
    }
    out = darmm_lss(r)
    assert out["lss_score"] == 15, out
    assert out["lss_level"] == "L4", out
    print("  PASS  Structured Six Sigma user -> L4")


def _test_other_field_lifts_score():
    r = {
        "lean_awareness": 1, "ss_awareness": 1, "knowledge_level": 3,
        "lean_implemented": 1, "lean_tools": ["5S", "Kaizen"],
        "lean_other": "TPM",
        "primary_motivation": "Quality improvement",
        "benefits_observed":  "Reduced defects",
    }
    out = darmm_lss(r)
    assert out["lss_score"] == 12, out
    assert out["lss_level"] == "L3", out
    print("  PASS  Other-field TPM adds 1 point")


def _test_other_field_cap_holds():
    r = {
        "lean_awareness": 1, "ss_awareness": 1, "knowledge_level": 3,
        "lean_implemented": 1, "lean_tools": ["5S"],
        "lean_other": "TPM, SMED, A3, Gemba, OEE",
    }
    out = darmm_lss(r)
    assert out["lss_score"] == 10, out
    print("  PASS  Other-field cap held at 2.0")


def _test_cat_b_rewording_no_double_count():
    r = {
        "lean_awareness": 1, "knowledge_level": 2,
        "lean_implemented": 1, "lean_tools": ["5S"],
        "lean_other": "Workplace organisation",
    }
    out = darmm_lss(r)
    assert out["lss_score"] == 6, out
    print("  PASS  Cat B re-wording does not double-count")


def _run_tests():
    print("Running LSS scoring unit tests...")
    _test_all_minimum_yields_L1()
    _test_all_maximum_yields_L5()
    _test_aware_but_no_tools_yields_L2()
    _test_5S_kaizen_user_yields_L3()
    _test_structured_six_sigma_yields_L4()
    _test_other_field_lifts_score()
    _test_other_field_cap_holds()
    _test_cat_b_rewording_no_double_count()
    print("All tests passed.\n")


def validate_against_dataset(csv_path="Survey_Dataset_120_MSMEs.csv"):
    """
    Reproduces the Week 1 Friday validation step on the 120-MSME CSV.
    The CSV does not yet contain Other-field columns, so this only
    exercises the standard scoring path (which must remain unchanged
    from the original engine to preserve the Chapter 4 numbers).
    """
    import pandas as pd
    from scipy.stats import pearsonr, chi2_contingency

    df = pd.read_csv(csv_path)

    def row_to_response(row):
        # Build the list of Lean tools that were ticked
        lean_tools = []
        if row["S3_Q2a_Tool_5S_1Yes_0No"] == 1:
            lean_tools.append("5S")
        if row["S3_Q2b_Tool_Kaizen_1Yes_0No"] == 1:
            lean_tools.append("Kaizen")
        if row["S3_Q2c_Tool_VSM_1Yes_0No"] == 1:
            lean_tools.append("VSM")
        if row["S3_Q2d_Tool_Kanban_1Yes_0No"] == 1:
            lean_tools.append("Kanban")
        if row["S3_Q2e_Tool_PokayYoke_1Yes_0No"] == 1:
            lean_tools.append("PokayYoke")

        # Build the list of Six Sigma tools that were ticked
        ss_tools = []
        if row["S3_Q4a_Tool_DMAIC_1Yes_0No"] == 1:
            ss_tools.append("DMAIC")
        if row["S3_Q4b_Tool_SPC_1Yes_0No"] == 1:
            ss_tools.append("SPC")
        if row["S3_Q4c_Tool_FMEA_1Yes_0No"] == 1:
            ss_tools.append("FMEA")
        if row["S3_Q4d_Tool_RCA_1Yes_0No"] == 1:
            ss_tools.append("RCA")

        # Put the response dict together for the scoring engine
        response = {
            "lean_awareness":     row["S2_Q1_Lean_Awareness_1Yes_0No"],
            "ss_awareness":       row["S2_Q2_Six_Sigma_Awareness_1Yes_0No"],
            "knowledge_level":    row["S2_Q4_Knowledge_Level_1to4"],
            "lean_implemented":   row["S3_Q1_Lean_Implemented_1Yes_0No"],
            "lean_tools":         lean_tools,
            "ss_implemented":     row["S3_Q3_SS_Implemented_1Yes_0No"],
            "ss_tools":           ss_tools,
            "primary_motivation": row["S3_Q5_Primary_Motivation"],
            "benefits_observed":  row["S3_Q6_Benefits_Observed"],
        }
        return response

    df["computed_score"] = df.apply(lambda r: calculate_lss_score(row_to_response(r)), axis=1)
    df["computed_level"] = df["computed_score"].apply(lambda s: assign_lss_level(s)[0])

    r, p = pearsonr(df["computed_score"], df["DARMM_Digital_Readiness_Score_0to10"])
    print(f"[Pearson]    LSS vs Digital  r = {r:.4f}, p = {p:.3e}   "
          f"{'PASS' if p<0.01 else 'FAIL'}")

    ct = pd.crosstab(
        df["S2_Q1_Lean_Awareness_1Yes_0No"],
        df["S3_Q1_Lean_Implemented_1Yes_0No"]
    )
    chi2, pval, dof, _ = chi2_contingency(ct)
    print(f"[Chi-square] Awareness x Adoption  chi2 = {chi2:.3f}, p = {pval:.3e}   "
          f"{'PASS' if pval<0.01 else 'FAIL'}")

    print("\nLevel distribution:")
    print("  Computed:", dict(df["computed_level"].value_counts().sort_index()))
    print("  Dataset: ", dict(df["DARMM_LSS_Level"].value_counts().sort_index()))

    agree = (df["computed_level"] == df["DARMM_LSS_Level"]).sum()
    print(f"\nLevel agreement: {agree}/120 ({agree/120*100:.1f}%) exact")


if __name__ == "__main__":
    _run_tests()
    try:
        validate_against_dataset()
    except FileNotFoundError:
        print("(Skipping dataset validation - CSV not found in cwd.)")
