import requests

def get_nearby_places(lat, lng):

    # 🛑 SAFETY CHECK
    if lat is None or lng is None:
        return []

    overpass_url = "http://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    (
      node["amenity"](around:1500,{lat},{lng});
      way["amenity"](around:1500,{lat},{lng});
      relation["amenity"](around:1500,{lat},{lng});

      node["shop"](around:1500,{lat},{lng});
      way["shop"](around:1500,{lat},{lng});

      node["office"](around:1500,{lat},{lng});
      way["office"](around:1500,{lat},{lng});
    );
    out center;
    """

    try:
        response = requests.get(
            overpass_url,
            params={"data": query},
            headers={"User-Agent": "startup-ai-simulator"},
            timeout=15
        )

        data = response.json()

    except Exception as e:
        print("Overpass error:", e)
        return []

    results = []

    for el in data.get("elements", []):
        tags = el.get("tags", {})

        # -------------------------
        # 🧠 SMART CLASSIFICATION
        # -------------------------
        if "amenity" in tags:
            category = "FOOD_SERVICE" if tags["amenity"] in [
                "restaurant", "cafe", "fast_food", "bar"
            ] else "AMENITY"
        elif "shop" in tags:
            category = "RETAIL"
        elif "office" in tags:
            category = "OFFICE"
        else:
            category = "OTHER"

        results.append({
            "name": tags.get("name", "Unknown"),
            "category": category,
            "raw_type": (
                tags.get("amenity")
                or tags.get("shop")
                or tags.get("office")
                or "unknown"
            ),
            "lat": el.get("lat") or el.get("center", {}).get("lat"),
            "lng": el.get("lon") or el.get("center", {}).get("lon")
        })

    return results