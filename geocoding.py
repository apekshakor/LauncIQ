import requests

OPENCAGE_API_KEY = "b4ec0e784e704e748fd356bbd094de12"

def get_lat_lng(location):

    url = "https://api.opencagedata.com/geocode/v1/json"

    params = {
        "q": f"{location}, India",   # 🔥 improves match rate
        "key": OPENCAGE_API_KEY,
        "limit": 1,
        "no_annotations": 1
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        print("DEBUG OPENCAGE RESPONSE:", data)

        # ❌ CHECK API STATUS FIRST
        if data.get("status", {}).get("code") != 200:
            print("OpenCage Error:", data.get("status"))
            return None, None

        results = data.get("results", [])

        if not results:
            return None, None

        geometry = results[0].get("geometry", {})

        lat = geometry.get("lat")
        lng = geometry.get("lng")

        return lat, lng

    except Exception as e:
        print("Geocoding error:", e)
        return None, None