
import streamlit as st
import requests

st.set_page_config(page_title="AI Bug Busters", layout="wide")

# ✅ ✅ PREMIUM COLORFUL CSS
st.markdown("""
<style>

.main-title {
    font-size: 34px;
    font-weight: 800;
    background: linear-gradient(90deg, #6366f1, #22c55e, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.card {
    padding: 18px;
    border-radius: 16px;
    background: linear-gradient(135deg, #ffffff, #f8fafc);
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    margin-bottom: 16px;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #334155;
}

.badge-high {
    padding: 5px 10px;
    border-radius: 8px;
    background-color: #dcfce7;
    color: #15803d;
    font-weight: 600;
}

.badge-medium {
    padding: 5px 10px;
    border-radius: 8px;
    background-color: #fef3c7;
    color: #92400e;
    font-weight: 600;
}

.badge-low {
    padding: 5px 10px;
    border-radius: 8px;
    background-color: #fee2e2;
    color: #991b1b;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ✅ HEADER
st.markdown('<div class="main-title">🚀 AI Bug Busters</div>', unsafe_allow_html=True)
st.caption("AI-Powered Incident Decision Intelligence")

# ✅ INPUT
issue_input = st.text_input("Enter Incident Description")

if st.button("🔍 Analyze Incident"):

    if not issue_input.strip():
        st.warning("⚠ Please enter an issue")
        st.stop()

    data = requests.get(
        f"http://127.0.0.1:8000/analyze?issue={issue_input}"
    ).json()

    # ✅ HOW SYSTEM WORKS
    with st.expander("🔍 How the system works"):
        st.write("""
- Uses AI embeddings to understand meaning  
- Matches with historical incidents  
- Calculates similarity (confidence)  
- Suggests fix + explanation + risk  
""")

    if "error" in data:
        st.error(data["error"])
        st.stop()

    # ✅ FALLBACK
    if "best_practices" in data:
        st.warning(data["message"])

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown('### 📊 Confidence ℹ️')
        st.caption("Similarity between input and known incidents")
        st.progress(float(data.get("confidence", 0)))

        st.markdown('### 📖 Explanation ℹ️')
        st.caption("Why system could not find a strong match")
        st.info(data["explanation"])

        st.markdown('### 💡 Best Practices ℹ️')
        st.caption("General troubleshooting steps")
        for tip in data["best_practices"]:
            st.write(f"✅ {tip}")

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        confidence = float(data["confidence"])
        risk = data.get("risk", "low")
        level = data.get("level")

        # ✅ EXECUTIVE SUMMARY
        st.markdown('<div class="card">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("✅ Issue Match", data["matched_issue"])
            st.caption("Closest incident identified using AI similarity")

        with col2:
            st.metric("📊 Confidence", f"{round(confidence*100,2)}%")
            st.caption("Indicates how closely your issue matches known cases")

        with col3:
            st.metric("⚠ Risk", risk.upper())
            st.caption("Impact level of applying this fix")

        st.markdown('</div>', unsafe_allow_html=True)

        # ✅ TABS
        tab1, tab2, tab3 = st.tabs(["🔍 Details", "📖 Explanation", "⚠ Impact"])

        # ✅ DETAILS
        with tab1:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.markdown('### 🧠 AI Match ℹ️')
                st.caption("Matched using semantic similarity (embedding comparison)")

                st.write("✅ Matched Issue:", data["matched_issue"])
                st.write("🔍 Root Cause:", data.get("root_cause"))

                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.markdown('### 🛠 Suggested Fix ℹ️')
                st.caption("Resolution derived from similar historical incidents")

                st.success(data["suggested_fix"])

                st.markdown('### 📊 Confidence ℹ️')
                st.caption("Higher score means higher similarity")

                st.progress(confidence)

                if confidence > 0.8:
                    st.markdown('<span class="badge-high">High Confidence</span>', unsafe_allow_html=True)
                elif confidence > 0.5:
                    st.markdown('<span class="badge-medium">Medium Confidence</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-low">Low Confidence</span>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

            # ✅ RISK
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown('### ⚠ Risk ℹ️')
            st.caption("Indicates potential impact of applying this fix")

            if risk == "low":
                st.success("✅ Safe to apply")

            elif risk == "medium":
                st.warning("⚠ Validate before applying")

            elif risk == "high":
                st.error("🚨 Requires careful review")

            st.markdown('</div>', unsafe_allow_html=True)

        # ✅ EXPLANATION
        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown('### 📖 Explanation ℹ️')
            st.caption("AI-generated reasoning behind recommendation")

            st.info(data["explanation"])

            st.markdown('</div>', unsafe_allow_html=True)

        # ✅ IMPACT
        with tab3:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown('### ⚠ Impact ℹ️')
            st.caption("Potential consequences if issue is not resolved")

            if "disk" in data["matched_issue"].lower():
                st.write("- Storage exhaustion")
                st.write("- Application crash")
                st.write("- Logging failure")

            elif "cpu" in data["matched_issue"].lower():
                st.write("- Slow performance")
                st.write("- Latency increase")
                st.write("- Instability")

            else:
                st.write("- Issue persists")
                st.write("- Performance degradation")
                st.write("- Service impact")

            st.markdown('</div>', unsafe_allow_html=True)

        # ✅ FINAL RECOMMENDATION
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown('### 💡 Recommendation ℹ️')
        st.caption("Based on combined confidence and risk evaluation")

        if level == "HIGH_CONFIDENCE":
            st.success("✅ Strong recommendation")

        elif level == "MEDIUM_CONFIDENCE":
            st.warning("⚠ Validate before applying")

        else:
            st.info("💡 Investigate further")

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("AI Bug Busters | Enterprise AI Decision Intelligence 🚀 for CTS ING Hackathon 2026")