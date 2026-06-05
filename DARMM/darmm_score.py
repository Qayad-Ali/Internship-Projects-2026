"""Combined scoring wrapper: calls both engines and returns 5-field result with darmm_position."""

from lss_scoring import darmm_lss
from digital_scoring import darmm_digital


def darmm_score(response):
    """
    Run both axes of the DARMM model and return the grid placement.

    Args:
        response: dict of survey answers (see lss_scoring.py and
                  digital_scoring.py for the expected keys)

    Returns:
        dict with 5 fields - the Module 1 minimum:
            lss_score, lss_level, digital_score, digital_level, darmm_position
    """
    # First get the LSS score and level
    lss_result = darmm_lss(response)

    # Then get the digital readiness score and level
    digital_result = darmm_digital(response)

    # Build the grid position string like "L3-B"
    position = lss_result["lss_level"] + "-" + digital_result["digital_level"]

    # Put everything together for the output
    output = {
        "lss_score":      lss_result["lss_score"],
        "lss_level":      lss_result["lss_level"],
        "digital_score":  digital_result["digital_score"],
        "digital_level":  digital_result["digital_level"],
        "darmm_position": position,
    }
    return output



if __name__ == "__main__":

    # A few test enterprises so I can check the engine end-to-end
    examples = [
        ("Ravi's Micro Shop (unaware, paper-only)", {
            "knowledge_level": 1,
        }),
        ("Sharma Engineering (5S+Kaizen, Excel)", {
            "lean_awareness": 1, "ss_awareness": 1, "knowledge_level": 3,
            "lean_implemented": 1, "lean_tools": ["5S", "Kaizen"],
            "digital_tools": ["Excel"], "self_rating": "B",
            "primary_motivation": "Customer requirement",
            "benefits_observed": "Reduced defects",
        }),
        ("Tier-2 Supplier (structured SS, ERP)", {
            "lean_awareness": 1, "ss_awareness": 1, "knowledge_level": 3,
            "lean_implemented": 1, "lean_tools": ["5S", "Kaizen", "VSM"],
            "ss_implemented": 1, "ss_tools": ["DMAIC", "SPC"],
            "digital_tools": ["ERP"], "self_rating": "C",
            "primary_motivation": "OEM pressure",
            "benefits_observed": "Lower costs",
        }),
        ("Tier-1 Supplier (full integration, IoT)", {
            "lean_awareness": 1, "ss_awareness": 1, "knowledge_level": 4,
            "lean_implemented": 1, "lean_tools": ["5S","Kaizen","VSM","Kanban","PokayYoke"],
            "ss_implemented": 1, "ss_tools": ["DMAIC","SPC","FMEA","RCA"],
            "digital_tools": ["IoT", "ERP"], "self_rating": "D",
            "primary_motivation": "Cost reduction",
            "benefits_observed": "Reduced defects and rework",
        }),
    ]
  
    print("DARMM combined scoring demo")
    

    for name, r in examples:
        out = darmm_score(r)
        print("")
        print(name)
        print("  LSS     : " + out["lss_level"] + " (score " + str(out["lss_score"]) + ")")
        print("  Digital : " + out["digital_level"] + " (score " + str(out["digital_score"]) + ")")
        print("  Position: " + out["darmm_position"])
