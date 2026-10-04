import sys
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st
from langgraph.types import Command

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from app.graph.workflow import synapse_graph

st.set_page_config(
    page_title="Synapse-AI | Enterprise Decision Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
.stApp{background:#0b0f14}
.main .block-container{max-width:1480px;padding:1.8rem 3rem 2rem}
.brand{display:flex;align-items:center;gap:14px;margin-bottom:2px}
.brand-mark{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#1d8cf8,#16c6a3);display:flex;align-items:center;justify-content:center;color:white;font-size:22px;font-weight:800}
.brand-name{font-size:32px;font-weight:750;letter-spacing:-1px;color:#f4f7fb}
.brand-subtitle{color:#8d98a8;font-size:15px;margin-left:56px;margin-bottom:24px}
.section-label{color:#dfe6ef;font-size:17px;font-weight:650;margin:20px 0 10px}
.status-chip{display:inline-block;padding:6px 11px;border-radius:999px;background:#12261f;border:1px solid #205b48;color:#55d6a7;font-size:12px;font-weight:600;margin-right:6px}
div[data-testid="stMetric"]{background:#111720;border:1px solid #202936;border-radius:14px;padding:14px 16px;min-height:105px}
div[data-testid="stMetricLabel"]{color:#8d98a8}div[data-testid="stMetricValue"]{color:#f4f7fb;font-size:25px}
.stButton>button{border-radius:9px;font-weight:650;min-height:42px}
.action-card{background:#111720;border:1px solid #252e3a;border-left:3px solid #2f8df5;border-radius:10px;padding:14px 16px;margin-bottom:10px}
.action-title{color:#eef3f8;font-size:14px;font-weight:650}.action-meta{color:#8d98a8;font-size:12px;margin-top:5px}
.risk-card{border-radius:14px;padding:20px;border:1px solid #303846;background:#111720}.risk-high{border-color:#7d3434;background:#241316}.risk-medium{border-color:#80682d;background:#241f13}.risk-low{border-color:#28634f;background:#12221d}
.risk-number{font-size:38px;font-weight:750;color:#f4f7fb}.risk-label{color:#9aa5b4;font-size:12px;text-transform:uppercase;letter-spacing:.8px}
.policy-card{background:#0e151d;border:1px solid #202936;border-radius:10px;padding:14px 16px;color:#b9c3cf;font-size:13px;line-height:1.55}
.review-banner{background:linear-gradient(90deg,rgba(29,140,248,.10),rgba(22,198,163,.06));border:1px solid #284766;border-radius:14px;padding:18px 20px;margin:18px 0 14px}
.review-title{color:#eef5fc;font-size:18px;font-weight:700}.review-text{color:#93a1b2;font-size:13px;margin-top:5px}
.footer{text-align:center;color:#586474;font-size:11px;padding:28px 0 8px}
hr{border-color:#202936!important}
</style>
""", unsafe_allow_html=True)

for key, default in {
    "workflow_result": None,
    "interrupt_data": None,
    "thread_id": "streamlit-session-1",
    "modify_mode": False,
    "uploaded_df": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.markdown("""
<div class="brand"><div class="brand-mark">◈</div><div class="brand-name">Synapse-AI</div></div>
<div class="brand-subtitle">Enterprise Agentic Decision Intelligence</div>
<span class="status-chip">Decision Intelligence</span>
<span class="status-chip">Policy Grounded</span>
<span class="status-chip">Human Governed</span>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Business Analysis Request</div>', unsafe_allow_html=True)
question = st.text_area("Business question", placeholder="Describe the business problem you want Synapse-AI to analyze...", height=80, label_visibility="collapsed")
col_upload, col_run = st.columns([4,1])
with col_upload:
    uploaded_file = st.file_uploader("Business dataset", type=["csv"], label_visibility="collapsed")
with col_run:
    run_clicked = st.button("Run Analysis", type="primary", use_container_width=True)

if run_clicked:
    if not question:
        st.warning("Please enter a business question.")
    elif not uploaded_file:
        st.warning("Please upload a CSV dataset.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            file_path = temp_file.name
        st.session_state.uploaded_df = pd.read_csv(file_path)
        initial_state = {"file_path": file_path, "user_question": question}
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        with st.spinner("Synapse-AI is analyzing the business problem..."):
            result = synapse_graph.invoke(initial_state, config=config)
        if "__interrupt__" in result:
            st.session_state.interrupt_data = result["__interrupt__"][0].value
            st.session_state.workflow_result = None
        else:
            st.session_state.workflow_result = result
            st.session_state.interrupt_data = None
        st.rerun()

if st.session_state.interrupt_data:
    interrupt_data = st.session_state.interrupt_data
    st.markdown("---")
    st.markdown('<div class="review-banner"><div class="review-title">Human Review Required</div><div class="review-text">Review the AI-generated recommendations before finalizing the decision.</div></div>', unsafe_allow_html=True)
    for action in interrupt_data.get("actions", []):
        st.markdown(f'<div class="action-card"><div class="action-title">{action["action"]}</div><div class="action-meta">Priority: <b>{action["priority"]}</b> &nbsp;•&nbsp; {action["reason"]}</div></div>', unsafe_allow_html=True)
    col1,col2,col3=st.columns(3)
    config={"configurable":{"thread_id":st.session_state.thread_id}}
    with col1:
        if st.button("Approve Recommendation", type="primary", use_container_width=True):
            decision={"status":"APPROVED","message":"Human approved the proposed actions."}
            st.session_state.workflow_result=synapse_graph.invoke(Command(resume=decision),config=config)
            st.session_state.interrupt_data=None
            st.rerun()
    with col2:
        if st.button("Modify Recommendation", use_container_width=True): st.session_state.modify_mode=True
    with col3:
        if st.button("Reject Recommendation", use_container_width=True):
            decision={"status":"REJECTED","message":"Human rejected the proposed actions."}
            st.session_state.workflow_result=synapse_graph.invoke(Command(resume=decision),config=config)
            st.session_state.interrupt_data=None
            st.rerun()
    if st.session_state.modify_mode:
        modification=st.text_area("Modification",placeholder="Describe the change to the recommendation...")
        if st.button("Submit Modification",type="primary") and modification:
            decision={"status":"MODIFIED","message":modification}
            st.session_state.workflow_result=synapse_graph.invoke(Command(resume=decision),config=config)
            st.session_state.interrupt_data=None
            st.session_state.modify_mode=False
            st.rerun()

result=st.session_state.workflow_result
if result:
    st.markdown("---")
    st.markdown('<div class="section-label">Business Health Overview</div>',unsafe_allow_html=True)
    analysis=result.get("analysis",{})
    numeric=analysis.get("numeric_summary",{})
    if numeric:
        cols=st.columns(4)
        for i,column in enumerate(list(numeric.keys())[:4]):
            with cols[i]:
                st.metric(column.replace("_"," ").title(),f"{numeric[column]['mean']:,.2f}","Average")

    left,right=st.columns([1.35,1])
    with left:
        st.markdown('<div class="section-label">Business Insights</div>',unsafe_allow_html=True)
        insights=result.get("insights",[])
        if insights:
            for insight in insights:
                st.markdown(f'<div class="action-card"><div class="action-title">{insight}</div></div>',unsafe_allow_html=True)
        else: st.info("No specific business insights were generated.")
    with right:
        st.markdown('<div class="section-label">Risk Assessment</div>',unsafe_allow_html=True)
        risk=result.get("risk",{})
        score=risk.get("risk_score",0); level=risk.get("risk_level","LOW"); recommended=risk.get("recommended_action","Continue monitoring")
        cls={"HIGH":"risk-high","MEDIUM":"risk-medium","LOW":"risk-low"}.get(level,"risk-low")
        st.markdown(f'<div class="risk-card {cls}"><div class="risk-label">Risk Score</div><div class="risk-number">{score}/100</div><div class="risk-label">{level} RISK</div><br><div class="action-meta">Recommended response: {recommended}</div></div>',unsafe_allow_html=True)
        reasons=risk.get("reasons",[])
        if reasons:
            st.markdown("**Key Risk Drivers**")
            for reason in reasons: st.markdown(f"• {reason}")

    left,right=st.columns([1.25,1])
    with left:
        st.markdown('<div class="section-label">Recommended Actions</div>',unsafe_allow_html=True)
        actions=result.get("actions",[])
        if actions:
            for action in actions:
                st.markdown(f'<div class="action-card"><div class="action-title">{action["action"]}</div><div class="action-meta">Priority: <b>{action["priority"]}</b><br>{action["reason"]}</div></div>',unsafe_allow_html=True)
        else: st.info("No recommended actions were generated.")
    with right:
        st.markdown('<div class="section-label">Enterprise Knowledge</div>',unsafe_allow_html=True)
        sources=result.get("rag_sources",[])
        if sources:
            for source in sources: st.markdown(f'<div class="policy-card"><b>Source</b><br>{source}</div>',unsafe_allow_html=True)
        else: st.info("No enterprise policy source was retrieved.")
        rag_context=result.get("rag_context","")
        if rag_context:
            with st.expander("View Retrieved Policy Evidence"): st.write(rag_context)

    if st.session_state.uploaded_df is not None:
        df=st.session_state.uploaded_df.copy()
        numeric_columns=df.select_dtypes(include="number").columns.tolist()
        if numeric_columns:
            st.markdown('<div class="section-label">Data Trends</div>',unsafe_allow_html=True)
            chart_columns=numeric_columns[:3]
            tabs=st.tabs([c.replace("_"," ").title() for c in chart_columns])
            for tab,column in zip(tabs,chart_columns):
                with tab: st.line_chart(df[[column]])

    if "human_decision" in result:
        decision=result["human_decision"]
        status=decision.get("status","UNKNOWN"); message=decision.get("message","")
        st.markdown("---")
        st.markdown('<div class="section-label">Final Decision</div>',unsafe_allow_html=True)
        if status=="APPROVED": st.success(f"APPROVED — {message}")
        elif status=="REJECTED": st.error(f"REJECTED — {message}")
        elif status=="MODIFIED": st.warning(f"MODIFIED — {message}")
        else: st.info(f"{status} — {message}")

st.markdown('<div class="footer">Synapse-AI&nbsp;&nbsp;•&nbsp;&nbsp;Enterprise Agentic Decision Intelligence</div>',unsafe_allow_html=True)
