def final_report(state):
    analyses = state.get("analyses", {})
    analysis_text = analyses.get("main", "No competitor analysis available.")

    coords = state.get("coordinates")

    if isinstance(coords, dict):
        coordinates_text = f"Latitude: {coords.get('lat')}, Longitude: {coords.get('lng')}"
    else:
        coordinates_text = "Coordinates not available"

    report = f"""
# 🚀 AI Startup Report

---

## 📍 Location

**Location:** {state.get('location')}  
**Coordinates:** {coordinates_text}

---

## 💡 Refined Idea

{state.get('refined_idea')}

---

## 🏪 Competitor Analysis

{analysis_text}

---

## ⭐ Evaluation

{state.get('justification', 'No evaluation generated.')}

---

## 📈 Market Trends

{state.get('trends', 'No trends generated.')}

---

## 🚚 Supply Chain

{state.get('supply_info', 'No supply chain generated.')}

---

## 📢 Marketing Strategy

{state.get('marketing', 'No marketing generated.')}

---

## 🎯 Final Recommendation

Focus on clear differentiation, strong local positioning, customer experience, and controlled spending during the initial launch.
"""

    return {
        **state,
        "report": report
    }