# agents/data_agent.py

import sys
import os
import re
import json
import requests

# Allows direct testing:
# python agents/data_agent.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm import logic_llm


# --------------------------------------------------
# JSON extraction from LLM
# --------------------------------------------------
def extract_json(text):
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    return None


# --------------------------------------------------
# Safe keyword matching
# --------------------------------------------------
def keyword_in_text(keyword, text):
    """
    Word-safe keyword matching.
    Prevents false positives like:
    'pet' matching 'petrol'
    """
    keyword = keyword.lower().strip()

    if not keyword:
        return False

    pattern = r"\b" + re.escape(keyword) + r"\b"
    return re.search(pattern, text) is not None


# --------------------------------------------------
# Fallback profile if LLM fails / rate-limits
# --------------------------------------------------
def build_fallback_profile(idea):
    idea_l = idea.lower()

    profile = {
        "category": idea_l,
        "direct_keywords": idea_l.split(),
        "indirect_keywords": [],
        "osm_tags": [
            {"key": "shop", "value": "yes"},
            {"key": "amenity", "value": "yes"}
        ]
    }

    # Pet-related businesses
    if "pet" in idea_l or "dog" in idea_l or "cat" in idea_l or "animal" in idea_l:
        profile["category"] = "pet business"
        profile["direct_keywords"] = [
            "pet cafe",
            "dog cafe",
            "cat cafe",
            "pet-friendly",
            "paw",
            "paws",
            "woof",
            "bark"
        ]
        profile["indirect_keywords"] = [
            "cafe",
            "restaurant",
            "pet shop",
            "veterinary",
            "animal shelter",
            "dog park"
        ]
        profile["osm_tags"] = [
            {"key": "amenity", "value": "cafe"},
            {"key": "amenity", "value": "restaurant"},
            {"key": "shop", "value": "pet"},
            {"key": "amenity", "value": "veterinary"},
            {"key": "leisure", "value": "dog_park"}
        ]

    # Cafe / food businesses
    elif "cafe" in idea_l or "coffee" in idea_l or "restaurant" in idea_l or "food" in idea_l:
        profile["category"] = "cafe"
        profile["direct_keywords"] = [
            "cafe",
            "coffee",
            "coffee shop"
        ]
        profile["indirect_keywords"] = [
            "restaurant",
            "bakery",
            "fast food",
            "tea"
        ]
        profile["osm_tags"] = [
            {"key": "amenity", "value": "cafe"},
            {"key": "amenity", "value": "restaurant"},
            {"key": "amenity", "value": "fast_food"},
            {"key": "shop", "value": "bakery"}
        ]

    # Florist
    elif "florist" in idea_l or "flower" in idea_l:
        profile["category"] = "florist"
        profile["direct_keywords"] = [
            "florist",
            "flower",
            "flowers"
        ]
        profile["indirect_keywords"] = [
            "gift",
            "decor",
            "event"
        ]
        profile["osm_tags"] = [
            {"key": "shop", "value": "florist"},
            {"key": "shop", "value": "gift"}
        ]

    # Gym / fitness
    elif "gym" in idea_l or "fitness" in idea_l:
        profile["category"] = "fitness"
        profile["direct_keywords"] = [
            "gym",
            "fitness",
            "crossfit"
        ]
        profile["indirect_keywords"] = [
            "sports",
            "yoga",
            "pilates"
        ]
        profile["osm_tags"] = [
            {"key": "leisure", "value": "fitness_centre"},
            {"key": "sport", "value": "fitness"}
        ]

    # Education
    elif "school" in idea_l or "tuition" in idea_l or "coaching" in idea_l or "education" in idea_l:
        profile["category"] = "education"
        profile["direct_keywords"] = [
            "school",
            "tuition",
            "coaching",
            "academy",
            "classes"
        ]
        profile["indirect_keywords"] = [
            "college",
            "library",
            "training"
        ]
        profile["osm_tags"] = [
            {"key": "amenity", "value": "school"},
            {"key": "amenity", "value": "college"},
            {"key": "amenity", "value": "library"}
        ]

    # Healthcare
    elif "clinic" in idea_l or "medical" in idea_l or "doctor" in idea_l or "pharmacy" in idea_l:
        profile["category"] = "healthcare"
        profile["direct_keywords"] = [
            "clinic",
            "doctor",
            "medical",
            "pharmacy"
        ]
        profile["indirect_keywords"] = [
            "hospital",
            "healthcare",
            "diagnostic"
        ]
        profile["osm_tags"] = [
            {"key": "amenity", "value": "clinic"},
            {"key": "amenity", "value": "hospital"},
            {"key": "amenity", "value": "pharmacy"},
            {"key": "healthcare", "value": "doctor"}
        ]

    # Grocery / retail
    elif "grocery" in idea_l or "store" in idea_l or "retail" in idea_l or "mart" in idea_l:
        profile["category"] = "retail"
        profile["direct_keywords"] = [
            "grocery",
            "store",
            "mart",
            "supermarket"
        ]
        profile["indirect_keywords"] = [
            "shop",
            "market",
            "convenience"
        ]
        profile["osm_tags"] = [
            {"key": "shop", "value": "supermarket"},
            {"key": "shop", "value": "convenience"},
            {"key": "shop", "value": "yes"}
        ]

    return profile


# --------------------------------------------------
# LLM creates generic search profile
# --------------------------------------------------
def get_search_profile(state):
    idea = state.get("idea", "")
    business_type = state.get("business_type", "")
    target_customers = state.get("target_customers", "")

    prompt = f"""
You are generating OpenStreetMap search metadata for competitor analysis.

Business idea: {idea}
Business type: {business_type}
Target customers: {target_customers}

Return ONLY valid JSON in this exact format:

{{
  "category": "short category",
  "direct_keywords": ["keyword1", "keyword2", "keyword3"],
  "indirect_keywords": ["keyword1", "keyword2", "keyword3"],
  "osm_tags": [
    {{"key": "amenity", "value": "cafe"}},
    {{"key": "shop", "value": "yes"}}
  ]
}}

Rules:
- direct_keywords must include broad category words AND niche words.
- Example: for "pet cafe", use ["pet cafe", "dog cafe", "cat cafe", "paw", "paws"].
- Example: for "organic grocery store", use ["grocery", "organic", "store", "market"].
- indirect_keywords should include related alternatives.
- Use common OpenStreetMap keys: amenity, shop, tourism, leisure, healthcare, office, craft.
- Use value "yes" for broad category search.
- Keywords must be lowercase.
- Do not include explanation.
"""

    try:
        response = logic_llm.invoke(prompt)
        parsed = extract_json(response.content)

        print("🧠 LLM SEARCH PROFILE:", parsed)

        if parsed:
            return parsed

    except Exception as e:
        print("⚠️ LLM profile generation failed:", e)

    return build_fallback_profile(idea)


# --------------------------------------------------
# Overpass query builder
# --------------------------------------------------
def build_tag_query(osm_tags, lat, lng, radius):
    parts = []

    for tag in osm_tags:
        key = tag.get("key")
        value = tag.get("value")

        if not key:
            continue

        if value in ["*", "yes", None, ""]:
            parts.append(f'node(around:{radius},{lat},{lng})["{key}"];')
            parts.append(f'way(around:{radius},{lat},{lng})["{key}"];')
        else:
            parts.append(f'node(around:{radius},{lat},{lng})["{key}"="{value}"];')
            parts.append(f'way(around:{radius},{lat},{lng})["{key}"="{value}"];')

    if not parts:
        parts = [
            f'node(around:{radius},{lat},{lng})["shop"];',
            f'way(around:{radius},{lat},{lng})["shop"];',
            f'node(around:{radius},{lat},{lng})["amenity"];',
            f'way(around:{radius},{lat},{lng})["amenity"];'
        ]

    return f"""
[out:json][timeout:40];
(
  {' '.join(parts)}
);
out center tags;
"""


def build_fallback_query(lat, lng, radius):
    return f"""
[out:json][timeout:40];
(
  node(around:{radius},{lat},{lng})["name"];
  way(around:{radius},{lat},{lng})["name"];
);
out center tags;
"""


# --------------------------------------------------
# Overpass request
# --------------------------------------------------
def fetch_overpass(query):
    urls = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://overpass.openstreetmap.ru/api/interpreter"
    ]

    headers = {
        "User-Agent": "AI-Startup-Simulator/1.0"
    }

    for url in urls:
        try:
            response = requests.post(
                url,
                data={"data": query},
                headers=headers,
                timeout=60
            )

            print("🌐 OVERPASS URL:", url)
            print("🌐 OVERPASS STATUS:", response.status_code)

            if response.status_code == 200:
                data = response.json()
                return data.get("elements", [])

            print("❌ OVERPASS ERROR:", response.text[:500])

        except Exception as e:
            print("❌ OVERPASS REQUEST FAILED:", e)

    return []


# --------------------------------------------------
# Normalize raw OSM place
# --------------------------------------------------
def normalize_place(place):
    tags = place.get("tags", {})
    name = tags.get("name")

    if not name:
        return None

    lat = place.get("lat")
    lng = place.get("lon")

    if lat is None or lng is None:
        center = place.get("center", {})
        lat = center.get("lat")
        lng = center.get("lon")

    place_type = (
        tags.get("amenity")
        or tags.get("shop")
        or tags.get("leisure")
        or tags.get("tourism")
        or tags.get("office")
        or tags.get("craft")
        or tags.get("healthcare")
        or "mapped_place"
    )

    return {
        "name": name,
        "type": place_type,
        "lat": lat,
        "lng": lng,
        "tags": tags
    }


# --------------------------------------------------
# Better competitor classification
# --------------------------------------------------
def classify_place(place, profile):
    name = place.get("name", "").lower()
    place_type = str(place.get("type", "")).lower()
    tags = place.get("tags", {})

    category = profile.get("category", "").lower()
    direct_keywords = profile.get("direct_keywords", [])
    indirect_keywords = profile.get("indirect_keywords", [])

    tag_text = " ".join(str(v).lower() for v in tags.values())
    text = " ".join([name, place_type, tag_text])

    # Direct match
    if any(keyword_in_text(keyword, text) for keyword in direct_keywords):
        return "direct"

    # Indirect match
    if any(keyword_in_text(keyword, text) for keyword in indirect_keywords):
        return "indirect"

    # Category-specific fallback logic

    if category == "pet business":
        if place_type in [
            "cafe",
            "restaurant",
            "fast_food",
            "bakery",
            "pet",
            "veterinary",
            "dog_park"
        ]:
            return "indirect"
        return "nearby"

    if category == "cafe":
        if place_type == "cafe":
            return "direct"
        if place_type in ["restaurant", "fast_food", "bakery"]:
            return "indirect"

    if category == "florist":
        if place_type == "florist":
            return "direct"
        if place_type in ["gift", "event", "decor"]:
            return "indirect"

    if category == "fitness":
        if place_type in ["fitness_centre", "fitness"]:
            return "direct"
        if place_type in ["sports_centre", "yoga", "pilates"]:
            return "indirect"

    if category == "education":
        if place_type in ["school", "college", "university", "library"]:
            return "indirect"

    if category == "healthcare":
        if place_type in ["clinic", "hospital", "doctors", "pharmacy"]:
            return "indirect"

    if category == "retail":
        if place_type in ["supermarket", "convenience", "retail", "mall"]:
            return "direct"
        if place_type not in ["mapped_place", "unknown"]:
            return "indirect"

    return "nearby"


def format_places(items):
    if not items:
        return "None found in mapped data."

    return "\n".join(
        [f"- {p['name']} ({p['type']})" for p in items[:10]]
    )


# --------------------------------------------------
# Main data agent
# --------------------------------------------------
def data_agent(state):
    print("🔥 DATA AGENT RUNNING")

    coords = state.get("coordinates")
    idea = state.get("idea", "")
    radius = state.get("radius", 5000)

    print("📍 COORDS RECEIVED:", coords)
    print("💡 IDEA:", idea)
    print("📏 RADIUS:", radius)

    if not coords:
        return {
            **state,
            "places": [],
            "competitor_profile": {},
            "analyses": {
                "main": "No coordinates found, so competitor analysis could not be performed.",
                "total_count": 0,
                "direct_count": 0,
                "indirect_count": 0,
                "competition_level": "Unknown"
            }
        }

    lat = coords.get("lat")
    lng = coords.get("lng")

    if lat is None or lng is None:
        return {
            **state,
            "places": [],
            "competitor_profile": {},
            "analyses": {
                "main": "Invalid coordinates, so competitor analysis could not be performed.",
                "total_count": 0,
                "direct_count": 0,
                "indirect_count": 0,
                "competition_level": "Unknown"
            }
        }

    profile = get_search_profile(state)

    query = build_tag_query(
        profile.get("osm_tags", []),
        lat,
        lng,
        radius
    )

    print("🔎 IDEA QUERY:", query)

    raw_places = fetch_overpass(query)
    print("📦 RAW IDEA RESULTS:", len(raw_places))

    if len(raw_places) < 3:
        print("⚠️ Too few idea-specific results. Running fallback query...")

        fallback_query = build_fallback_query(lat, lng, radius)
        print("🔎 FALLBACK QUERY:", fallback_query)

        raw_places = fetch_overpass(fallback_query)
        print("📦 RAW FALLBACK RESULTS:", len(raw_places))

    places = []
    seen = set()

    for raw in raw_places:
        normalized = normalize_place(raw)

        if not normalized:
            continue

        name_key = normalized["name"].lower().strip()

        if name_key in seen:
            continue

        seen.add(name_key)

        normalized["competition_category"] = classify_place(normalized, profile)
        places.append(normalized)

    direct = [p for p in places if p["competition_category"] == "direct"]
    indirect = [p for p in places if p["competition_category"] == "indirect"]
    nearby = [p for p in places if p["competition_category"] == "nearby"]

    total_count = len(places)
    direct_count = len(direct)
    indirect_count = len(indirect)

    if direct_count == 0 and indirect_count == 0:
        competition_level = "Unknown / Low mapped competition"
        insight = (
            "No clearly relevant competitors were found in mapped OpenStreetMap data. "
            "This does not guarantee there are no real competitors."
        )
    elif direct_count == 0 and indirect_count > 0:
        competition_level = "Moderate"
        insight = (
            "No direct niche competitors were found, but many related businesses exist nearby. "
            "This suggests demand exists, but differentiation will be important."
        )
    elif direct_count <= 3:
        competition_level = "Moderate"
        insight = (
            "Some direct competitors were found. Differentiation through positioning, "
            "experience, pricing, or niche targeting will matter."
        )
    else:
        competition_level = "High"
        insight = (
            "Multiple direct competitors were found. Strong positioning, branding, "
            "and execution will be important."
        )

    analysis = f"""
### 🏪 Competitor Analysis

**Business Idea:** {state.get("idea")}  
**Location:** {state.get("location")}  
**Detected Category:** {profile.get("category", "Unknown")}  
**Search Radius:** {radius / 1000:.1f} km  

---

### 📌 Competition Summary

- Total Nearby Mapped Places Found: **{total_count}**
- Direct Competitors: **{direct_count}**
- Indirect Competitors: **{indirect_count}**
- Competition Level: **{competition_level}**

---

### 🎯 Direct Competitors

{format_places(direct)}

---

### ⚠️ Indirect Competitors

{format_places(indirect)}

---

### 🧩 Other Nearby Mapped Businesses

{format_places(nearby)}

---

### 💡 Insight

{insight}
"""

    print("✅ NORMALIZED PLACES:", total_count)
    print("🎯 DIRECT:", direct_count)
    print("⚠️ INDIRECT:", indirect_count)

    return {
        **state,
        "places": places,
        "competitor_profile": profile,
        "analyses": {
            "main": analysis,
            "direct_count": direct_count,
            "indirect_count": indirect_count,
            "total_count": total_count,
            "competition_level": competition_level,
            "direct_competitors": direct,
            "indirect_competitors": indirect,
            "nearby_businesses": nearby
        }
    }


# --------------------------------------------------
# Direct test runner
# --------------------------------------------------
if __name__ == "__main__":
    test_state = {
        "idea": "pet cafe",
        "location": "Pune",
        "business_type": "Cafe",
        "target_customers": "pet owners",
        "coordinates": {
            "lat": 18.5204,
            "lng": 73.8567
        },
        "radius": 10000
    }

    result = data_agent(test_state)

    print("\n🎯 FINAL ANALYSIS")
    print(result.get("analyses", {}).get("main"))

    print("\n📍 PLACES FOUND:", len(result.get("places", [])))

    for place in result.get("places", [])[:20]:
        print(
            "-",
            place["name"],
            "|",
            place["type"],
            "|",
            place["competition_category"]
        )