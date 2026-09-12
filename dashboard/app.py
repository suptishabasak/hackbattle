import streamlit as st

st.set_page_config(
    page_title="AI Test Selector",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI-Powered Risk-Aware Predictive Test Selection")

st.write(
    "Select the most relevant tests for a code change "
    "using dependency analysis, risk scoring, and historical data."
)

st.divider()

st.header("📌 Current Pull Request")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Changed Files")
    st.write("📄 src/payment.py")
    st.write("📄 src/checkout.py")
    st.write("📄 src/user.py")

with col2:
    st.subheader("Selected Tests")
    st.write("🧪 test_payment.py")
    st.write("🧪 test_checkout.py")
    st.write("🧪 test_user.py")

st.divider()

st.header("📊 Test Selection Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Affected Tests", 12)
col2.metric("Selected Tests", 6)
col3.metric("Tests Skipped", 6)
col4.metric("Time Saved", "48%")

st.divider()

st.header("🔍 Why were these tests selected?")

with st.expander("test_payment.py"):
    st.write("Selected because payment.py was modified.")
    st.write("Risk Score: 92%")
    st.write("Confidence: 88%")

with st.expander("test_checkout.py"):
    st.write("Selected because checkout.py depends on the changed code.")
    st.write("Risk Score: 84%")
    st.write("Confidence: 91%")

st.divider()

st.header("🕒 Historical Replay")

st.write(
    "Historical pull requests will be replayed here "
    "to measure test reduction and regression detection."
)