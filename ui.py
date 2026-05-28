import streamlit as st
import pandas as pd
from xhtml2pdf import pisa
from graph.workflow import build_graph

# ─────────────────────────────────────────
# Page config — must be FIRST st call
# ─────────────────────────────────────────
st.set_page_config(
    page_title="LaunchIQ · Startup Simulator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# Global CSS — light professional theme
# ─────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ──────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ── Root variables ────────────────────────────────── */
:root {
    --bg:        #F7F6F2;
    --surface:   #FFFFFF;
    --border:    #E8E4DC;
    --accent:    #1A1A2E;
    --accent2:   #E85D26;
    --accent3:   #2D6A4F;
    --muted:     #7A7570;
    --text:      #1C1A18;
    --tag-bg:    #FFF3ED;
    --tag-text:  #E85D26;
    --radius:    12px;
    --shadow:    0 2px 16px rgba(28,26,24,0.07);
}

/* ── Base ───────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

[data-testid="stMain"] {
    background-color: var(--bg) !important;
}

/* ── Sidebar ────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--accent) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: #F0EDE6 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #9B9490 !important;
}


/* ── Sidebar Inputs Full Blue Theme ───────────────── */

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] select {

    background-color: #262440 !important;
    color: #F0EDE6 !important;

    border: 1px solid #3A3860 !important;
    border-radius: 10px !important;

}

/* Selectbox container */
[data-testid="stSidebar"] div[data-baseweb="select"] > div {

    background-color: #262440 !important;
    border: 1px solid #3A3860 !important;
    border-radius: 10px !important;
    color: #F0EDE6 !important;

}

/* Selected text inside selectbox */
[data-testid="stSidebar"] div[data-baseweb="select"] span {

    color: #F0EDE6 !important;

}

/* Slider track background */
[data-testid="stSidebar"] .stSlider > div > div {

    color: #E85D26 !important;

}

/* Number inputs / text fields */
[data-testid="stSidebar"] .stTextInput div[data-baseweb="input"] {

    background-color: #262440 !important;
    border-radius: 10px !important;
    border: 1px solid #3A3860 !important;

}

/* Dropdown hover */
[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover {

    border-color: #E85D26 !important;

}

/* Sidebar button */
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #E85D26 0%, #F07A45 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.65rem 1.2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(232,93,38,0.35) !important;
}

[data-testid="stSidebar"] .stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(232,93,38,0.45) !important;
}

/* ── Headings ───────────────────────────────────────── */
h1, h2, h3, h4,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.02em !important;
}

/* ── Metric cards ───────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1.1rem 1.3rem !important;
    box-shadow: var(--shadow) !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.45rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
}

/* ── Tabs ───────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 2px solid var(--border) !important;
    gap: 0 !important;
}

[data-testid="stTabs"] button[role="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.6rem 1.2rem !important;
    margin-bottom: -2px !important;
    transition: color 0.2s !important;
    background: transparent !important;
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--accent2) !important;
    border-bottom-color: var(--accent2) !important;
    font-weight: 600 !important;
}

/* ── Dataframe ──────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow) !important;
}

/* ── Info / Warning / Success boxes ────────────────── */
[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border-left-width: 4px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Download button ────────────────────────────────── */
.stDownloadButton button {
    background-color: var(--accent) !important;
    color: #F0EDE6 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s ease !important;
}

.stDownloadButton button:hover {
    background-color: #2A2850 !important;
    transform: translateY(-1px) !important;
}

/* ── Divider ────────────────────────────────────────── */
hr {
    border-color: var(--border) !important;
}

/* ── Spinner ────────────────────────────────────────── */
[data-testid="stSpinner"] {
    color: var(--accent2) !important;
}

/* ── Content cards (markdown sections) ─────────────── */
.content-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem 1.8rem;
    box-shadow: var(--shadow);
    margin-bottom: 1.2rem;
}

/* ── Badge chip ─────────────────────────────────────── */
.badge {
    display: inline-block;
    background: var(--tag-bg);
    color: var(--tag-text);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 999px;
    border: 1px solid rgba(232,93,38,0.25);
    margin-bottom: 0.5rem;
}

/* ── Section header accent line ─────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
}

.section-header .line {
    flex: 1;
    height: 1px;
    background: var(--border);
}
            
             /* ── FIX STREAMLIT SIDEBAR COLLAPSE ICON ─────────── */

[data-testid="collapsedControl"] span {
    display: none !important;
}

[data-testid="collapsedControl"]::after {
    content: "⬅";
    font-size: 18px;
    color: white;
    font-weight: bold;
}

/* Style button */
[data-testid="collapsedControl"] {
    background-color: #1A1A2E !important;
    border: 1px solid #3A3860 !important;
    border-radius: 10px !important;
    width: 38px !important;
    height: 38px !important;
}

/* Hover effect */
[data-testid="collapsedControl"]:hover {
    border-color: #E85D26 !important;
    background-color: #262440 !important;
}
</style>
""", unsafe_allow_html=True)

app = build_graph()

# ─────────────────────────────────────────
# Hero header
# ─────────────────────────────────────────
st.markdown("""
<div style="padding: 2.2rem 0 1.4rem 0;">
    <span class="badge">AI-Powered</span>
    <h1 style="font-size:2.6rem; font-weight:800; margin:0.3rem 0 0.5rem 0; line-height:1.15;">
        LaunchIQ
        <span style="color:#E85D26;">·</span>
        Startup Simulator
    </h1>
    <p style="color:#7A7570; font-size:1.05rem; max-width:640px; margin:0; font-weight:300;">
        Hyper-personalised startup intelligence — location, competitors, trends,
        supply chain and marketing, all in one plan.
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.4rem 0 1rem 0;">
        <div style="font-family:'Syne',sans-serif; font-size:1.25rem; font-weight:700;
                    color:#F0EDE6; letter-spacing:-0.01em;">
            ⚡ Startup Details
        </div>
        <div style="font-size:0.78rem; color:#6B6880; margin-top:4px;">
            Fill in the fields below to generate your plan.
        </div>
    </div>
    <hr style="border-color:#2E2C4A; margin:0 0 1rem 0;">
    """, unsafe_allow_html=True)

    idea = st.text_input("Startup Idea", value="pet cafe")
    location = st.text_input("Location", value="Pune")

    business_type = st.selectbox(
        "Business Type",
        ["Cafe", "Retail", "Service", "Tech", "Food", "Education", "Healthcare", "Other"]
    )

    budget = st.selectbox(
        "Budget",
        ["Low (<₹50k)", "Medium (₹50k–₹5L)", "High (>₹5L)"]
    )

    target_customers = st.text_input("Target Customers", value="pet owners and animal lovers")

    experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Expert"])
    time_commitment = st.selectbox("Time Commitment", ["Part-time", "Full-time"])

    radius_km = st.slider("Competitor Radius (km)", min_value=1, max_value=15, value=5)

    st.markdown("<div style='margin-top:1.4rem;'></div>", unsafe_allow_html=True)
    run = st.button("🚀 Generate Startup Plan", use_container_width=True)

# ─────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────
def get_analysis_text(result):
    analyses = result.get("analyses")
    if isinstance(analyses, dict):
        return analyses.get("main", "No analysis available.")
    if isinstance(analyses, str):
        return analyses
    return "No analysis available."

def get_coordinates(result):
    coords = result.get("coordinates")
    if isinstance(coords, dict):
        return coords.get("lat"), coords.get("lng")
    return None, None

def get_score_text(result):
    scores = result.get("scores")
    if isinstance(scores, dict):
        return scores.get("main", "No evaluation available.")
    if isinstance(scores, str):
        return scores
    return "No evaluation available."

def get_competitor_dataframe(result):
    places = result.get("places", [])
    rows = []
    for place in places:
        if isinstance(place, dict):
            rows.append({
                "Name": place.get("name", "Unknown"),
                "Type": place.get("type", "unknown"),
                "Category": place.get("competition_category", "unknown"),
                "Latitude": place.get("lat"),
                "Longitude": place.get("lng"),
            })
    return pd.DataFrame(rows)

def render_section(icon, title, content, badge_label=None):
    """Render a styled content card."""
    badge_html = f'<span class="badge">{badge_label}</span><br>' if badge_label else ""
    st.markdown(f"""
    <div class="content-card">
        {badge_html}
        <div class="section-header">
            <span style="font-family:'Syne',sans-serif; font-size:1.05rem; font-weight:700;">
                {icon} {title}
            </span>
            <div class="line"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(content)

# ─────────────────────────────────────────
# Main execution
# ─────────────────────────────────────────
if run:
    if not idea.strip() or not location.strip():
        st.warning("⚠️  Please enter both a startup idea and a location.")
        st.stop()

    user_input = {
        "idea": idea,
        "location": location,
        "business_type": business_type,
        "budget": budget,
        "target_customers": target_customers,
        "experience": experience,
        "time_commitment": time_commitment,
        "radius": radius_km * 1000,
    }

    with st.spinner("🔍 AI agents are analysing your startup idea…"):
        result = app.invoke(user_input)

    st.success("✅  Startup plan generated!")

    lat, lng           = get_coordinates(result)
    analysis_text      = get_analysis_text(result)
    score_text         = get_score_text(result)
    competitors_df     = get_competitor_dataframe(result)
    analyses           = result.get("analyses", {})
    competitor_count   = (
        analyses.get("total_count", len(result.get("places", [])))
        if isinstance(analyses, dict)
        else len(result.get("places", []))
    )
    competition_level  = analyses.get("competition_level", "N/A") if isinstance(analyses, dict) else "N/A"

    # ── Snapshot metrics ──────────────────────────────
    st.markdown("<div style='margin: 0.5rem 0 1rem 0;'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📍 Location",      result.get("location", "N/A"))
    with c2:
        st.metric("🗺️ Coordinates",  "Found ✓" if lat and lng else "Not found")
    with c3:
        st.metric("🏪 Competitors",   competitor_count)
    with c4:
        st.metric("📊 Competition",   competition_level)

    st.markdown("<hr style='margin: 1.6rem 0;'>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💡 Idea",
        "📍 Location",
        "🏪 Competitors",
        "📈 Market & Supply",
        "📣 Marketing",
        "📄 Report",
    ])

    # ── Tab 1: Idea ───────────────────────────────────
    with tab1:
        col_a, col_b = st.columns([1, 1], gap="large")

        with col_a:
            st.markdown("""
            <div class="content-card">
                <div class="section-header">
                    <span style="font-family:'Syne',sans-serif; font-weight:700;">
                        ✨ Refined Idea
                    </span>
                    <div class="line"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(result.get("refined_idea", "No refined idea generated."))

        with col_b:
            st.markdown("""
            <div class="content-card">
                <div class="section-header">
                    <span style="font-family:'Syne',sans-serif; font-weight:700;">
                        🏆 Best Business Plan
                    </span>
                    <div class="line"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(result.get("best_idea", "No best idea selected."))

        st.markdown("""
        <div class="content-card" style="margin-top:1rem;">
            <div class="section-header">
                <span style="font-family:'Syne',sans-serif; font-weight:700;">
                    🎯 Evaluation Score
                </span>
                <div class="line"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(score_text)

    # ── Tab 2: Location ───────────────────────────────
    with tab2:
        st.markdown("""
        <div class="content-card">
            <div class="section-header">
                <span style="font-family:'Syne',sans-serif; font-weight:700;">
                    📍 Location Insights
                </span>
                <div class="line"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        lc1, lc2, lc3 = st.columns(3)
        with lc1:
            st.metric("City / Area", result.get("location", "N/A"))
        with lc2:
            st.metric("Latitude",  f"{lat:.4f}" if lat else "—")
        with lc3:
            st.metric("Longitude", f"{lng:.4f}" if lng else "—")

        if lat and lng:
            st.map(pd.DataFrame({"lat": [lat], "lon": [lng]}))
        else:
            st.warning("Coordinates not available. Check OpenCage API key or location input.")

    # ── Tab 3: Competitors ────────────────────────────
    with tab3:
        st.markdown("""
        <div class="content-card">
            <div class="section-header">
                <span style="font-family:'Syne',sans-serif; font-weight:700;">
                    🔍 Competitor Analysis
                </span>
                <div class="line"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(analysis_text)

        if not competitors_df.empty:
            st.markdown("#### 📋 Nearby Businesses")
            st.dataframe(competitors_df, use_container_width=True, hide_index=True)

            map_points = competitors_df.dropna(subset=["Latitude", "Longitude"]).copy()
            if not map_points.empty:
                map_points = map_points.rename(columns={"Latitude": "lat", "Longitude": "lon"})
                st.markdown("#### 🗺️ Competitor Map")
                st.map(map_points[["lat", "lon"]])
        else:
            st.info("No nearby competitors found from OpenStreetMap data.")

    # ── Tab 4: Market & Supply ────────────────────────
    with tab4:
        mc1, mc2 = st.columns([1, 1], gap="large")

        with mc1:
            st.markdown("""
            <div class="content-card">
                <div class="section-header">
                    <span style="font-family:'Syne',sans-serif; font-weight:700;">
                        📈 Market Trends
                    </span>
                    <div class="line"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(result.get("trends", "No trend data generated."))

        with mc2:
            st.markdown("""
            <div class="content-card">
                <div class="section-header">
                    <span style="font-family:'Syne',sans-serif; font-weight:700;">
                        🏭 Supply Chain
                    </span>
                    <div class="line"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(result.get("supply_info", "No supply chain data generated."))

    # ── Tab 5: Marketing ──────────────────────────────
    with tab5:
        st.markdown("""
        <div class="content-card">
            <div class="section-header">
                <span style="font-family:'Syne',sans-serif; font-weight:700;">
                    📣 Marketing Strategy
                </span>
                <div class="line"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(result.get("marketing", "No marketing strategy generated."))

    # ── Tab 6: Report ─────────────────────────────────
    with tab6:
        report = result.get("report", "Report not generated.")

        st.markdown("""
        <div class="content-card">
            <div class="section-header">
                <span style="font-family:'Syne',sans-serif; font-weight:700;">
                    📄 Final Startup Report
                </span>
                <div class="line"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(report, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
        pdf_file = "startup_report.pdf"

        # Create PDF file from the report HTML/text
        with open(pdf_file, "w+b") as result_file:
            pisa_status = pisa.CreatePDF(
                report,
                dest=result_file
            )

        # Provide download button for the generated PDF
        with open(pdf_file, "rb") as pdf:
            st.download_button(
                label="📥 Download Professional PDF Report",
                data=pdf,
                file_name="startup_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
 
else:
    # ── Empty state ───────────────────────────────────
    st.markdown("""
    <div style="
        margin-top: 3rem;
        text-align: center;
        padding: 4rem 2rem;
        background: white;
        border: 1.5px dashed #D9D4CC;
        border-radius: 16px;
        max-width: 640px;
        margin-left: auto;
        margin-right: auto;
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
        <h3 style="font-family:'Syne',sans-serif; font-size:1.4rem;
                   font-weight:700; color:#1C1A18; margin:0 0 0.6rem;">
            Ready to build something great?
        </h3>
        <p style="color:#7A7570; font-size:0.95rem; max-width:400px;
                  margin:0 auto; line-height:1.6;">
            Fill in your startup details in the sidebar and click
            <strong style="color:#E85D26;">Generate Startup Plan</strong>
            to get your personalised AI-powered business plan.
        </p>
    </div>
    """, unsafe_allow_html=True)