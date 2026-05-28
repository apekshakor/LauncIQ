def final_report(state):
    analyses = state.get("analyses", {})
    analysis_text = analyses.get("main", "No competitor analysis available.")

    coords = state.get("coordinates")

    if isinstance(coords, dict):
        coordinates_text = f"Latitude: {coords.get('lat')}, Longitude: {coords.get('lng')}"
    else:
        coordinates_text = "Coordinates not available"

    report = f"""
<html>
<head>
<style>
body {{
    font-family: Arial, sans-serif;
    padding: 40px;
    color: #222;
    line-height: 1.7;
}}

h1 {{
    color: #E85D26;
    text-align: center;
    border-bottom: 2px solid #ddd;
    padding-bottom: 10px;
}}

.section {{
    margin-top: 30px;
    padding: 20px;
    background: #f8f8f8;
    border-radius: 10px;
}}

h2 {{
    color: #1A1A2E;
}}
</style>
</head>

<body>

<h1>🚀 AI Startup Report</h1>

<div class="section">
<h2>📍 Location</h2>
<p><b>Location:</b> {state.get('location')}</p>
<p><b>Coordinates:</b> {coordinates_text}</p>
</div>

<div class="section">
<h2>💡 Refined Idea</h2>
<p>{state.get('refined_idea')}</p>
</div>

<div class="section">
<h2>🏪 Competitor Analysis</h2>
<p>{analysis_text}</p>
</div>

<div class="section">
<h2>⭐ Evaluation</h2>
<p>{state.get('justification')}</p>
</div>

<div class="section">
<h2>📈 Market Trends</h2>
<p>{state.get('trends')}</p>
</div>

<div class="section">
<h2>🚚 Supply Chain</h2>
<p>{state.get('supply_info')}</p>
</div>

<div class="section">
<h2>📣 Marketing Strategy</h2>
<p>{state.get('marketing')}</p>
</div>

</body>
</html>
"""

    return {
        **state,
        "report": report
    }