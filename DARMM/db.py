"""DARMM Supabase client - saves each survey submission to the database."""

from supabase import create_client, Client
import streamlit as st


# Display-string -> DB-column mappings
LEAN_TOOL_DB_KEYS = {
    "5S (Workplace Organisation)": "tool_5s",
    "Kaizen (Continuous Improvement Events)": "tool_kaizen",
    "Value Stream Mapping (VSM)": "tool_vsm",
    "Kanban (Inventory and Flow Control)": "tool_kanban",
    "Poka-Yoke / Error-Proofing": "tool_pokayoke",
    "Visual Management Boards": "tool_visualmgmt",
    "Standard Work documentation": "tool_stdwork",
}

SS_TOOL_DB_KEYS = {
    "DMAIC project framework": "tool_dmaic",
    "Statistical Process Control (SPC)": "tool_spc",
    "FMEA (Failure Mode and Effects Analysis)": "tool_fmea",
    "Root Cause Analysis (5 Whys / Fishbone)": "tool_rca",
    "Process Capability Analysis (Cpk)": "tool_cpk",
}

DIGITAL_TOOL_DB_KEYS = {
    "None - all records are paper-based": "digital_tool_paper",
    "MS Excel or Google Sheets for production tracking": "digital_tool_excel",
    "Basic accounting software (Tally, QuickBooks) - financial only": "digital_tool_accounting",
    "ERP system (Tally Prime, Odoo, SAP B1) for production and quality": "digital_tool_erp",
    "Dedicated QMS software": "digital_tool_qms",
    "CAD / CAM software for production engineering": "digital_tool_cad_cam",
    "IoT sensors or machine monitoring systems": "digital_tool_iot",
    "Cloud-based analytics or dashboard tools": "digital_tool_cloud_analytics",
}

KNOWLEDGE_LEVEL_MAP = {
    "No knowledge at all": 1,
    "Basic awareness (heard of it, never implemented)": 2,
    "Moderate understanding (implemented some practices)": 3,
    "High understanding (actively use LSS in operations)": 4,
}

SELF_RATING_MAP = {
    "Level A - No digital tools; paper records only": "A",
    "Level B - Basic digital only (spreadsheets, basic accounting)": "B",
    "Level C - Intermediate digital (ERP, digital QMS, some production data tracking)": "C",
    "Level D - Advanced digital (IoT, real-time analytics, integrated production management)": "D",
}


def get_client() -> Client:
    """Build the Supabase client from Streamlit secrets."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


def _yn(v):
    """Yes/No -> 1/0. Returns None if v is None."""
    if v is None:
        return None
    return 1 if v == "Yes" else 0


def _tools_to_columns(selected, mapping):
    """Convert a multiselect list into per-column 0/1 flags."""
    cols = {db_key: 0 for db_key in mapping.values()}
    for label in selected or []:
        if label in mapping:
            cols[mapping[label]] = 1
    return cols


def build_row(session_state, lss_result, digital_result, cluster_name, source):
    """Translate Streamlit session_state + engine output into a DB row dict."""
    row = {
        # Section 1
        "company_name": session_state.get("q1_1") or None,
        "industry_segment": session_state.get("q1_2"),
        "size_category": session_state.get("q1_3"),
        "years_operation": session_state.get("q1_4"),
        "primary_customer": session_state.get("q1_5"),
        "cluster_location": session_state.get("q1_6"),

        # Section 2
        "lean_awareness": _yn(session_state.get("q2_1")),
        "ss_awareness": _yn(session_state.get("q2_2")),
        "learning_channels": session_state.get("q2_3", []),
        "knowledge_level": KNOWLEDGE_LEVEL_MAP.get(session_state.get("q2_4")),

        # Section 3 - Lean
        "lean_implemented": _yn(session_state.get("q3_1")),
        "lean_other": session_state.get("q3_2_other") or None,

        # Section 3 - Six Sigma
        "ss_implemented": _yn(session_state.get("q3_3")),
        "ss_other": session_state.get("q3_4_other") or None,

        # Section 3 - Motivation / Benefits
        "primary_motivation": session_state.get("q3_5", []),
        "benefits_observed": session_state.get("q3_6", []),

        # Section 4
        "barriers": session_state.get("q4_1", []),
        "lss_benefit_belief": session_state.get("q4_2"),
        "support_needed": session_state.get("q4_3", []),
        "pilot_willing": _yn(session_state.get("q4_4")),

        # Section 5
        "digital_other": session_state.get("q5_1_other") or None,
        "self_rating": SELF_RATING_MAP.get(session_state.get("q5_2")),
        "digital_investment_plan": session_state.get("q5_3"),
        "interview_willing": _yn(session_state.get("q5_4")),

        # Engine outputs
        "lss_score": lss_result["lss_score"],
        "lss_level": lss_result["lss_level"],
        "digital_score": digital_result["digital_score"],
        "digital_level": digital_result["digital_level"],
        "darmm_position": lss_result["lss_level"] + "-" + digital_result["digital_level"],
        "cluster_name": cluster_name,
        "pathway_source": source,
        "discrepancy_flag": digital_result.get("discrepancy_flag"),
    }

    # Add the tool binary columns
    row.update(_tools_to_columns(session_state.get("q3_2_tools", []), LEAN_TOOL_DB_KEYS))
    row.update(_tools_to_columns(session_state.get("q3_4_tools", []), SS_TOOL_DB_KEYS))
    row.update(_tools_to_columns(session_state.get("q5_1_tools", []), DIGITAL_TOOL_DB_KEYS))

    return row


def save_response(session_state, lss_result, digital_result, cluster_name, source):
    """Insert a survey submission into the responses table.
    Returns (success: bool, error_message: str or None)."""
    try:
        client = get_client()
        row = build_row(session_state, lss_result, digital_result, cluster_name, source)
        client.table("responses").insert(row).execute()
        return True, None
    except Exception as e:
        return False, str(e)
