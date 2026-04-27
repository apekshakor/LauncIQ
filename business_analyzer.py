def analyze_business(places, idea):

    total_places = len(places)

    ratings = []
    for p in places:
        if "rating" in p:
            ratings.append(p["rating"])

    avg_rating = sum(ratings)/len(ratings) if ratings else 0

    # simple scoring logic
    competition_score = min(total_places / 20, 1)  # normalize

    success_score = (1 - competition_score) * 0.6 + (avg_rating / 5) * 0.4

    if success_score > 0.7:
        verdict = "HIGH SUCCESS POTENTIAL"
    elif success_score > 0.4:
        verdict = "MODERATE RISK"
    else:
        verdict = "HIGH COMPETITION / RISKY"

    return {
        "total_competitors": total_places,
        "avg_rating": round(avg_rating, 2),
        "success_score": round(success_score, 2),
        "verdict": verdict
    }