import os
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import pearsonr, chi2_contingency

_HERE = os.path.dirname(os.path.abspath(__file__))


def load_data(data_path=None):
    if data_path is None:
        data_path = os.path.join(_HERE, "Survey_Dataset_120_MSMEs.csv")
    return pd.read_csv(data_path)
def validate_data(df):
    issues={}
    missing=df.isnull().sum()
    cols_with_missing=missing[missing>0]
    if len(cols_with_missing)>0:
        issues["missing_values"]=cols_with_missing.to_dict()

    yes_no_cols=[c for c in df.columns if c.endswith("_1Yes_0No")] 
    for col in yes_no_cols:
        unique_vals=df[col].dropna().unique()
        valid=set(unique_vals).issubset({0,1}) 
        if not valid:
            issues.setdefault("invalid_binary_values",{})[col]=list(unique_vals)

    knowledge_col="S2_Q4_Knowledge_Level_1to4"
    if knowledge_col in df.columns:
        bad=df[(df[knowledge_col]<1)| (df[knowledge_col]>4)]
        if len(bad)>0:
            issues["invalid_knowledge_levels"]=len(bad)



    size_col="S1_Size_Category"
    if size_col in df.columns:
        expected={"Micro","Small","Medium"}
        actual=set(df[size_col].dropna().unique())
        extras=actual-expected         
        if extras:
            issues["unexpected_size_labels"]=list(extras)


    lss_lvl_col="DARMM_LSS_Level"
    if lss_lvl_col in df.columns:
        expected={"L1","L2","L3","L4","L5"} 
        ACTUAL=set(df[lss_lvl_col].dropna().unique())
        extras=ACTUAL-expected
        if extras:
            issues["unexpected_lss_levels"]=list(extras)
    dig_lvl_col="DARMM_Digital_Level"
    if dig_lvl_col in df.columns:
        expected={"A","B","C","D"}
        actual=set(df[dig_lvl_col].dropna().unique())
        extras=actual-expected
        if extras:
            issues["unexpected_digital_levels"]=list(extras)
    return issues

##headline percentages
def descrip_all(df):
    stats={
        "n":len(df),
         "lean_aware_pct":       round(df["S2_Q1_Lean_Awareness_1Yes_0No"].mean() * 100, 1),
        "ss_aware_pct":         round(df["S2_Q2_Six_Sigma_Awareness_1Yes_0No"].mean() * 100, 1),
        "lean_implemented_pct": round(df["S3_Q1_Lean_Implemented_1Yes_0No"].mean() * 100, 1),
        "ss_implemented_pct":   round(df["S3_Q3_SS_Implemented_1Yes_0No"].mean() * 100, 1),
        "pilot_willing_pct":    round(df["S4_Q_Pilot_Trial_Willing_1Yes_0No"].mean() * 100, 1),                     
    }   
    return stats

##tool adoption rates
def descrip_tools(df):
    lean_tools = [
        ("S3_Q2a_Tool_5S_1Yes_0No",        "5S"),
        ("S3_Q2b_Tool_Kaizen_1Yes_0No",    "Kaizen"),
        ("S3_Q2c_Tool_VSM_1Yes_0No",       "VSM"),
        ("S3_Q2d_Tool_Kanban_1Yes_0No",    "Kanban"),
        ("S3_Q2e_Tool_PokayYoke_1Yes_0No", "Poka-Yoke"),
    ]
    ss_tools = [
        ("S3_Q4a_Tool_DMAIC_1Yes_0No", "DMAIC"),
        ("S3_Q4b_Tool_SPC_1Yes_0No",   "SPC"),
        ("S3_Q4c_Tool_FMEA_1Yes_0No",  "FMEA"),
        ("S3_Q4d_Tool_RCA_1Yes_0No",   "RCA"),
    ]
    rows=[]
    for col,name in lean_tools:
        rows.append({
            "Methodology":"Lean",
            "Tool": name,
            "% Adopted":round(df[col].mean()*100,1),

        })
    for col,name in ss_tools:
        rows.append({
            "Methodology":"Six Sigma",
            "Tool": name,
            "% Adopted":round(df[col].mean()*100,1),

        })
    return pd.DataFrame(rows).sort_values("% Adopted",ascending=False)       



#numeric stats
def descrip_numeric(df):
    cols=[
         "S2_Q4_Knowledge_Level_1to4",
        "DARMM_LSS_Maturity_Score_0to20",
        "DARMM_Digital_Readiness_Score_0to10",
        "Total_Barriers_Selected",
    ]
    summary=df[cols].describe().round(2)
    return summary



##msme size
def descrip_by_size(df):
    """Awareness and adoption percentages by MSME size category."""
    grouped = df.groupby("S1_Size_Category").agg(
        n=("Enterprise_ID", "count"),
        lean_aware_pct=("S2_Q1_Lean_Awareness_1Yes_0No", lambda x: round(x.mean() * 100, 1)),
        ss_aware_pct=("S2_Q2_Six_Sigma_Awareness_1Yes_0No", lambda x: round(x.mean() * 100, 1)),
        lean_implemented_pct=("S3_Q1_Lean_Implemented_1Yes_0No", lambda x: round(x.mean() * 100, 1)),
        ss_implemented_pct=("S3_Q3_SS_Implemented_1Yes_0No", lambda x: round(x.mean() * 100, 1)),
        mean_lss_score=("DARMM_LSS_Maturity_Score_0to20", "mean"),
        mean_digital_score=("DARMM_Digital_Readiness_Score_0to10", "mean"),
    ).reset_index()
    grouped["mean_lss_score"]     = grouped["mean_lss_score"].round(2)
    grouped["mean_digital_score"] = grouped["mean_digital_score"].round(2)
    return grouped

def table_4_1_sample_distri(df):
    counts=df["S1_Size_Category"].value_counts()
    total=len(df)
    table=pd.DataFrame({
        "MSME Category":counts.index,
        "No. of Enterprises":counts.values,
        "% of Sample":(counts.values/total*100).round(1),
    })
    total_row=pd.DataFrame({
        "MSME Category": ["Total"],
        "No. of Enterprises": [total],
        "% of Sample": [100.0],
    })

    table = pd.concat([table, total_row], ignore_index=True)
    return table


def table_4_2_digital(df):
    table=pd.crosstab(df["DARMM_Digital_Level"],df["S1_Size_Category"],margins=True,margins_name="Overall",) 
    order=["A","B","C","D","Overall"]
    table=table.reindex(order)
    cols=["Micro","Small","Medium","Overall"]
    table=table[cols]
    return table   

def table_4_5_darmm(df):
    grid=pd.crosstab(df["DARMM_Digital_Level"],df["DARMM_LSS_Level"],)
    grid=grid.reindex(index=["D","C","B","A"],columns=["L1","L2","L3","L4","L5"],fill_value=0)
    return grid


def chart_lss_bysize(df):
    awareness_table=df.groupby("S1_Size_Category").agg( lean_aware=("S2_Q1_Lean_Awareness_1Yes_0No", "mean"),
        ss_aware=("S2_Q2_Six_Sigma_Awareness_1Yes_0No", "mean"),
    ).reset_index()
    awareness_table["lean_aware"] *= 100
    awareness_table["ss_aware"] *= 100

    fig=go.Figure()
    fig.add_trace(go.Bar(x=awareness_table["S1_Size_Category"],y=awareness_table["lean_aware"],name="Lean awareness",)) 
    fig.add_trace(go.Bar(x=awareness_table["S1_Size_Category"],y=awareness_table["ss_aware"],name="Six Sigma awareness",))
    fig.update_layout(title="LSS aware by MSME sizes",xaxis_title="MSME size category",yaxis_title="% Aware",barmode="group",height=400,)
    return fig


def chart_adopt_bysize(df):
        table=df.groupby("S1_Size_Category").agg(

            lean_impl=("S3_Q1_Lean_Implemented_1Yes_0No","mean"),
            ss_impl=("S3_Q3_SS_Implemented_1Yes_0No","mean"),
        ).reset_index() 
        table["lean_impl"]*=100 
        table["ss_impl"]*=100
        fig=go.Figure()
        fig.add_trace(go.Bar(
            x=table["S1_Size_Category"],y=table["lean_impl"],
            name="Lean implemented",
        ))
        fig.add_trace(go.Bar(
            x=table["S1_Size_Category"],y=table["ss_impl"],
            name="Six Sigma Implemented",
        ))
        fig.update_layout(
            title="Implementation Rate by MSME Size",
            xaxis_title="MSME Size Category",
            yaxis_title="Implementation Rate (%)",
            barmode="group",
            height=400,
        )
        return fig


def chart_barr_freq(df):
    barrier_cols = [
        ("S4_B1_Lack_Awareness_Knowledge", "B1: Lack of awareness"),
        ("S4_B2_High_Implementation_Cost", "B2: High cost"),
        ("S4_B3_Resistance_to_Change", "B3: Resistance to change"),
        ("S4_B4_Lack_Skilled_Workforce", "B4: Lack of skilled workforce"),
        ("S4_B5_Short_Term_Financial_Focus", "B5: Short-term focus"),
        ("S4_B6_Difficulty_Data_Collection", "B6: Data collection difficulty"),
        ("S4_B7_No_Govt_Institutional_Support", "B7: No govt support"),
        ("S4_B8_No_Customer_Market_Pressure", "B8: No market pressure"),
    ]
    rows = []
    for col, label in barrier_cols:
        rows.append({"Barrier": label, "% citing": df[col].mean() * 100})
    barrier_df = pd.DataFrame(rows).sort_values("% citing", ascending=True)

    fig = go.Figure(go.Bar(
        x=barrier_df["% citing"],
        y=barrier_df["Barrier"],
        orientation="h",
    ))
    fig.update_layout(
        title="Most Cited Barriers to LSS Adoption",
        xaxis_title="% of Respondents Citing",
        height=400,
    )
    return fig

def chart_awareness_adopt_gap(df):
    crosstab=pd.crosstab(df["S2_Q1_Lean_Awareness_1Yes_0No"],df["S3_Q1_Lean_Implemented_1Yes_0No"],)
    crosstab.index=["not aware","aware"]
    crosstab.columns=["not implemented","implemented"]
    fig=go.Figure()
    fig.add_trace(go.Bar(x=crosstab.index,y=crosstab["not implemented"],name="not implemented",))
    fig.add_trace(go.Bar(x=crosstab.index,y=crosstab["implemented"],name="implemented",))
    fig.update_layout(title="awareness vs adoption gap",xaxis_title="lean awareness status",yaxis_title="number of enterprises",barmode="stack",height=400,)
    return fig


def pearson_lss_digi(df):
    r,p =pearsonr(df["DARMM_LSS_Maturity_Score_0to20"],df["DARMM_Digital_Readiness_Score_0to10"],)
    return {
        "r":round(r,4),
        "p": p,
        "n":len(df),
    }


def chi_awareness(df):
    ct=pd.crosstab(df["S2_Q1_Lean_Awareness_1Yes_0No"],df["S3_Q1_Lean_Implemented_1Yes_0No"],)
    chi2,p,dof,_=chi2_contingency(ct)
    return {
        "chi square":round(chi2,3),
        "p":p,
        "dof":dof,
        "n":len(df),}
