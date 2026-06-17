import pandas as pd
import os
import streamlit as st
from analytics import(descrip_all,descrip_tools,descrip_numeric,descrip_by_size,table_4_1_sample_distri,table_4_2_digital,table_4_5_darmm,chart_lss_bysize,chart_adopt_bysize,chart_barr_freq,chart_awareness_adopt_gap,pearson_lss_digi,chi_awareness)
st.set_page_config(page_title="DARMM Research Dashboard",layout="wide")
_HERE=os.path.dirname(os.path.abspath(__file__))

_CSV_PATH=os.path.join(_HERE,"Survey_Dataset_120_MSMEs.csv")
st.title("DARMM Research Dashboard")
st.divider()
st.markdown("### Lean Six Sigma Awareness, Adoption, and Digital Readiness "
    "in General Engineering Manufacturing MSMEs — Bangalore, India"
)
st.caption("PhD Research | NIT Calicut |Jith John Francis(P230090ME) "
           "--Supervised by Dr.Vinay V. Panicker")
st.caption("120 Enterprises surveyed in Bangalore(chapter 4 data).")
st.divider()
st.header("Headline Percentages")


df=pd.read_csv(_CSV_PATH)
headline=descrip_all(df)
row1_c1,row1_c2,row1_c3=st.columns(3)
row1_c1.metric("Sample size ",str(headline["n"]))
row1_c2.metric("Lean aware",str(headline["lean_aware_pct"])+"%")
row1_c3.metric("Six Sigma Aware",str(headline["ss_aware_pct"])+"%")
 
row2_c1,row2_c2,row3_c3=st.columns(3)
row2_c1.metric("Lean Implemented",str(headline["lean_implemented_pct"])+"%")
row2_c2.metric("Six Sigma implemented",str(headline["ss_implemented_pct"])+"%")
row3_c3.metric("willing to pilot",str(headline["pilot_willing_pct"])+"%")
st.divider()
#--
st.header("Sample Distribution")
st.subheader("Table 4.1- sample by Industry,Size,Years,Cluster")
st.dataframe(table_4_1_sample_distri(df),width="stretch")

st.subheader("Table 4.2- Digital Readiness by MSME Size")
st.dataframe(table_4_2_digital(df),width="stretch")

st.subheader("Table 4.5--DARMM Grid Counts")
st.dataframe(table_4_5_darmm(df),width="stretch")
#--
st.divider()
st.header("Numeric Statistics")
st.dataframe(descrip_numeric(df),width="stretch")

st.subheader("Stats by Company size")
st.dataframe(descrip_by_size(df),width="stretch")

#--
st.divider()
st.header("Statistical Findings")
pear=pearson_lss_digi(df)
chi=chi_awareness(df)
#--
st.subheader("Pearson Correlation -LSS Maturity x Digital Readiness")
p_c1,p_c2,p_c3=st.columns(3)
p_c1.metric("r (correlation)",str(round(pear["r"],3)))
p_c2.metric("p-value","{:.2e}".format(pear["p"]))
p_c3.metric("n",str(pear["n"]))

if pear["p"]<0.001:
    sig_text="highly significant p<0.0001"
elif pear["p"]  <0.05:
    sig_text="significant p<0.05"
else:
    sig_text="not significant"

#--

st.subheader("Chi-square -LSS Awareness x Adoption")
c_c1,c_c2,c_c3,c_c4=st.columns(4)
c_c1.metric("Chi-sqaure",str(round(chi["chi square"],2)))  
c_c2.metric("p-value",'{:.2e}'.format(chi["p"])) 
c_c3.metric("dof",str(chi["dof"]))
c_c4.metric("n",str(chi["n"]))

if chi["p"]<0.001:
    chi_text="highly signficant (p<0.001)"
elif chi["p"]<0.05:
    chi_text="signficant(p<0.05)"
else:
    chi_text="not significant"


st.divider()
st.header("Charts")
st.subheader("LSS Awareness by Company Size")
st.plotly_chart(chart_lss_bysize(df),width="stretch")

st.subheader("Adoption by Company Size")
st.plotly_chart(chart_adopt_bysize(df),width="stretch")

st.subheader("Barrier Frequency")
st.plotly_chart(chart_barr_freq(df),width="stretch")

st.subheader("Awareness vs Adoption Gap by Knowledge level")
st.plotly_chart(chart_awareness_adopt_gap(df),width="stretch")
st.divider()



