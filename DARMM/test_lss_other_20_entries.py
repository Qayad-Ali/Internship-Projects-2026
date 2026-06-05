"""
Run  20 real "Other" field entries through the LSS Other classifier.
Pass rule: correct category AND score within +/-0.2 of expected.
"""
from lss_other_field import score_other_field, classify_one_entry

#  20 entries
TEST_CASES = [
    # Q3.2 Lean (14 entries)
    {"n": 1,  "entry": "TPM",
     "expected_cat": "A", "expected_score": 1.0},
    {"n": 2,  "entry": "OEE board on shopfloor",
     "expected_cat": "A", "expected_score": 1.0},
    {"n": 3,  "entry": "SMED - changeover time reduction",
     "expected_cat": "A", "expected_score": 1.0},
    {"n": 4,  "entry": "Gemba walks by management",
     "expected_cat": "A", "expected_score": 1.0},
    {"n": 5,  "entry": "A3 sheets for problems",
     "expected_cat": "A", "expected_score": 1.0},
    {"n": 6,  "entry": "6S (with safety)",
     "expected_cat": "B", "expected_score": 1.0, "maps_to": "5S"},
    {"n": 7,  "entry": "Shadow boards and floor markings",
     "expected_cat": "B", "expected_score": 1.0, "maps_to": "VisualManagement"},
    {"n": 8,  "entry": "SOP for all machine operations",
     "expected_cat": "B", "expected_score": 1.0, "maps_to": "StandardWork"},
    {"n": 9,  "entry": "Pull system for components to assembly",
     "expected_cat": "B", "expected_score": 1.0, "maps_to": "Kanban"},
    {"n": 10, "entry": "CI events quarterly",
     "expected_cat": "B", "expected_score": 1.0, "maps_to": "Kaizen"},
    {"n": 11, "entry": "Mistake proofing jigs for drilling",
     "expected_cat": "B", "expected_score": 1.0, "maps_to": "PokayYoke"},
    {"n": 12, "entry": "ISO 9001:2015 certified",
     "expected_cat": "C", "expected_score": 0.6},
    {"n": 13, "entry": "PPAP and APQP as per customer",
     "expected_cat": "C", "expected_score": 0.7},
    {"n": 14, "entry": "Daily housekeeping roster",
     "expected_cat": "D", "expected_score": 0.3},

    # Q3.4 Six Sigma (6 entries)
    {"n": 15, "entry": "Gauge R&R for critical dimensions",
     "expected_cat": "A", "expected_score": 1.0},
    {"n": 16, "entry": "SIPOC mapping done for all processes",
     "expected_cat": "A", "expected_score": 0.8},
    {"n": 17, "entry": "Pareto chart for top rejection reasons",
     "expected_cat": "A", "expected_score": 0.8},
    {"n": 18, "entry": "8D reports for customer complaints",
     "expected_cat": "C", "expected_score": 0.7},
    {"n": 19, "entry": "PDCA for all quality issues",
     "expected_cat": "C", "expected_score": 0.6},
    {"n": 20, "entry": "Our own corrective action log (not formal 8D)",
     "expected_cat": "E", "expected_score": 0.3},
]


def run_tests():
    print("===========================================================================")
    print(" 20 real Other-field entries vs LSS Other classifier")
    print("===========================================================================")
    print()

    passes = 0
    fails  = 0
    fail_details = []

    for tc in TEST_CASES:
        # We assume the standard tool was NOT ticked, so Cat B re-wordings
        # get full credit (same as 6S, SOP, CI events without ticking 5S etc.)
        entry_text = tc["entry"]
        expected_cat = tc["expected_cat"]
        expected_score = tc["expected_score"]

        # Run the classifier on this entry
        score, breakdown = score_other_field(entry_text, already_ticked_tools=[])

        # Pull the actual category from the first non-CAP-applied entry
        if len(breakdown) > 0:
            actual_cat = breakdown[0]["category"]
        else:
            actual_cat = "-"

        # Pass rule: correct category AND score within +/- 0.2
        cat_ok = (actual_cat == expected_cat)
        score_ok = (abs(score - expected_score) <= 0.2)

        if cat_ok and score_ok:
            passes = passes + 1
            status = "PASS"
        else:
            fails = fails + 1
            status = "FAIL"
            fail_details.append((tc["n"], entry_text, actual_cat, score, tc))

        # Print the result row
        short_entry = entry_text[:42]
        print("  [" + status + "] #" + str(tc["n"]).rjust(2) + ": '" +
              short_entry.ljust(42) + "' -> Cat " + str(actual_cat) +
              " score " + str(round(score, 1)) +
              "  (exp Cat " + expected_cat + " score " + str(expected_score) + ")")

    print()
    print("RESULT: " + str(passes) + "/20 pass (" + str(round(passes/20*100)) + "%)")

    if len(fail_details) > 0:
        print()
        print("FAILURES (details):")
        for n, entry, got_cat, got_score, tc in fail_details:
            print("  #" + str(n) + ": '" + entry + "'")
            print("     got: Cat " + str(got_cat) + ", score " + str(got_score))
            print("     exp: Cat " + tc["expected_cat"] +
                  ", score " + str(tc["expected_score"]))
            # Show why it matched what it matched
            cat, weight, maps_to, notes = classify_one_entry(entry)
            print("     trace: classify_one_entry returned Cat " + str(cat) +
                  ", weight " + str(weight))
            print("            notes: " + str(notes))
            print()


if __name__ == "__main__":
    run_tests()
