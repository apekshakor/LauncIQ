import os
import requests
from dotenv import load_dotenv

load_dotenv()


def location_agent(state):
    location = state.get("location", "").strip()

    if not location:
        print("❌ No location provided")
        return {
            **state,
            "coordinates": None
        }

    api_key = os.getenv("OPENCAGE_API_KEY")

    print("📍 Location input:", location)
    print("🔑 OPENCAGE API KEY:", api_key)

    if not api_key:
        print("❌ OpenCage API key missing")
        return {
            **state,
            "coordinates": None
        }

    url = "https://api.opencagedata.com/geocode/v1/json"

    params = {
        "q": location + ", India",
        "key": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        data = response.json()

        print("🌐 OpenCage response:", data)

        status = data.get("status", {})
        if status.get("code") != 200:
            print("❌ OpenCage API error:", status.get("message"))
            return {
                **state,
                "coordinates": None
            }

        results = data.get("results", [])

        if not results:
            print("❌ No coordinates found")
            return {
                **state,
                "coordinates": None
            }

        geometry = results[0]["geometry"]

        lat = geometry["lat"]
        lng = geometry["lng"]

        print("✅ Coordinates found:", lat, lng)

        return {
            **state,
            "coordinates": {
                "lat": lat,
                "lng": lng
            }
        }

    except Exception as e:
        print("❌ Location agent error:", e)

        return {
            **state,
            "coordinates": None
        }


if __name__ == "__main__":
    test_state = {
        "location": "Pune"
    }

    result = location_agent(test_state)

    print("\n🎯 FINAL OUTPUT:")
    print(result)