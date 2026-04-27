def analyze_variations(state):
    places = state.get("places", [])

    names = []
    for p in places[:5]:
        if "tags" in p and "name" in p["tags"]:
            names.append(p["tags"]["name"])

    competitor_count = len(places)

    analysis = f"""
Competitors Found: {competitor_count}

Top Competitors:
{', '.join(names) if names else "Not enough data"}
"""

    return {
        **state,
        "analyses": {"main": analysis}
    }