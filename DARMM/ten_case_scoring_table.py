"""Prints a 10-case scoring table for review (2 enterprises per LSS level)."""

import pandas as pd
from darmm_score import darmm_score

CSV = "Survey_Dataset_120_MSMEs.csv"


def row_to_response(row):
    CSV_MAP = {
        "Paper records and manual registers only":      ["None"],
        "MS Excel spreadsheets":                        ["Excel"],
        "Google Sheets + basic Tally ERP":              ["Excel", "Accounting"],
        "Excel-based production and quality tracking":  ["Excel"],
        "Tally Prime ERP with production module":       ["ERP"],
        "Odoo ERP (cloud)":                             ["ERP"],
        "SAP Business One with QMS module":             ["ERP", "QMS"],
        "SAP ERP + IoT machine monitoring":             ["ERP", "IoT"],
    }
    digital_tools = CSV_MAP.get(row["Digital_Tools_Currently_Used"], [])

    # Build the list of Lean tools that were ticked in the CSV
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
        "digital_tools":      digital_tools,
        # No Q5.2 self-rating in the CSV; engine handles missing gracefully
    }
    return response


def pick_10_representative_cases(df):
    """
    Pick 2 enterprises from each LSS level. Strategy:
      - First pick: the most "central" enterprise (modal tool stack)
      - Second pick: the most "boundary" enterprise (score near a cutoff)
    """
    cases = []
    for level in ["L1", "L2", "L3", "L4", "L5"]:
        # Get all enterprises at this level
        subset = df[df["DARMM_LSS_Level"] == level].copy()
        if len(subset) == 0:
            continue
        # Sort them by their LSS score so we can pick middle and edge
        subset = subset.sort_values("DARMM_LSS_Maturity_Score_0to20")

        # First case: the middle enterprise (most typical for this level)
        middle_index = len(subset) // 2
        first = subset.iloc[middle_index]
        cases.append(first)

        # Second case: a different enterprise from the same level
        # (the lowest scorer, or the highest if the lowest is already picked)
        if len(subset) > 1:
            lowest = subset.iloc[0]
            highest = subset.iloc[-1]
            if first.name != lowest.name:
                second = lowest
            else:
                second = highest
            cases.append(second)

    return cases


def main():
    df = pd.read_csv(CSV)
    cases = pick_10_representative_cases(df)

    print("=" * 110)
    print(" DARMM 10-CASE SCORING TABLE (for Mr. Jith review) ".center(110, "="))
    print("=" * 110)
    print()

    # Table header
    header = (
        f"{'ID':<10} {'Size':<7} {'Tools Used':<25} "
        f"{'LSS man':<7} {'LSS pred':<8} {'LSS ok':<7} "
        f"{'DIG man':<7} {'DIG pred':<8} {'DIG ok':<7} "
        f"{'Grid pred':<10}"
    )
    print(header)
    print("-" * 100)

    lss_correct = 0
    dig_correct = 0
    grid_correct = 0

    for row in cases:
        r = row_to_response(row)
        out = darmm_score(r)

        lss_man = row["DARMM_LSS_Level"]
        dig_man = row["DARMM_Digital_Level"]
        grid_man = row["DARMM_Position"]
        grid_pred = out["darmm_position"]

        # Check whether each axis matches the manual label
        if out["lss_level"] == lss_man:
            lss_ok = "OK"
            lss_correct = lss_correct + 1
        else:
            lss_ok = "MISS"

        if out["digital_level"] == dig_man:
            dig_ok = "OK"
            dig_correct = dig_correct + 1
        else:
            dig_ok = "MISS"

        if grid_pred == grid_man:
            grid_correct = grid_correct + 1

        # Shorten tool list for table width
        tools_str = row["Digital_Tools_Currently_Used"]
        if len(tools_str) > 24:
            tools_str = tools_str[:22] + ".."

        print(
            f"{row['Enterprise_ID']:<10} "
            f"{row['S1_Size_Category']:<7} "
            f"{tools_str:<25} "
            f"{lss_man:<7} {out['lss_level']:<8} {lss_ok:<7} "
            f"{dig_man:<7} {out['digital_level']:<8} {dig_ok:<7} "
            f"{grid_pred:<10}"
        )

    # Summary footer
    n = len(cases)
    print("-" * 100)
    print(f"\nSummary across {n} cases:")
    print(f"  LSS axis    : {lss_correct}/{n} correct ({lss_correct/n*100:.0f}%)")
    print(f"  Digital axis: {dig_correct}/{n} correct ({dig_correct/n*100:.0f}%)")
    print(f"  Grid cell   : {grid_correct}/{n} correct ({grid_correct/n*100:.0f}%)")

    # Detailed breakdown of each case (for Mr. Jith to inspect closely)
    print()
    print("=" * 110)
    print(" Per-case detail (for inspection) ".center(110, "="))
    print("=" * 110)

    for i, row in enumerate(cases, 1):
        r = row_to_response(row)
        out = darmm_score(r)
        print(f"\nCase {i:2d}  ({row['Enterprise_ID']}, {row['S1_Size_Category']}, "
              f"{row['S1_Industry_Segment']})")
        print(f"    Lean awareness = {r['lean_awareness']},  "
              f"SS awareness = {r['ss_awareness']},  "
              f"Knowledge = {r['knowledge_level']}/4")
        print(f"    Lean tools ticked     : {r['lean_tools']}")
        print(f"    Six Sigma tools ticked: {r['ss_tools']}")
        print(f"    Digital tools (CSV)   : {row['Digital_Tools_Currently_Used']}")
        print(f"    Engine LSS  : score={out['lss_score']:>2}  ->  "
              f"{out['lss_level']}    "
              f"[manual: {row['DARMM_LSS_Level']}]")
        print(f"    Engine DIG  : score={out['digital_score']:>4}  -> "
              f"{out['digital_level']}     "
              f"[manual: {row['DARMM_Digital_Level']}]")
        print(f"    Grid pos    : {out['darmm_position']}              "
              f"[manual: {row['DARMM_Position']}]")


if __name__ == "__main__":
    main()
