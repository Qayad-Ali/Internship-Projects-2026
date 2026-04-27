import streamlit as st
import matplotlib.pyplot as plt
import statistics

st.title("Quality Data Analysis Tool")
st.markdown("""
<style>
.stApp {
    background-color: #384959 ;
   
}
</style>
""", unsafe_allow_html=True)
# ── INPUTS ──────────────────────────────────────────────
st.header("Input Data")
st.subheader("Dimension Data")
dim_input = st.text_input(
    "Dimension values (comma separated, in mm)",
    value="10.1, 10.3, 9.8, 10.5, 10.2, 9.7, 10.4, 10.6, 9.9, 10.2"
)

col1, col2 = st.columns(2)
with col1:
    target = st.number_input("Target value (mm)", value=10.0)
with col2:
    tolerance = st.number_input("Tolerance (±mm)", value=0.3)
st.divider()
st.subheader("Defect Counts")
col3, col4, col5, col6 = st.columns(4)
with col3:
    scratch = st.number_input("Scratch", value=35, min_value=0)
with col4:
    dent = st.number_input("Dent", value=25, min_value=0)
with col5:
    crack = st.number_input("Crack", value=15, min_value=0)
with col6:
    others = st.number_input("Others", value=10, min_value=0)

# ANALYSIS 
if st.button("Run Analysis"):
    st.divider()


    # Parse dimension vals
    vals = [float(x.strip()) for x in dim_input.split(",") if x.strip()]

    st.header("Dimension Analysis")

    mean  = statistics.mean(vals)
    lo    = target - tolerance
    hi    = target + tolerance
    out_of_spec = [v for v in vals if v < lo or v > hi]

    st.write(f"*Mean:*{mean:.3f} mm")
    st.write(f"*Minimum:* {min(vals)} mm")
    st.write(f"*Maximum:* {max(vals)} mm")
    st.write(f"*Tolerance band:* {lo:.2f} mm  –  {hi:.2f} mm")

    if out_of_spec:
        st.error(f"Out-of-spec values: {out_of_spec}")
    else:
        st.success("All values are within tolerance.")

    # Run chart
   
    st.divider()

    #DEFECT ANALYSIS
    st.header("Defect Analysis")

    defects = {"Scratch": scratch, "Dent": dent, "Crack": crack, "Others": others}
    total   = sum(defects.values())
    sorted_defects = dict(sorted(defects.items(), key=lambda x: x[1], reverse=True))
    top_defect = list(sorted_defects.keys())[0]

    st.write(f"**Total defects:** {total}")
    st.write(f"**Major defect:** {top_defect} ({defects[top_defect]} count)")

    st.subheader("Defect Contribution")
    for name, count in sorted_defects.items():
        pct = 100 * count / total
        st.write(f"- {name}: {count}  ({pct:.1f}%)")

    # Bar chart
    fig2, ax2 = plt.subplots()
    fig2.patch.set_facecolor('#384959')   
    ax2.set_facecolor('#2F3D4C')          

    ax2.bar(sorted_defects.keys(), sorted_defects.values(), color=["#e74c3c","#3498db","#2ecc71","#f39c12"])
    ax2.set_xlabel("Defect Type")
    ax2.set_ylabel("Count")
    ax2.set_title("Defect Count by Type")
    st.pyplot(fig2)
    
