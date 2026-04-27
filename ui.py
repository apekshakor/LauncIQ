import streamlit as st
import pandas as pd
from graph.workflow import build_graph


st.set_page_config(
    page_title="AI Startup Simulator",
    page_icon="🚀",
    layout="wide"
)

app = build_graph()


st.title("🚀 AI Startup Simulator")
st.caption("Personalized startup planning using location, competitors, trends, supply chain, and marketing agents.")


# -----------------------------
# Sidebar inputs
# -----------------------------
st.sidebar.header("📥 Startup Details")

idea = st.sidebar.text_input("💡 Startup Idea", value="pet cafe")
location = st.sidebar.text_input("📍 Location", value="Pune")

business_type = st.sidebar.selectbox(
    "🏢 Business Type",
    ["Cafe", "Retail", "Service", "Tech", "Food", "Education", "Healthcare", "Other"]
)

budget = st.sidebar.selectbox(
    "💰 Budget",
    [
        "Low (<₹50k)",
        "Medium (₹50k–₹5L)",
        "High (>₹5L)"
    ]
)

target_customers = st.sidebar.text_input(
    "🎯 Target Customers",
    value="pet owners and animal lovers"
)

experience = st.sidebar.selectbox(
    "🧠 Experience Level",
    ["Beginner", "Intermediate", "Expert"]
)

time_commitment = st.sidebar.selectbox(
    "⏳ Time Commitment",
    ["Part-time", "Full-time"]
)

radius_km = st.sidebar.slider(
    "📍 Competitor Search Radius (km)",
    min_value=1,
    max_value=15,
    value=5
)

run = st.sidebar.button("🚀 Generate Startup Plan", use_container_width=True)


# -----------------------------
# Helper functions
# -----------------------------
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


# -----------------------------
# Main execution
# -----------------------------
if run:
    if not idea.strip() or not location.strip():
        st.warning("Please enter both startup idea and location.")
        st.stop()

    user_input = {
        "idea": idea,
        "location": location,
        "business_type": business_type,
        "budget": budget,
        "target_customers": target_customers,
        "experience": experience,
        "time_commitment": time_commitment,
        "radius": radius_km * 1000
    }

    with st.spinner("🤖 AI agents are analyzing your startup idea..."):
        result = app.invoke(user_input)

    st.success("✅ Startup plan generated!")

    lat, lng = get_coordinates(result)
    analysis_text = get_analysis_text(result)
    score_text = get_score_text(result)
    competitors_df = get_competitor_dataframe(result)

    analyses = result.get("analyses", {})
    competitor_count = analyses.get("total_count", len(result.get("places", []))) if isinstance(analyses, dict) else len(result.get("places", []))
    competition_level = analyses.get("competition_level", "N/A") if isinstance(analyses, dict) else "N/A"

    # -----------------------------
    # Summary cards
    # -----------------------------
    st.subheader("📌 Startup Snapshot")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Location", result.get("location", "N/A"))

    with c2:
        st.metric("Coordinates", "Found" if lat and lng else "Not found")

    with c3:
        st.metric("Competitors", competitor_count)

    with c4:
        st.metric("Competition", competition_level)

    st.divider()

    # -----------------------------
    # Tabs
    # -----------------------------
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💡 Idea",
        "📍 Location",
        "🏪 Competitors",
        "📈 Market & Supply",
        "📢 Marketing",
        "📄 Report"
    ])

    with tab1:
        st.subheader("💡 Refined Idea")
        st.markdown(result.get("refined_idea", "No refined idea generated."))

        st.subheader("🏆 Best Business Plan")
        st.markdown(result.get("best_idea", "No best idea selected."))

        st.subheader("⭐ Evaluation")
        st.markdown(score_text)

    with tab2:
        st.subheader("📍 Location Insights")

        st.write(f"**Location:** {result.get('location', 'N/A')}")

        if lat and lng:
            st.write(f"**Latitude:** {lat}")
            st.write(f"**Longitude:** {lng}")

            location_df = pd.DataFrame({
                "lat": [lat],
                "lon": [lng]
            })

            st.map(location_df)
        else:
            st.warning("Coordinates not available. Check OpenCage API key or location input.")

    with tab3:
        st.subheader("🏪 Competitor Analysis")
        st.markdown(analysis_text)

        if not competitors_df.empty:
            st.subheader("📋 Nearby Mapped Businesses")
            st.dataframe(competitors_df, use_container_width=True)

            map_points = competitors_df.dropna(subset=["Latitude", "Longitude"]).copy()

            if not map_points.empty:
                map_points = map_points.rename(columns={
                    "Latitude": "lat",
                    "Longitude": "lon"
                })

                st.subheader("🗺️ Competitor Map")
                st.map(map_points[["lat", "lon"]])
        else:
            st.info("No nearby competitors found from OpenStreetMap mapped data.")

    with tab4:
        st.subheader("📈 Market Trends")
        st.markdown(result.get("trends", "No trend data generated."))

        st.subheader("🚚 Supply Chain")
        st.markdown(result.get("supply_info", "No supply chain data generated."))

    with tab5:
        st.subheader("📢 Marketing Strategy")
        st.markdown(result.get("marketing", "No marketing strategy generated."))

    with tab6:
        st.subheader("🧾 Final Report")

        report = result.get("report", "Report not generated.")

        st.markdown(report)

        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name="startup_report.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    st.info("Enter startup details in the sidebar and click **Generate Startup Plan**.")