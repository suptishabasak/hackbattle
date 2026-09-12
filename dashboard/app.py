import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ──────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Test Selector",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# GLOBAL STYLES
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 15% 0%, #161b2e 0%, #0b0e17 45%, #0a0c13 100%);
}

/* Hide default Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #11141f 0%, #0c0e17 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* Sidebar radio -> nav-like buttons */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 0.65rem 0.9rem;
    margin-bottom: 0.5rem;
    width: 100%;
    transition: all 0.15s ease;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(99,102,241,0.10);
    border-color: rgba(99,102,241,0.4);
}

/* Top banner / hero */
.hero {
    background: linear-gradient(135deg, rgba(99,102,241,0.14) 0%, rgba(236,72,153,0.08) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.75rem;
}
.hero h1 {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 0.4rem;
    background: linear-gradient(90deg, #ffffff, #c7d2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: rgba(255,255,255,0.65);
    font-size: 1.02rem;
    margin: 0;
}
.pr-pill {
    display: inline-block;
    background: rgba(99,102,241,0.18);
    border: 1px solid rgba(99,102,241,0.45);
    color: #c7d2fe;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    margin-bottom: 0.9rem;
}

/* Section headers */
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0.2rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Generic card */
.card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.85rem;
    transition: border-color 0.15s ease;
}
.card:hover {
    border-color: rgba(99,102,241,0.35);
}
.card-title {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: 0.95rem;
    color: #e2e8f0;
}
.card-sub {
    color: rgba(255,255,255,0.55);
    font-size: 0.85rem;
    margin-top: 0.35rem;
    line-height: 1.4;
}

/* File chips */
.file-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(99,102,241,0.10);
    border: 1px solid rgba(99,102,241,0.35);
    color: #a5b4fc;
    padding: 0.45rem 0.9rem;
    border-radius: 9px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.83rem;
    margin: 0 0.5rem 0.6rem 0;
}

/* Risk badges */
.badge {
    display: inline-block;
    padding: 0.22rem 0.75rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    margin-left: 0.6rem;
}
.badge-high   { background: rgba(239,68,68,0.15);  color:#f87171; border:1px solid rgba(239,68,68,0.4); }
.badge-medium { background: rgba(234,179,8,0.15);  color:#facc15; border:1px solid rgba(234,179,8,0.4); }
.badge-low    { background: rgba(34,197,94,0.15);  color:#4ade80; border:1px solid rgba(34,197,94,0.4); }

/* Confidence bar */
.bar-track {
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    height: 6px;
    width: 100%;
    margin-top: 0.5rem;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 999px;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem 1.1rem;
}
div[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.6); }

/* Divider */
hr { border-color: rgba(255,255,255,0.07) !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# DEMO DATA (swap these for real outputs from Person 1 / 2 / 3 modules)
# ──────────────────────────────────────────────────────────────────────────
CHANGED_FILES = ["src/payment.py", "src/checkout.py", "src/user.py"]

SELECTED_TESTS = [
    {
        "name": "test_payment.py",
        "risk": "High",
        "confidence": 88,
        "reason": "Directly modifies payment.py — core logic changed in this PR.",
        "dependency_path": "src/payment.py → PaymentProcessor → test_payment.py",
    },
    {
        "name": "test_checkout.py",
        "risk": "High",
        "confidence": 91,
        "reason": "checkout.py imports payment.py; change propagates through checkout flow.",
        "dependency_path": "src/payment.py → src/checkout.py → test_checkout.py",
    },
    {
        "name": "test_user.py",
        "risk": "Medium",
        "confidence": 74,
        "reason": "user.py touched indirectly via shared auth utils used at checkout.",
        "dependency_path": "src/user.py → auth_utils → test_user.py",
    },
    {
        "name": "test_order_history.py",
        "risk": "Low",
        "confidence": 55,
        "reason": "Historically flaky co-failure with checkout tests; included as a safety net.",
        "dependency_path": "historical co-failure signal (last 30 PRs)",
    },
]

BADGE_CLASS = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}
BAR_COLOR = {"High": "#f87171", "Medium": "#facc15", "Low": "#4ade80"}

# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR NAV
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 AI Test Selector")
    st.caption("Risk-aware predictive CI")
    st.write("")
    page = st.radio(
        "Navigate",
        ["📌 Current PR", "🧪 Test Selection", "🕒 Historical Replay"],
        label_visibility="collapsed",
    )
    st.write("")
    st.divider()
    st.caption("Connected modules")
    st.markdown("🟢 Dependency Graph — *live*")
    st.markdown("🟢 GitHub / PR Data — *live*")
    st.markdown("🟡 ML Risk Scoring — *demo data*")

# ──────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="pr-pill">PR #125 · main ← feature/payment-refactor</div>
    <h1>AI-Powered Risk-Aware Predictive Test Selection</h1>
    <p>Analyze code changes and intelligently select the most relevant tests using
    dependency analysis, risk scoring, and historical CI data.</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# SUMMARY METRICS (always visible)
# ──────────────────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Suite", "1,240 tests")
m2.metric("Selected", f"{len(SELECTED_TESTS)} tests", delta="-93% reduction")
m3.metric("Est. Time Saved", "18.4 min", delta="66% faster")
m4.metric("Avg. Confidence", "77%")

st.write("")

# ──────────────────────────────────────────────────────────────────────────
# PAGE: CURRENT PR
# ──────────────────────────────────────────────────────────────────────────
if page == "📌 Current PR":
    left, right = st.columns([1, 1.3], gap="large")

    with left:
        st.markdown('<div class="section-title">📂 Changed Files</div>', unsafe_allow_html=True)
        chips = "".join(f'<span class="file-chip">📄 {f}</span>' for f in CHANGED_FILES)
        st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="section-title">🔗 Impact Path</div>', unsafe_allow_html=True)
        for t in SELECTED_TESTS[:2]:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">{t['dependency_path']}</div>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-title">🧪 Selected Tests</div>', unsafe_allow_html=True)
        for t in SELECTED_TESTS:
            badge = f'<span class="badge {BADGE_CLASS[t["risk"]]}">{t["risk"]} Risk</span>'
            bar_color = BAR_COLOR[t["risk"]]
            st.markdown(f"""
            <div class="card">
                <span class="card-title">{t['name']}</span>{badge}
                <div class="card-sub">{t['reason']}</div>
                <div style="display:flex; justify-content:space-between; margin-top:0.6rem;">
                    <span style="font-size:0.78rem; color:rgba(255,255,255,0.5);">Confidence</span>
                    <span style="font-size:0.78rem; color:rgba(255,255,255,0.8); font-weight:600;">{t['confidence']}%</span>
                </div>
                <div class="bar-track">
                    <div class="bar-fill" style="width:{t['confidence']}%; background:{bar_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# PAGE: TEST SELECTION (explainability)
# ──────────────────────────────────────────────────────────────────────────
elif page == "🧪 Test Selection":
    st.markdown('<div class="section-title">🔍 Why was each test selected?</div>', unsafe_allow_html=True)
    st.caption("Every recommendation is backed by a dependency trace or a historical signal — nothing is a black box.")
    st.write("")

    for t in SELECTED_TESTS:
        badge = f'<span class="badge {BADGE_CLASS[t["risk"]]}">{t["risk"]} Risk</span>'
        with st.expander(f"{t['name']}  ·  {t['risk']} risk  ·  {t['confidence']}% confidence"):
            st.markdown(f"**Reason:** {t['reason']}")
            st.markdown(f"**Dependency trace:** `{t['dependency_path']}`")
            c1, c2 = st.columns(2)
            c1.metric("Risk Score", t["risk"])
            c2.metric("Confidence", f"{t['confidence']}%")
            if t["confidence"] < 65:
                st.warning("⚠️ Confidence below safety threshold — additional regression tests were auto-triggered.")

# ──────────────────────────────────────────────────────────────────────────
# PAGE: HISTORICAL REPLAY
# ──────────────────────────────────────────────────────────────────────────
elif page == "🕒 Historical Replay":
    st.markdown('<div class="section-title">🕒 Historical PR Replay</div>', unsafe_allow_html=True)
    st.caption("Replaying past PRs through the model to validate test reduction and regression recall.")
    st.write("")

    # Demo trend data — replace with Person 3's validation output
    df = pd.DataFrame({
        "PR": [f"#{n}" for n in range(110, 126)],
        "Tests Run (Full Suite)": [1240] * 16,
        "Tests Run (AI-Selected)": [180, 165, 210, 140, 190, 160, 205, 130,
                                     175, 150, 195, 120, 160, 140, 110, 87],
        "Regression Caught": [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    })

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["PR"], y=df["Tests Run (Full Suite)"],
        name="Full Suite", mode="lines",
        line=dict(color="rgba(255,255,255,0.25)", width=2, dash="dot"),
    ))
    fig.add_trace(go.Scatter(
        x=df["PR"], y=df["Tests Run (AI-Selected)"],
        name="AI-Selected", mode="lines+markers",
        line=dict(color="#818cf8", width=3),
        fill="tozeroy", fillcolor="rgba(129,140,248,0.12)",
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title=None, yaxis_title="Tests executed",
    )
    st.plotly_chart(fig, width="stretch")

    c1, c2, c3 = st.columns(3)
    c1.metric("Avg. Test Reduction", "87%")
    c2.metric("Regressions Caught", f"{df['Regression Caught'].sum()} / {len(df)} PRs")
    c3.metric("False Negatives", "0", delta="No missed regressions", delta_color="off")

    st.write("")
    st.markdown('<div class="section-title">📋 Recent Replay Log</div>', unsafe_allow_html=True)
    display_df = df.rename(columns={
        "Tests Run (Full Suite)": "Full Suite",
        "Tests Run (AI-Selected)": "AI-Selected",
        "Regression Caught": "Regression?",
    }).copy()
    display_df["Regression?"] = display_df["Regression?"].map({1: "🔴 Yes", 0: "🟢 No"})
    st.dataframe(display_df, width="stretch", hide_index=True)