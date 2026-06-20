import pandas as pd
import os
import streamlit as st
# from analytics import(descrip_all,descrip_tools,descrip_numeric,descrip_by_size,table_4_1_sample_distri,table_4_2_digital,table_4_5_darmm,chart_lss_bysize,chart_adopt_bysize,chart_barr_freq,chart_awareness_adopt_gap,pearson_lss_digi,chi_awareness)
st.set_page_config(page_title="DARMM Research Dashboard",layout="wide")
# _HERE=os.path.dirname(os.path.abspath(__file__))
import plotly.graph_objects as go
from db import fetch_all_responses
df=fetch_all_responses()
# _CSV_PATH=os.path.join(_HERE,"Survey_Dataset_120_MSMEs.csv")
st.title("DARMM Research Dashboard")
st.divider()
st.markdown("### Lean Six Sigma Awareness, Adoption, and Digital Readiness "
    "in General Engineering Manufacturing MSMEs — Bangalore, India"
)
st.caption("PhD Research | NIT Calicut |Jith John Francis(P230090ME) "
           "--Supervised by Dr.Vinay V. Panicker")

st.divider()


if df.empty or len(df) < 2:
    st.info("Bubble chart will populate as more MSMEs submit responses.")
else:
    import numpy as np

    # Jitter so overlapping bubbles spread visually
    np.random.seed(42)
    df["lss_jitter"] = (df["lss_score"] + np.random.uniform(-0.3, 0.3, size=len(df))).clip(lower=0)
    df["dig_jitter"] = (df["digital_score"] + np.random.uniform(-0.15, 0.15, size=len(df))).clip(lower=0)

    # Color mapping — one color per company size
    size_color_map = {
        "Micro (1-9 employees)":   "#4472C4",  # blue
        "Small (10-49 employees)": "#70AD47",  # green
        "Medium (50-249 employees)": "#ED7D31", # orange
    }

    fig = go.Figure()

    # Add ONE trace per size category
    for size_label, color in size_color_map.items():
        sub = df[df["size_category"] == size_label]
        if len(sub) == 0:
            continue
        fig.add_trace(go.Scatter(
            x=sub["lss_jitter"],
            y=sub["dig_jitter"],
            mode="markers",
            name=size_label,
            marker=dict(
                size=22,
                color=color,
                opacity=0.75,
                line=dict(width=2, color="white"),
            ),
            text=sub["darmm_position"],
            customdata=sub[["lss_score", "digital_score", "size_category"]].values,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "LSS Score: %{customdata[0]:.1f}<br>"
                "Digital Score: %{customdata[1]:.1f}<br>"
                "Size: %{customdata[2]}"
                "<extra></extra>"
            ),
        ))

    # Cutoff lines (added ONCE, after all traces)
    for x_cut in [2, 9, 13, 17]:
        fig.add_vline(x=x_cut, line_dash="dash", line_color="gray", opacity=0.4)
    for y_cut in [2.4, 5.4, 8.0]:
        fig.add_hline(y=y_cut, line_dash="dash", line_color="gray", opacity=0.4)

    # Zone labels at top (L1-L5)
    lss_zones = [("L1", 1), ("L2", 5.5), ("L3", 11), ("L4", 15), ("L5", 18.5)]
    for label, x_pos in lss_zones:
        fig.add_annotation(
            x=x_pos,
            y=0.98,
            xref="x",
            yref="paper",
            text="<b>" + label + "</b>",
            showarrow=False,
            font=dict(size=14, color="#FFC000"),
        )

    # Zone labels on the left (A-D)
    dig_zones = [("A", 1.2), ("B", 3.9), ("C", 6.7), ("D", 9.0)]
    for label, y_pos in dig_zones:
        fig.add_annotation(
            x=1.05,
            y=y_pos,
            xref="paper",
            yref="y",
            text="<b>" + label + "</b>",
            showarrow=False,
            font=dict(size=14, color="#FFC000"),
            
        )

    # Layout (added ONCE, after everything)
    fig.update_layout(
        title="DARMM Bubble Chart — LSS Maturity vs Digital Readiness<br>"
              "<sub>Bubble color = MSME size, Live data from " + str(len(df)) + " submissions</sub>",
        margin=dict(l=120, r=180, t=100, b=60),
        legend=dict(
            title="Company Size",
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
        ),
        xaxis=dict(
            title="LSS Maturity Score",
            range=[0, 20],
            tickmode="array",
            tickvals=[0, 2, 9, 13, 17, 20],
            ticktext=["0", "2", "9", "13", "17", "20"],
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)",
        ),
        yaxis=dict(
            title="Digital Readiness Score",
            range=[0, 10],
            tickmode="array",
            tickvals=[0, 2.4, 5.4, 8.0, 10],
            ticktext=["0", "2.4", "5.4", "8.0", "10"],
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)",
        ),
        height=600,
    )

    # Render chart (ONCE, at the end)
    st.plotly_chart(fig, use_container_width=True)

# df=pd.read_csv(_CSV_PATH)
# headline=descrip_all(df)
# row1_c1,row1_c2,row1_c3=st.columns(3)
# row1_c1.metric("Sample size ",str(headline["n"]))
# row1_c2.metric("Lean aware",str(headline["lean_aware_pct"])+"%")
# row1_c3.metric("Six Sigma Aware",str(headline["ss_aware_pct"])+"%")
 
# row2_c1,row2_c2,row3_c3=st.columns(3)
# row2_c1.metric("Lean Implemented",str(headline["lean_implemented_pct"])+"%")
# row2_c2.metric("Six Sigma implemented",str(headline["ss_implemented_pct"])+"%")
# row3_c3.metric("willing to pilot",str(headline["pilot_willing_pct"])+"%")
# st.divider()
# #--
# st.header("Sample Distribution")
# st.subheader("Table 4.1- sample by Industry,Size,Years,Cluster")
# st.dataframe(table_4_1_sample_distri(df),width="stretch")

# st.subheader("Table 4.2- Digital Readiness by MSME Size")
# st.dataframe(table_4_2_digital(df),width="stretch")

# st.subheader("Table 4.5--DARMM Grid Counts")
# st.dataframe(table_4_5_darmm(df),width="stretch")
# #--
# st.divider()
# st.header("Numeric Statistics")
# st.dataframe(descrip_numeric(df),width="stretch")

# st.subheader("Stats by Company size")
# st.dataframe(descrip_by_size(df),width="stretch")

# #--
# st.divider()
# st.header("Statistical Findings")
# pear=pearson_lss_digi(df)
# chi=chi_awareness(df)
# #--
# st.subheader("Pearson Correlation -LSS Maturity x Digital Readiness")
# p_c1,p_c2,p_c3=st.columns(3)
# p_c1.metric("r (correlation)",str(round(pear["r"],3)))
# p_c2.metric("p-value","{:.2e}".format(pear["p"]))
# p_c3.metric("n",str(pear["n"]))

# if pear["p"]<0.001:
#     sig_text="highly significant p<0.0001"
# elif pear["p"]  <0.05:
#     sig_text="significant p<0.05"
# else:
#     sig_text="not significant"

# #--

# st.subheader("Chi-square -LSS Awareness x Adoption")
# c_c1,c_c2,c_c3,c_c4=st.columns(4)
# c_c1.metric("Chi-sqaure",str(round(chi["chi square"],2)))  
# c_c2.metric("p-value",'{:.2e}'.format(chi["p"])) 
# c_c3.metric("dof",str(chi["dof"]))
# c_c4.metric("n",str(chi["n"]))

# if chi["p"]<0.001:
#     chi_text="highly signficant (p<0.001)"
# elif chi["p"]<0.05:
#     chi_text="signficant(p<0.05)"
# else:
#     chi_text="not significant"


# st.divider()
# st.header("Charts")
# st.subheader("LSS Awareness by Company Size")
# st.plotly_chart(chart_lss_bysize(df),width="stretch")

# st.subheader("Adoption by Company Size")
# st.plotly_chart(chart_adopt_bysize(df),width="stretch")

# st.subheader("Barrier Frequency")
# st.plotly_chart(chart_barr_freq(df),width="stretch")

# st.subheader("Awareness vs Adoption Gap by Knowledge level")
# st.plotly_chart(chart_awareness_adopt_gap(df),width="stretch")
# st.divider()


st.divider()
st.subheader("Dashboard 1 - who responded")
if df.empty or len(df)<2:
    st.info("Profile dashboard will populate as more MSMEs submit responses")
else:
    
    
    st.markdown("**Distribution by company size**")
    size_order=["Micro (1-9 employees)","Small (10-49 employees)","Medium (50-249 employees)"]
    size_counts=df["size_category"].value_counts().reindex(size_order,fill_value=0)
    fig_size=go.Figure(go.Bar(x=size_counts.index.tolist(),y=size_counts.values.tolist(),marker_color="#1a3f7f",text=size_counts.values.tolist(),textposition="outside",))
    fig_size.update_layout(height=500,xaxis_title="",yaxis_title="Number of MSMEs",showlegend=False,margin=dict(t=30,b=80),)    
    st.plotly_chart(fig_size,width="stretch")

    st.markdown("**Distribution by Customer Type**")
    cust_counts=df["primary_customer"].value_counts()
    fig_cust=go.Figure(go.Bar(
        x=cust_counts.values.tolist(),y=cust_counts.index.tolist(),orientation="h",marker_color="#70AD47",text=cust_counts.values.tolist(),textposition="outside",))
    fig_cust.update_layout(height=500,xaxis_title="Number of MSMEs",yaxis_title="",showlegend=False,margin=dict(l=10,r=30),)
    st.plotly_chart(fig_cust,width="stretch")
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
    st.plotly_chart(fig_aware,width="stretch") 
    st.markdown("**LSS Adoption Funnel**")
    n_total=len(df)
    n_aware=int((df["lean_awareness"]==1).sum())
    n_impl_raw=int((df["lean_implemented"]==1).sum())
    tool_cols=["tool_5s","tool_kaizen","tool_vsm","tool_kanban","tool_pokayoke"]
    tool_cols_exist=[c for c in tool_cols if c in df.columns]
    if tool_cols_exist:
        n_tools_per_row=df[tool_cols_exist].sum(axis=1)
        n_structured=int(((df["lean_implemented"]==1) & (n_tools_per_row>=2)).sum())
    else:
        n_structured=0
    fig_funnel=go.Figure(go.Funnel(y=["Total respondents","Lean aware","Lean implemented","Structured(2+ tools)"],x=[n_total,n_aware,n_impl_raw,n_structured],marker_color=["#4472C4","#5B9BD5","#70AD47","#A9D08E"],
                                    textposition="inside",textinfo="value+percent initial",))
    fig_funnel.update_layout(height=400,margin=dict(l=20,r=10,t=20,b=20),)
    st.plotly_chart(fig_funnel,width="stretch")

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
    st.plotly_chart(fig_tools,width="stretch")       


        
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
    st.plotly_chart(fig_pareto,width="stretch")
    
   
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
    st.plotly_chart(fig_grouped,width="stretch")

    st.markdown("**Do MSMEs believe LSS can benefit them?**")
    belief_counts=df["lss_benefit_belief"].dropna().value_counts()
    fig_belief=go.Figure(go.Pie(labels=belief_counts.index.tolist(),values=belief_counts.values.tolist(),hole=0.4,marker=dict(colors=["#70AD47","#FFC000","#C00000"]),
                                ))
    fig_belief.update_layout(height=350,legend=dict(orientation="h",yanchor="bottom",y=-0.25),margin=dict(t=20,b=80),
                                )        
    st.plotly_chart(fig_belief,width="stretch")
        
        
