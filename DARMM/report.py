import os
import tempfile
from datetime import  datetime
import pandas as pd
from fpdf import FPDF
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
_HERE=os.path.dirname(os.path.abspath(__file__))
_CSV_PATH=os.path.join(_HERE,"Survey_Dataset_120_MSMEs.csv")

clusters={1:{"name": "Analogue Beginners",
        "pathway": (
            "Begin at Tier 1. OSK-only. Paper-based tools exclusively. No "
            "digital investment required. Focus on 5S and visual discipline "
            "for 8-12 weeks before any further action."),},
    2: {
        "name": "Digitally Basic Beginners",
        "pathway": (
            "Begin at Tier 1. OSK with digital companion templates. Introduce "
            "basic spreadsheet defect tracking alongside 5S. Progress to Tier "
            "2 Kaizen within 3-4 months."), },
    3: {
        "name": "Partial Adopters",
        "pathway": (
            "Enter at Tier 2. Consolidate 5S with sustained audit system. "
            "Begin Kaizen facilitation. Introduce VSM. Plan digital tracking "
            "for OEE within 6 months."  ),},
    4: {
        "name": "Structured Implementers", "pathway": (
            "Enter at Tier 2/3 boundary. Data-driven Kaizen + DMAIC "
            "introduction. ERP integration of quality data. KPI dashboard "
            "development."),},
    5: {
        "name": "Advanced Integrators",
        "pathway": (
            "Full Tier 3 with I4.0 integration. IIoT-enabled SPC. Predictive "
            "quality analytics. Benchmark-driven continuous improvement "
            "cadence."),},}
diagonal_map={
    ("L1","A"):1,("L2","A"):1,("L1","B"):2,("L2","B"):2,("L3","A"):3,("L3","B"):3,("L4","B"):4,("L4","C"):4,("L5","C"):5,("L5","D"):5,}


OFF_DIAGONAL_PATHWAYS = {

    # ---------------- Digital-lagging wing ----------------

    ("L4", "A"): (
        "Advanced Lean capability established; paper records are now the "
        "binding constraint. Move defect and downtime tracking from paper to "
        "spreadsheet templates. Once routine, proceed to ERP integration of "
        "quality data per the Structured Implementer pathway."
    ),

    ("L5", "A"): (
        "World-class Lean maturity established; paper records limit its "
        "reach. Digitise in sequence: spreadsheet tracking of existing 5S, "
        "defect and OEE records first, then an entry-level ERP. Compressed "
        "cadence appropriate given mature processes. Sequence I4.0 after ERP."
    ),

    ("L5", "B"): (
        "World-class Lean maturity with spreadsheet tracking in place. Data "
        "integration is the next constraint. Adopt an entry-level ERP and "
        "migrate quality data into one system. IIoT-enabled SPC becomes "
        "valuable once ERP data exists; sequence it after."
    ),

    # ---------------- Lean-lagging / digital-first wing ----------------

    ("L4", "D"): (
        "Advanced Lean practice with IIoT infrastructure already in place. "
        "Consolidate the upper-tier toolset: data-driven Kaizen plus DMAIC "
        "introduction, using IIoT process data as the measurement base. This "
        "completes the transition to the Advanced Integrator pathway."
    ),

    ("L3", "C"): (
        "Established Lean foundations with ERP/QMS already in place - ahead "
        "of requirement. Complete Tier 2: sustained 5S audits, Kaizen "
        "facilitation, VSM. Log Kaizen actions and begin OEE tracking inside "
        "the existing ERP rather than separately."
    ),

    ("L3", "D"): (
        "Established Lean foundations with IIoT sensing already in place. "
        "Complete Tier 2: sustained 5S audits, Kaizen facilitation, VSM. "
        "Route live machine data into Kaizen project selection and "
        "verification, positioning directly for data-driven DMAIC."
    ),

    ("L2", "C"): (
        "ERP/QMS adopted early - a digital base most enterprises build "
        "later. Lean foundations are the constraint. Begin at Tier 1: 5S and "
        "visual discipline for 8-12 weeks, logging defects and audit scores "
        "in the existing ERP. Then progress to Tier 2 Kaizen."
    ),

    ("L2", "D"): (
        "Advanced digital infrastructure in place; Lean foundations are the "
        "constraint. Begin at Tier 1: 5S and visual discipline for 8-12 "
        "weeks, scoring audits on existing dashboards. Then progress to Tier "
        "2 Kaizen with live machine data ready."
    ),

    ("L1", "C"): (
        "ERP/QMS adopted ahead of the Lean journey. Begin at Tier 1: 5S and "
        "visual discipline for 8-12 weeks before further action, recording "
        "audit scores and defects in the existing system from week one. Then "
        "progress to Tier 2 Kaizen."
    ),

    ("L1", "D"): (
        "IoT infrastructure adopted ahead of the Lean journey - an asset "
        "once foundations exist. Begin at Tier 1: 5S and visual discipline "
        "for 8-12 weeks, tracking audit scores digitally from day one. Then "
        "progress to Tier 2 Kaizen with machine data ready."
    ),
}
OFF_DIAGONAL_NAMES = {
    ("L4", "A"): "Advanced Lean, Analogue Records",
    ("L5", "A"): "World-Class Lean, Analogue Records",
    ("L5", "B"): "World-Class Lean, Basic Digital",
    ("L4", "D"): "Advanced Lean, Digitally Equipped",
    ("L3", "C"): "Established Lean, Digitally Ahead",
    ("L3", "D"): "Established Lean, Digitally Advanced",
    ("L2", "C"): "Early Lean, Digitally Ahead",
    ("L2", "D"): "Early Lean, Digitally Advanced",
    ("L1", "C"): "Digital-First Starter (ERP in place)",
    ("L1", "D"): "Digital-First Starter (IIoT in place)",
}
OFF_DIAGONAL_ACTIONS = {
    ("L4", "A"): [
        "Move defect and downtime tracking from paper to a spreadsheet template (Excel/Google Sheets) on one production line.",
        "Digitise your existing audit records first - your established formats transfer directly to spreadsheet form.",
        "Once spreadsheet tracking is routine (4-6 weeks), plan ERP integration of quality data as the next step.",
    ],
    ("L5", "A"): [
        "Move your existing 5S audit scores, defect logs and OEE records from paper to spreadsheet-based tracking.",
        "Set a compressed review cadence (fortnightly) - your mature processes mean this transition is faster than typical.",
        "Once spreadsheet tracking is routine, evaluate an entry-level ERP suited to MSMEs; sequence I4.0 technologies after ERP data exists.",
    ],
    ("L5", "B"): [
        "Shortlist and adopt an entry-level ERP suited to MSMEs, prioritising quality and production modules.",
        "Migrate your existing spreadsheet quality data into the ERP so trend analysis runs across processes.",
        "Once ERP data is flowing, plan IIoT-enabled SPC on one critical process as the next step.",
    ],
    ("L4", "D"): [
        "Run one DMAIC project on a recurring quality issue, using your IIoT process data as the measurement base.",
        "Consolidate data-driven Kaizen routines with a monthly cadence on your highest-defect line.",
        "Once DMAIC is established on live sensor data, deploy IIoT-enabled SPC on one critical process.",
    ],
    ("L3", "C"): [
        "Consolidate existing 5S with a sustained weekly audit roster.",
        "Begin facilitating one Kaizen event per month, logging actions and outcomes in your existing ERP/QMS.",
        "Start OEE tracking for at least one machine inside the ERP you already operate.",
    ],
    ("L3", "D"): [
        "Consolidate existing 5S with a sustained weekly audit roster.",
        "Begin one Kaizen event per month, using your IIoT machine data to select and verify improvement projects.",
        "Introduce value stream mapping on your main product family, with sensor data as the data source.",
    ],
    ("L2", "C"): [
        "Implement 5S (Sort, Set in Order, Shine, Standardise, Sustain) on one production line.",
        "Log defects and 5S audit scores in the ERP/QMS you already operate, rather than on paper.",
        "Sustain the practice for 8-12 weeks, then progress to Tier 2 Kaizen with digital tracking already in place.",
    ],
    ("L2", "D"): [
        "Implement 5S on one production line.",
        "Score and display 5S audits on your existing dashboards so workplace discipline is visible in real time.",
        "Sustain for 8-12 weeks, then begin Kaizen with live machine data ready to guide improvement projects.",
    ],
    ("L1", "C"): [
        "Implement 5S on one production line.",
        "Record 5S audit scores and defects in your ERP/QMS from the first week.",
        "Sustain for 8-12 weeks before adding any other Lean tool, then progress to Tier 2 Kaizen.",
    ],
    ("L1", "D"): [
        "Implement 5S on one production line.",
        "Repurpose your IoT capability from day one - track and display 5S audit scores digitally.",
        "Sustain for 8-12 weeks before adding any other Lean tool, then progress to Tier 2 Kaizen.",
    ],
}


cluster_actions = {
    1: [
        "Implement 5S (Sort, Set in Order, Shine, Standardise, Sustain) on one production line.",
        "Set up daily visual management boards (production board, quality board).",
        "Sustain the practice for 8-12 weeks before adding any other Lean tool.",
    ],
    2: [
        "Implement 5S on one production line.",
        "Create a basic spreadsheet (Excel/Google Sheets) for daily defect tracking.",
        "Plan to begin Kaizen events within 3-4 months once 5S is routine.",
    ],
    3: [
        "Consolidate existing 5S with a sustained weekly audit roster.",
        "Begin facilitating one Kaizen event per month on your highest-defect line.",
        "Plan digital OEE tracking for at least one machine within 6 months.",
    ],
    4: [
        "Run one DMAIC project on a recurring quality issue, with data from your ERP.",
        "Integrate quality records (defects, returns, complaints) into your ERP module.",
        "Build a basic KPI dashboard (production, quality, OEE) for management review.",
    ],
    5: [
        "Deploy IIoT-enabled SPC on at least one critical process.",
        "Begin predictive quality analytics using your existing production data.",
        "Establish a quarterly benchmark cadence against industry peers.",
    ],
}


def _latin1(text):
    replacements={"\u2013": "-",     # en dash
        "\u2014": " - ",   # em dash
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",}
    for bad,good in replacements.items():
        text=text.replace(bad,good)
    return text.encode("latin-1",errors="replace").decode("latin-1")   



def get_pathway(lss_level,digital_level):
    key=(lss_level,digital_level)
    if key in diagonal_map:
        cluster_num=diagonal_map[key]
        cluster=clusters[cluster_num]
        return(
            cluster["name"],
            _latin1(cluster["pathway"]),
            [_latin1(a) for a in cluster_actions[cluster_num]],
            "cluster",)
    
        
    if  key in OFF_DIAGONAL_PATHWAYS:
        return ( OFF_DIAGONAL_NAMES[key],
                _latin1(OFF_DIAGONAL_PATHWAYS[key]),
                [_latin1(a) for a in OFF_DIAGONAL_ACTIONS[key]],"derived",)
    return("unclassified","position not classified-please consult researcher,",[],"fallback",)



def compute_percentiles(lss_score,digital_score):
    df=pd.read_csv(_CSV_PATH)
    n=len(df)
    lss_pct=(df["DARMM_LSS_Maturity_Score_0to20"]<lss_score).sum()/n*100
    dig_pct=(df["DARMM_Digital_Readiness_Score_0to10"]<digital_score).sum()/n*100
    return round(lss_pct), round(dig_pct)


def make_grid_image(lss_level,digital_level):
    df=pd.read_csv(_CSV_PATH) 
    density=pd.crosstab(df["DARMM_Digital_Level"],df["DARMM_LSS_Level"])
    density=density.reindex(index=["A","B","C","D"],columns=["L1","L2","L3","L4","L5"],fill_value=0,)  
    fig,ax=plt.subplots(figsize=(6,4))
    ax.imshow(density.values,cmap="Greens",aspect="auto")
    ax.set_xticks(range(5))
    ax.set_xticklabels(["L1","L2","L3","L4","L5"])
    ax.set_yticks(range(4))
    ax.set_yticklabels(["A","B","C","D"])
    ax.set_xlabel("LSS operational maturity")
    ax.set_ylabel("digital readiness") 
    ax.set_title("position on the DARMM grid(n=120 MSMEs)")  


    for i in range(4):
        for j in range(5):
            ax.text(j,i,str(density.values[i,j]),
                    ha="center",va="center",fontsize=10)

    lss_idx=["L1","L2","L3","L4","L5"].index(lss_level)
    dig_idx=["A","B","C","D"].index(digital_level)
    ax.plot(lss_idx,dig_idx,"o",markersize=24,markerfacecolor="none",markeredgecolor="red",markeredgewidth=3)
    ax.text(lss_idx,dig_idx-0.45,"YOU",ha="center",color="red",fontsize=11,fontweight="bold")
    plt.tight_layout()
    tmp=tempfile.NamedTemporaryFile(suffix=".png",delete=False)
    plt.savefig(tmp.name,dpi=150,bbox_inches="tight")
    plt.close(fig)
    return tmp.name



## pdf builder
def generate_report(response, lss_result, digital_result, company_name="Anonymous Enterprise"):
    pdf = FPDF()
    pdf.add_page()

    # ---- 1. COVER ----
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, _latin1("DARMM Self Assessment Report"), ln=True, align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, _latin1("Company: " + company_name), ln=True, align="C")
    pdf.cell(0, 6, "Date: " + datetime.now().strftime("%d %B %Y"), ln=True, align="C")
    pdf.ln(6)

    # ---- 2. EXECUTIVE SUMMARY ----
    position = lss_result["lss_level"] + "-" + digital_result["digital_level"]
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 10, "Your DARMM Position: " + position, ln=True)

    # Position context - how many MSMEs share this position in the 120 sample
    df_sample = pd.read_csv(_CSV_PATH)
    total = len(df_sample)
    same_position = (df_sample["DARMM_Position"] == position).sum()
    pct_at_position = round(same_position / total * 100)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6,
        "Out of " + str(total) + " surveyed MSMEs in Bangalore, " +
        str(same_position) + " (" + str(pct_at_position) +
        "%) share this DARMM position."
    )
    pdf.ln(2)

    # ---- 3. GRID POSITION PLOT ----
    grid_path = make_grid_image(lss_result["lss_level"], digital_result["digital_level"])
    pdf.image(grid_path, x=30, w=150)
    pdf.ln(4)
    try:
        os.remove(grid_path)
    except OSError:
        pass

    # ---- 4. LSS SECTION ----
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Lean Six Sigma Maturity", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, _latin1("Level: " + lss_result["lss_level"] + " - " + lss_result["lss_level_name"]), ln=True)
    pdf.multi_cell(0, 6, _latin1(lss_result["lss_level_desc"]))
    pdf.ln(4)

    # ---- 5. DIGITAL SECTION + discrepancy flag ----
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Digital Readiness", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, _latin1("Level: " + digital_result["digital_level"] + " - " + digital_result["digital_level_name"]), ln=True)
    pdf.multi_cell(0, 6, _latin1(digital_result["digital_level_desc"]))
    if digital_result.get("discrepancy_flag"):
        pdf.ln(1)
        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(0, 5, _latin1("Note: " + digital_result["discrepancy_flag"]))
    pdf.ln(4)

    # ---- 6. RECOMMENDATION PATHWAY ----
    cluster_name, pathway, actions, source = get_pathway(
        lss_result["lss_level"], digital_result["digital_level"]
    )
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, _latin1("Recommended Entry Pathway: " + cluster_name), ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, pathway)
    pdf.ln(3)

    # ---- 7. THREE FIRST ACTIONS ----
    if actions:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Your first three actions", ln=True)
        pdf.set_font("Helvetica", "", 11)
        for i, action in enumerate(actions, start=1):
            pdf.multi_cell(0, 6, str(i) + ". " + action)
            pdf.ln(1)
    pdf.ln(4)

    # ---- 8. FOOTER ----
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 5, _latin1(
        "DARMM is a research framework from NIT Calicut measuring two axes of "
        "manufacturing maturity: Lean Six Sigma maturity (L1-L5) and Digital "
        "Readiness (A-D). This report compares your enterprise against a "
        "sample of 120 Bangalore MSMEs surveyed in 2026. "
        "Research: Jith John Francis (P230090ME), supervised by "
        "Dr. Vinay V. Panicker."
    ))
    

    return bytes(pdf.output())

             