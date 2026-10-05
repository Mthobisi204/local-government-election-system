
import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="eThekwini 2026 Election ML Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).parent
OUT = ROOT / "outputs"

st.markdown("""
<style>
.main {background-color:#f7f8fa;}
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
.hero {
    padding: 1.4rem 1.6rem;
    border-radius: 18px;
    background: linear-gradient(135deg,#111827,#334155);
    color:white;
    margin-bottom: 1rem;
}
.badge {
    display:inline-block;
    padding:0.25rem 0.6rem;
    border-radius:999px;
    background:#e2e8f0;
    color:#0f172a;
    font-size:0.78rem;
    font-weight:600;
    margin-right:0.35rem;
}
.warning {
    padding:0.8rem 1rem;
    border-left:5px solid #f59e0b;
    background:#fff7ed;
    border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>eThekwini 2026 Local Government Election</h1>
<p>Machine-learning analytical dashboard — 4 November 2026</p>
<span class="badge">Historical data</span>
<span class="badge">Geographic alignment</span>
<span class="badge">Model outputs</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("Project navigation")
page = st.sidebar.radio(
    "Select view",
    ["Overview","Metro result","Three wards","Turnout","Model evaluation","Methodology"]
)

st.sidebar.markdown("---")
st.sidebar.caption("This dashboard reports statistical model outputs. It does not predict which party or coalition will govern.")

def read_output(name):
    path = OUT / name
    if not path.exists():
        return None
    return pd.read_csv(path)

metro = read_output("metro_party_projection.csv")
wards = read_output("ward_projection.csv")
turnout = read_output("turnout_projection.csv")
evaluation = read_output("model_evaluation.csv")
selected = read_output("selected_wards.csv")

if page == "Overview":
    st.subheader("Project overview")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Study area","eThekwini")
    c2.metric("Prediction date","04 Nov 2026")
    c3.metric("Prediction geography","2026 wards")
    c4.metric("Model families","Regression + classification")

    st.markdown("""
    ### Analytical outputs
    **1. Metro:** projected vote share/votes and a mathematical 50% threshold check.  
    **2. Wards:** three selected wards with geographically defensible historical alignment.  
    **3. Parties:** projected vote totals and shares for all modelled relevant parties.  
    **4. Turnout:** projected turnout rate and estimated number of voters.
    """)
    st.markdown("""
    <div class="warning">
    <b>Interpretation rule:</b> 2021/2024 observations are historical; geographic reallocations and changes are derived estimates; 2026 values are model outputs. A projected leading party is not reported as the future governing party.
    </div>
    """, unsafe_allow_html=True)

elif page == "Metro result":
    st.subheader("1. Metro-wide projected result")
    if metro is None:
        st.error("Run the notebook first to create outputs/metro_party_projection.csv.")
    else:
        m = metro.copy()
        if "projected_share" in m:
            m["Projected vote share (%)"] = m["projected_share"]*100
        if "projected_votes" in m:
            m["Projected votes"] = m["projected_votes"]
        st.dataframe(m, use_container_width=True)
        if "projected_share" in m:
            chart = m.set_index("party")["projected_share"]*100
            st.bar_chart(chart)
            leader = m.sort_values("projected_share", ascending=False).iloc[0]
            st.success(f"Model output: largest projected aggregate vote share = {leader['party']} ({leader['projected_share']*100:.1f}%).")
            if leader["projected_share"] >= 0.50:
                st.info("The largest projected party crosses the 50% vote-share threshold. This is a mathematical threshold assessment, not a governing prediction.")
            else:
                st.info("No party crosses the 50% vote-share threshold in the model output. This indicates a possible mathematical coalition requirement, not a prediction of coalition formation.")

elif page == "Three wards":
    st.subheader("2. Three selected wards")
    if wards is None:
        st.error("Run the notebook first to create outputs/ward_projection.csv.")
    else:
        st.dataframe(wards, use_container_width=True)
        if {"ward_2026","projected_leader"}.issubset(wards.columns):
            st.bar_chart(
                wards.groupby("ward_2026")["projected_leader"].value_counts()
                .unstack(fill_value=0)
            )
    if selected is not None:
        st.caption("Selection rule: stable stronghold, competitive ward and political-transition ward, after geographic alignment.")
        st.dataframe(selected, use_container_width=True)

elif page == "Turnout":
    st.subheader("4. Projected voter turnout")
    if turnout is None:
        st.error("Run the notebook first to create outputs/turnout_projection.csv.")
    else:
        st.dataframe(turnout, use_container_width=True)
        if "projected_turnout_rate" in turnout.columns:
            rate = float(turnout["projected_turnout_rate"].iloc[0])
            st.metric("Projected turnout", f"{rate*100:.1f}%")
        if "projected_voters" in turnout.columns:
            voters = int(round(turnout["projected_voters"].iloc[0]))
            st.metric("Estimated voters", f"{voters:,}")

elif page == "Model evaluation":
    st.subheader("Model validation and evaluation")
    if evaluation is None:
        st.error("Run the notebook first to create outputs/model_evaluation.csv.")
    else:
        st.dataframe(evaluation, use_container_width=True)
        st.caption("Lower MAE/RMSE is better. Higher R² is better. Classification uses accuracy and balanced accuracy.")

elif page == "Methodology":
    st.subheader("Reproducible methodology")
    st.markdown("""
    ### Data acquisition
    IEC election results, IEC Atlas/geographic information, Stats SA Census 2022, Municipal Demarcation Board ward geography, and latest available voter-registration/candidate information.

    ### Geographic alignment
    Historical results are aligned to 2026 wards through voting districts or spatial weights. Ward numbers alone are never treated as stable geographic identifiers.

    ### Modelling
    - Party share: Random Forest regression with Linear Regression benchmark.
    - Ward leader: Random Forest multiclass classification.
    - Turnout: Gradient Boosting regression with Random Forest benchmark.

    ### Validation
    Historical/time-aware backtesting is used to avoid leakage from future elections.

    ### Evidence labels
    **Historical observation** = directly observed.  
    **Derived/aligned estimate** = calculated from historical observations.  
    **2026 model output** = generated by the fitted model.

    ### Governance
    The dashboard does not model coalition negotiations or predict who will govern.
    """)
