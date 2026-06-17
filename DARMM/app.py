"""DARMM Self-Assessment Streamlit wizard. Run: python -m streamlit run app.py"""

import os
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from db import save_response
from report import get_pathway
_HERE = os.path.dirname(os.path.abspath(__file__))
from lss_scoring import darmm_lss
from digital_scoring import darmm_digital
from report import generate_report



# st.set_page_config must be the very first Streamlit call
st.set_page_config(
    page_title="DARMM Self-Assessment",
    layout="wide",
)


# PAGE NAVIGATION HELPERS
if "page" not in st.session_state:
    st.session_state.page = 0


for _k in list(st.session_state.keys()):
    st.session_state[_k] = st.session_state[_k]


def go_next():
    st.session_state.page = st.session_state.page + 1


def go_back():
    st.session_state.page = st.session_state.page - 1


def restart():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state.page = 0


# OFFICIAL RESEARCH HEADER
st.markdown(
    "### Lean Six Sigma Awareness, Adoption, and Digital Readiness "
    "in General Engineering Manufacturing MSMEs — Bangalore, India"
)
st.caption(
    "PhD Research | NIT Calicut | Jith John Francis (P230090ME) "
    "— Supervised by Dr. Vinay V. Panicker"
)
st.divider()

# Confidentiality and purpose statement (only shown on the first page)
if st.session_state.page == 0:
    st.info(
        "**CONFIDENTIALITY AND PURPOSE STATEMENT**\n\n"
        "All responses will be kept strictly confidential and used exclusively "
        "for academic research purposes. No individual enterprise or respondent "
        "will be identified in any publication or report.\n\n"
        "Your insights will directly contribute to the development of a practical "
        "Lean Six Sigma framework designed specifically for MSMEs like yours.\n\n"
        "The questionnaire takes approximately 12–15 minutes to complete. There "
        "are no right or wrong answers — please respond based on your actual "
        "current situation."
    )

# DARMM title
st.title("DARMM Self-Assessment")


# CSS - make the two tab buttons bigger and more prominent
st.markdown(
    """
    <style>
    /* enlarge the tab labels */
    button[data-baseweb="tab"] {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        padding: 14px 28px !important;
        height: auto !important;
    }
    /* enlarge the tab label inner text (Streamlit wraps it in a <p>) */
    button[data-baseweb="tab"] div[data-testid="stMarkdownContainer"] p {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
    }
    /* a little spacing under the tab strip */
    div[data-baseweb="tab-list"] {
        margin-bottom: 1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# TWO TABS: Self-Assessment wizard + Population Overview dashboard
tab_self=st.container()


with tab_self:

    # Page tracker - only visible while the user is on the wizard tab
    st.progress(
        (st.session_state.page + 1) / 6,
        text="Page " + str(st.session_state.page + 1) + " of 6",
    )

    # PAGE 0 - SECTION 1 (Company Profile)
    if st.session_state.page == 0:
        st.header(" Section 1 - Company Profile")

        st.text_input("1.1  Company name (optional)", key="q1_1")

        st.radio(
            "1.2  Industry segment",
            ["Machining", "Fabrication", "Casting / Foundry",
             "Sheet Metal Processing", "General Engineering (Mixed)", "Other"],
            key="q1_2",
        )

        st.radio(
            "1.3  Company size (by employee count)",
            ["Micro (1-9 employees)", "Small (10-49 employees)", "Medium (50-249 employees)"],
            key="q1_3",
        )

        st.radio(
            "1.4  Years in operation",
            ["Less than 5 years", "5-10 years", "10-20 years", "More than 20 years"],
            key="q1_4",
        )

        st.radio(
            "1.5  Primary customer type",
            ["Automotive OEM / Tier-1 supplier", "Aerospace / Defence",
             "General engineering / Job shop", "Pharmaceutical equipment",
             "Industrial machinery", "Other"],
            key="q1_5",
        )

        st.radio(
            "1.6  Bangalore cluster location",
            ["Peenya", "Bommasandra", "Jigani", "Bidadi",
             "Harohalli", "Whitefield / EPIP", "Other"],
            key="q1_6",
        )

        st.button("Next →", on_click=go_next)


    # PAGE 1 - SECTION 2 (Awareness)
    elif st.session_state.page == 1:
        st.header(" Section 2 - Awareness")

        st.radio("2.1  Have you heard of Lean Manufacturing?", ["Yes", "No"], key="q2_1")

        st.radio("2.2  Have you heard of Six Sigma?", ["Yes", "No"], key="q2_2")

        st.multiselect(
            "2.3  If yes to either above, how did you learn about it? (select all that apply)",
            ["Industry training programme", "Online course or webinar",
             "Customer / OEM requirement", "Supplier or partner collaboration",
             "Industry association event", "Other"],
            key="q2_3",
        )

        # Q2.4 is MANDATORY - index=None so nothing is pre-selected
        st.radio(
            "2.4  How would you rate your company's current knowledge of LSS? (required)",
            ["No knowledge at all",
             "Basic awareness (heard of it, never implemented)",
             "Moderate understanding (implemented some practices)",
             "High understanding (actively use LSS in operations)"],
            index=None,
            key="q2_4",
        )

        col_back, col_next = st.columns(2)
        with col_back:
            st.button("← Back", on_click=go_back)
        with col_next:
            if st.session_state.get("q2_4") is None:
                st.button("Next →", disabled=True)
                st.error("Q2.4 is required before you can continue.")
            else:
                st.button("Next →", on_click=go_next)


    # PAGE 2 - SECTION 3 (Adoption)
    elif st.session_state.page == 2:
        st.header(" Section 3 - Adoption")

        # Q3.1 is MANDATORY
        st.radio(
            "3.1  Has your enterprise implemented any Lean tools or practices? (required)",
            ["Yes", "No"],
            index=None,
            key="q3_1",
        )

        # Skip logic: only show Q3.2 if Q3.1 == Yes
        if st.session_state.get("q3_1") == "Yes":
            st.multiselect(
                "3.2  Which Lean tools have you implemented? (select all that apply)",
                ["5S (Workplace Organisation)", "Kaizen (Continuous Improvement Events)",
                 "Value Stream Mapping (VSM)", "Kanban (Inventory and Flow Control)",
                 "Poka-Yoke / Error-Proofing", "Visual Management Boards",
                 "Standard Work documentation"],
                key="q3_2_tools",
            )
            st.text_input("3.2  Other Lean tool (optional)", key="q3_2_other")

        st.radio(
            "3.3  Has your enterprise implemented any Six Sigma tools or DMAIC?",
            ["Yes", "No"],
            index=None,
            key="q3_3",
        )

        # Skip logic: only show Q3.4 if Q3.3 == Yes
        if st.session_state.get("q3_3") == "Yes":
            st.multiselect(
                "3.4  Which Six Sigma tools have you used? (select all that apply)",
                ["DMAIC project framework", "Statistical Process Control (SPC)",
                 "FMEA (Failure Mode and Effects Analysis)",
                 "Root Cause Analysis (5 Whys / Fishbone)",
                 "Process Capability Analysis (Cpk)"],
                key="q3_4_tools",
            )
            st.text_input("3.4  Other Six Sigma tool (optional)", key="q3_4_other")

        st.multiselect(
            "3.5  What primarily motivated your interest in Lean / Six Sigma? (select up to 2)",
            ["Customer / OEM requirement or pressure", "Cost reduction objective",
             "Quality improvement target", "Production efficiency improvement",
             "Competitor advantage", "No specific motivation - not interested"],
            key="q3_5",
        )

        st.multiselect(
            "3.6  What key benefits have you observed after implementing LSS? (select up to 3)",
            ["Reduced defects and rework", "Increased production output",
             "Lower operational costs", "Faster lead times and deliveries",
             "Improved customer satisfaction scores", "Not applicable - no implementation yet"],
            key="q3_6",
        )

        col_back, col_next = st.columns(2)
        with col_back:
            st.button("← Back", on_click=go_back)
        with col_next:
            errors = []
            if st.session_state.get("q3_1") is None:
                errors.append("Q3.1 is required.")
            if len(st.session_state.get("q3_5", [])) > 2:
                errors.append("Q3.5: please select at most 2 motivations.")
            if len(st.session_state.get("q3_6", [])) > 3:
                errors.append("Q3.6: please select at most 3 benefits.")
            if errors:
                st.button("Next →", disabled=True)
                for e in errors:
                    st.error(e)
            else:
                st.button("Next →", on_click=go_next)


    # PAGE 3 - SECTION 4 (Barriers)
    elif st.session_state.page == 3:
        st.header(" Section 4 - Barriers")

        st.multiselect(
            "4.1  Main challenges preventing or limiting LSS adoption (select up to 3)",
            ["B1: Lack of awareness and knowledge about LSS concepts",
             "B2: High perceived implementation cost",
             "B3: Resistance to change from employees or owner",
             "B4: Lack of skilled workforce with quality improvement knowledge",
             "B5: Short-term financial focus",
             "B6: Difficulty collecting, recording, and analysing process data",
             "B7: Absence of government or institutional support for adoption",
             "B8: Insufficient customer or market pressure",
             "Other"],
            key="q4_1",
        )

        st.radio(
            "4.2  Do you believe LSS can benefit enterprises like yours?",
            ["Yes, definitely", "Maybe, but I am not sure how",
             "No, I do not think it is suitable for enterprises of my size"],
            key="q4_2",
        )

        st.multiselect(
            "4.3  What kind of support would most help your enterprise adopt LSS? (select up to 2)",
            ["Low-cost training programmes specifically for MSMEs",
             "Government incentives or subsidies for quality tool adoption",
             "Customer-driven requirements and supplier development support",
             "Access to affordable LSS consultants who understand MSMEs",
             "Industry networking forums and peer knowledge-sharing"],
            key="q4_3",
        )

        st.radio(
            "4.4  Would your enterprise participate in a pilot LSS framework trial (at no cost)?",
            ["Yes", "No"],
            key="q4_4",
        )

        col_back, col_next = st.columns(2)
        with col_back:
            st.button("← Back", on_click=go_back)
        with col_next:
            errors = []
            if len(st.session_state.get("q4_1", [])) > 3:
                errors.append("Q4.1: please select at most 3 challenges.")
            if len(st.session_state.get("q4_3", [])) > 2:
                errors.append("Q4.3: please select at most 2 support types.")
            if errors:
                st.button("Next →", disabled=True)
                for e in errors:
                    st.error(e)
            else:
                st.button("Next →", on_click=go_next)


    # PAGE 4 - SECTION 5 (Digital Technology Adoption)
    elif st.session_state.page == 4:
        st.header(" Section 5 - Digital Technology Adoption")

        st.multiselect(
            "5.1  What digital tools does your enterprise currently use? (select all that apply)",
            ["None - all records are paper-based",
             "MS Excel or Google Sheets for production tracking",
             "Basic accounting software (Tally, QuickBooks) - financial only",
             "ERP system (Tally Prime, Odoo, SAP B1) for production and quality",
             "Dedicated QMS software",
             "CAD / CAM software for production engineering",
             "IoT sensors or machine monitoring systems",
             "Cloud-based analytics or dashboard tools"],
            key="q5_1_tools",
        )
        st.text_input("5.1  Other digital tool (optional)", key="q5_1_other")

        st.radio(
            "5.2  How would you rate your enterprise's current level of digital technology adoption?",
            ["Level A - No digital tools; paper records only",
             "Level B - Basic digital only (spreadsheets, basic accounting)",
             "Level C - Intermediate digital (ERP, digital QMS, some production data tracking)",
             "Level D - Advanced digital (IoT, real-time analytics, integrated production management)"],
            key="q5_2",
        )

        st.radio(
            "5.3  Does your enterprise plan to invest in new digital tools in the next 12 months?",
            ["Yes - already planned and budgeted",
             "Yes - interested but not yet planned",
             "No - not a priority currently",
             "Uncertain"],
            key="q5_3",
        )

        st.radio(
            "5.4  Would you be open to a follow-up interview (about 20 minutes)?",
            ["Yes", "No"],
            key="q5_4",
        )

        col_back, col_submit = st.columns(2)
        with col_back:
            st.button("← Back", on_click=go_back)
        with col_submit:
            st.button("Submit →", on_click=go_next)


    # PAGE 5 - RESULT (scoring + DARMM heatmap)
    elif st.session_state.page == 5:
        st.header(" Your DARMM Result")

        # Safety check
        if st.session_state.get("q2_4") is None or st.session_state.get("q3_1") is None:
            st.error("Q2.4 (knowledge level) or Q3.1 (Lean implementation) was not "
                     "answered. Please go back and complete those questions.")
            st.button("← Back to the survey", on_click=go_back)
            st.stop()

        # Read every form value from session_state
        q2_1 = st.session_state.get("q2_1", "No")
        q2_2 = st.session_state.get("q2_2", "No")
        q2_4 = st.session_state.get("q2_4")
        q3_1 = st.session_state.get("q3_1", "No")
        q3_2_tools = st.session_state.get("q3_2_tools", [])
        q3_2_other = st.session_state.get("q3_2_other", "")
        q3_3 = st.session_state.get("q3_3", "No")
        q3_4_tools = st.session_state.get("q3_4_tools", [])
        q3_4_other = st.session_state.get("q3_4_other", "")
        q3_5 = st.session_state.get("q3_5", [])
        q3_6 = st.session_state.get("q3_6", [])
        q5_1_tools = st.session_state.get("q5_1_tools", [])
        q5_1_other = st.session_state.get("q5_1_other", "")
        q5_2 = st.session_state.get("q5_2", "Level A - No digital tools; paper records only")

        # Translation maps
        KNOWLEDGE_LEVEL_MAP = {
            "No knowledge at all": 1,
            "Basic awareness (heard of it, never implemented)": 2,
            "Moderate understanding (implemented some practices)": 3,
            "High understanding (actively use LSS in operations)": 4,
        }
        LEAN_TOOL_MAP = {
            "5S (Workplace Organisation)":                "5S",
            "Kaizen (Continuous Improvement Events)":     "Kaizen",
            "Value Stream Mapping (VSM)":                 "VSM",
            "Kanban (Inventory and Flow Control)":        "Kanban",
            "Poka-Yoke / Error-Proofing":                 "PokayYoke",
            "Visual Management Boards":                   "VisualManagement",
            "Standard Work documentation":                "StandardWork",
        }
        SS_TOOL_MAP = {
            "DMAIC project framework":                          "DMAIC",
            "Statistical Process Control (SPC)":                "SPC",
            "FMEA (Failure Mode and Effects Analysis)":         "FMEA",
            "Root Cause Analysis (5 Whys / Fishbone)":          "RCA",
            "Process Capability Analysis (Cpk)":                "Cpk",
        }
        DIGITAL_TOOL_MAP = {
            "None - all records are paper-based":                              "None",
            "MS Excel or Google Sheets for production tracking":               "Excel",
            "Basic accounting software (Tally, QuickBooks) - financial only":  "Accounting",
            "ERP system (Tally Prime, Odoo, SAP B1) for production and quality": "ERP",
            "Dedicated QMS software":                                          "QMS",
            "CAD / CAM software for production engineering":                   "CAD_CAM",
            "IoT sensors or machine monitoring systems":                       "IoT",
            "Cloud-based analytics or dashboard tools":                        "CloudAnalytics",
        }
        SELF_RATING_MAP = {
            "Level A - No digital tools; paper records only":                                  "A",
            "Level B - Basic digital only (spreadsheets, basic accounting)":                   "B",
            "Level C - Intermediate digital (ERP, digital QMS, some production data tracking)": "C",
            "Level D - Advanced digital (IoT, real-time analytics, integrated production management)": "D",
        }

        lean_tools_engine = []
        for t in q3_2_tools:
            if t in LEAN_TOOL_MAP:
                lean_tools_engine.append(LEAN_TOOL_MAP[t])

        ss_tools_engine = []
        for t in q3_4_tools:
            if t in SS_TOOL_MAP:
                ss_tools_engine.append(SS_TOOL_MAP[t])

        digital_tools_engine = []
        for t in q5_1_tools:
            if t in DIGITAL_TOOL_MAP:
                digital_tools_engine.append(DIGITAL_TOOL_MAP[t])

        real_motivations = []
        for m in q3_5:
            if m != "No specific motivation - not interested":
                real_motivations.append(m)
        if real_motivations:
            primary_motivation = ", ".join(real_motivations)
        else:
            primary_motivation = "Not applicable"

        real_benefits = []
        for b in q3_6:
            if b != "Not applicable - no implementation yet":
                real_benefits.append(b)
        if real_benefits:
            benefits_observed = ", ".join(real_benefits)
        else:
            benefits_observed = "Not applicable"

        engine_response = {
            "lean_awareness":     1 if q2_1 == "Yes" else 0,
            "ss_awareness":       1 if q2_2 == "Yes" else 0,
            "knowledge_level":    KNOWLEDGE_LEVEL_MAP[q2_4],
            "lean_implemented":   1 if q3_1 == "Yes" else 0,
            "lean_tools":         lean_tools_engine,
            "lean_other":         q3_2_other,
            "ss_implemented":     1 if q3_3 == "Yes" else 0,
            "ss_tools":           ss_tools_engine,
            "ss_other":           q3_4_other,
            "primary_motivation": primary_motivation,
            "benefits_observed":  benefits_observed,
            "digital_tools":      digital_tools_engine,
            "digital_other":      q5_1_other,
            "self_rating":        SELF_RATING_MAP[q5_2],
        }

        # Call the scoring engines
        lss_result = darmm_lss(engine_response)
        digital_result = darmm_digital(engine_response)
        # Save to Supabase (once per session)
        if not st.session_state.get("_response_saved"):
            cluster_name_db, _, _, source_db = get_pathway(
                lss_result["lss_level"], digital_result["digital_level"]
            )
            success, err = save_response(
                st.session_state, lss_result, digital_result,
                cluster_name_db, source_db
            )
            if success:
                st.session_state["_response_saved"] = True
                st.toast("Response saved to database")
            else:
                st.warning("Could not save to database: " + str(err))
        position = lss_result["lss_level"] + "-" + digital_result["digital_level"]

        st.success("Form submitted. Here is your DARMM position:")
        st.header("Your DARMM position: " + position)
        st.write("**LSS Operational Maturity:** " + lss_result["lss_level"] +
                 " - " + lss_result["lss_level_name"] +
                 "  (score " + str(lss_result["lss_score"]) + ")")
        st.write(lss_result["lss_level_desc"])
        st.write("**Digital Readiness:** " + digital_result["digital_level"] +
                 " - " + digital_result["digital_level_name"] +
                 "  (score " + str(digital_result["digital_score"]) + ")")
        st.write(digital_result["digital_level_desc"])

        # DARMM grid heatmap with respondent marker
        st.subheader("Your position on the DARMM grid")
        from db import fetch_all_responses
        df=fetch_all_responses()
        if df.empty or "darmm_position" not in df.columns:
            density=pd.DataFrame(0,index=["A","B","C","D"],columns=["L1","L2","L3","L4","L5"])
            n_total=0
        else:
            density=pd.crosstab(df["digital_level"],df["lss_level"])
            density=density.reindex(index=["A","B","C","D"],columns=["L1","L2","L3","L4","L5"],fill_value=0,)
            n_total=len(df)

        fig = go.Figure()

        # Layer 1: the heatmap (background colour = number of enterprises)
        fig.add_trace(go.Heatmap(
            z=density.values,
            x=density.columns.tolist(),
            y=density.index.tolist(),
            colorscale="Greens",
            text=density.values,
            texttemplate="%{text}",
            textfont={"size": 16},
            hovertemplate="LSS %{x}, Digital %{y}: %{z} enterprises<extra></extra>",
            colorbar=dict(title="Enterprises"),
        ))

        
        # Layer 2: red dot at the respondent's position
        fig.add_trace(go.Scatter(
            x=[lss_result["lss_level"]],
            y=[digital_result["digital_level"]],
            mode="markers+text",
            marker=dict(symbol="circle", size=22, color="red",
                        line=dict(color="white", width=2)),
            text=["YOU"],
            textposition="top center",
            textfont=dict(color="red", size=14),
            hovertemplate="You are here: " + position + "<extra></extra>",
            showlegend=False,
        ))

        fig.update_layout(
            title="Sector heatmap (n="+str(n_total)+ "MSMEs)",
            xaxis_title="LSS Operational Maturity",
            yaxis_title="Digital Readiness",
            height=450,
        )

        st.plotly_chart(fig, width='stretch')


        st.divider()
        st.subheader("Dashboard 1 - who responded")
        if df.empty or len(df)<2:
            st.info("Profile dashboard will populate as more MSMEs submit responses")
        else:
            col1,col2=st.columns(2)
            with col1:
                st.markdown("**Distribution by company size**")
                size_order=["Micro (1-9 employees)","Small (10-49 employees)","Medium (50-249 employees)"]
                size_counts=df["size_category"].value_counts().reindex(size_order,fill_value=0)
                fig_size=go.Figure(go.Bar(x=size_counts.index.tolist(),y=size_counts.values.tolist(),marker_color="#1a3f7f",text=size_counts.values.tolist(),textposition="outside",))
                fig_size.update_layout(height=320,xaxis_title="",yaxis_title="Number of MSMEs",showlegend=False,margin=dict(t=30,b=80),)    
                st.plotly_chart(fig_size,width='stretch')
            with col2:
                st.markdown("**Distribution by Customer Type**")
                cust_counts=df["primary_customer"].value_counts()
                fig_cust=go.Figure(go.Bar(
                    x=cust_counts.values.tolist(),y=cust_counts.index.tolist(),orientation="h",marker_color="#70AD47",text=cust_counts.values.tolist(),textposition="outside",))
                fig_cust.update_layout(height=320,xaxis_title="Number of MSMEs",yaxis_title="",showlegend=False,margin=dict(l=10,r=30),)
                st.plotly_chart(fig_cust,width='stretch')
        st.divider()
        st.subheader("Dashboard 2-LSS Awareness and adoption")
        if df.empty or len(df)<2:
            st.info("Awareness dashboard will populate as more MSMEs submit responses")
        else:
            st.markdown("**Lean vs Six Sigma Awareness by company size**")
            size_order=["Micro (1-9 employees)","Small (10-49 employees)","Medium (50-249 employees)"]
            aware_by_size=df.groupby("size_category").agg(lean_aware_pct=("lean_awareness","mean")   ,ss_aware_pct=("ss_awareness","mean"),)
            aware_by_size=(aware_by_size*100).reindex(size_order,fill_value=0)
            fig_aware=go.Figure()
            fig_aware.add_trace(go.Bar(name="Lean Awareness",x=aware_by_size.index.tolist(),y=aware_by_size["lean_aware_pct"].tolist(),marker_color="#4472c4",text=[str(int(v))+"%" for v in aware_by_size["lean_aware_pct"].tolist()],textposition="auto",) )
            fig_aware.add_trace(go.Bar(name="Six Sigma Awareness",x=aware_by_size.index.tolist(),y=aware_by_size["ss_aware_pct"].tolist(),marker_color="#F1843B",text=[str(int(v))+"%" for v in aware_by_size["ss_aware_pct"].tolist()],textposition="auto"))
            fig_aware.update_layout(barmode="group",height=350,xaxis_title="",yaxis_title="% of MSMEs aware",legend=dict(orientation="h",yanchor="bottom",y=-0.4),margin=dict(b=100),)
            st.plotly_chart(fig_aware,width='stretch') 

            col1,col2=st.columns(2)
            with col1:
                st.markdown("**LSS Adoption Funnel**")
                n_total=len(df)
                n_aware=int((df["lean_awareness"]==1).sum())
                n_impl_raw=int((df["lean_implemented"]==1).sum())
                tool_cols=["tool_5s","tool_kaizen","tool_vsm","tool_kanban","tool+pokayoke"]
                tool_cols_exist=[c for c in tool_cols if c in df.columns]
                if tool_cols_exist:
                    n_tools_per_row=df[tool_cols_exist].sum(axis=1)
                    n_structured=int(((df["lean_implemented"]==1) & (n_tools_per_row>=2)).sum())
                else:
                    n_structured=0
                fig_funnel=go.Figure(go.Funnel(y=["Total respondents","Lean aware","Lean implemented","Structured(2+ tools)"],x=[n_total,n_aware,n_impl_raw,n_structured],marker_color=["#4472C4","#5B9BD5","#70AD47","#A9D08E"],
                                               textposition="inside",textinfo="value+percent initial",))
                fig_funnel.update_layout(height=400,margin=dict(l=20,r=10,t=20,b=20),)
                st.plotly_chart(fig_funnel,width='stretch')
            with col2:
                st.markdown("**Most Common Lean Tools**")
                tool_labels = {
                    "tool_5s": "5S",
                    "tool_kaizen": "Kaizen",
                    "tool_vsm": "VSM",
                    "tool_kanban": "Kanban",
                    "tool_pokayoke": "Poka-Yoke",
                }   
                tool_data=[]
                for col,label in tool_labels.items():
                    if col in df.columns:
                        tool_data.append({"Tool":label,"Adoption":int((df[col]==1).sum())})
                tool_df=pd.DataFrame(tool_data).sort_values("Adoption",ascending=True)
                fig_tools=go.Figure(go.Bar(x=tool_df["Adoption"].tolist(),y=tool_df["Tool"].tolist(),orientation="h",marker_color="#7030A0",text=tool_df["Adoption"].tolist(),textposition="outside"))
                fig_tools.update_layout(height=400,xaxis_title="Number of MSMEs",yaxis_title="",margin=dict(l=10,r=40),) 
                st.plotly_chart(fig_tools,width='stretch')       


                
        st.divider()
        st.subheader("Dashboard 3- Barriers to LSS Adoption")
        if df.empty or len(df)<2:
            st.info("Barriers dashboard will populate as more MSMEs submits responses")
        else:
            def barrier_short(text):
                if not isinstance(text,str):
                    return "?"
                if text=="Other":
                    return "Other"
                if ":" in text:
                    return text.split(":",1)[0].strip()
                return text[:8]
            st.markdown("**All Barriers ranked by Frequencies**")
            barrier_counts=df["barriers"].explode().dropna().value_counts()
            fig_pareto=go.Figure(go.Bar(x=barrier_counts.values.tolist(),y=barrier_counts.index.tolist(),orientation="h",marker_color="#C00000",text=barrier_counts.values.tolist(),textposition="outside",))   
            fig_pareto.update_layout(height=400,xaxis_title="Number of MSMEs citing this barrier",yaxis_title="",yaxis=dict(autorange="reversed"),margin=dict(l=10,r=40),)
            st.plotly_chart(fig_pareto,width='stretch')
            col1,col2=st.columns(2)
            with col1:
                st.markdown("**Top 3 barriers by company sizes**")
                top3_barriers=barrier_counts.head(3).index.tolist()
                exploded = df[["size_category", "barriers"]].explode("barriers")
                exploded = exploded[exploded["barriers"].isin(top3_barriers)]
                exploded["barrier_short"] = exploded["barriers"].apply(barrier_short)
                cross=pd.crosstab(exploded["barrier_short"],exploded["size_category"]) 
                fig_grouped=go.Figure()
                for size in cross.columns:
                    fig_grouped.add_trace(go.Bar(name=size,x=cross.index.tolist(),y=cross[size].tolist(),))
                fig_grouped.update_layout(height=350,barmode="group",xaxis_title="",yaxis_title="Count",legend=dict(orientation="h",yanchor="bottom",y=-0.45),margin=dict(b=120),)
                st.plotly_chart(fig_grouped,width='stretch')
            with col2:
                st.markdown("**Do MSMEs believe LSS can benefit them?**")
                belief_counts=df["lss_benefit_belief"].dropna().value_counts()
                fig_belief=go.Figure(go.Pie(labels=belief_counts.index.tolist(),values=belief_counts.values.tolist(),hole=0.4,marker=dict(colors=["#70AD47","#FFC000","#C00000"]),
                                            ))
                fig_belief.update_layout(height=350,legend=dict(orientation="h",yanchor="bottom",y=-0.25),margin=dict(t=20,b=80),
                                         )        
                st.plotly_chart(fig_belief,width='stretch')
                    
                   
        # --- NEW: PDF download ---
        company_name_for_pdf = st.session_state.get("q1_1", "") or "Anonymous Enterprise"
        pdf_bytes = generate_report(
            engine_response, lss_result, digital_result, company_name_for_pdf
        )
        st.download_button(
            label=" Download your DARMM Assessment Report (PDF)",
            data=pdf_bytes,
            file_name="DARMM_Report_" + company_name_for_pdf.replace(" ", "_") + ".pdf",
            mime="application/pdf",
        )
        # --- end NEW ---

        st.button("Take the survey again", on_click=restart)

