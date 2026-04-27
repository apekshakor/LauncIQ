from utils.llm import logic_llm


def trends_agent(state):
    idea = state.get("idea", "")
    location = state.get("location", "")

    try:
        response = logic_llm.invoke(f"""
Analyze current market trends for:

Business: {idea}
Location: {location}

Include:
- demand trend
- customer behavior
- pricing trends
""")

        trends = response.content

    except Exception as e:
        print("⚠️ trends LLM failed:", e)

        trends = f"""
### Market Trends

- Demand for localized businesses like **{idea}** depends strongly on customer convenience and neighborhood density.
- Customers in {location} may prefer businesses with strong online visibility, reviews, and clear differentiation.
- Pricing should be tested locally using competitor observation and early customer feedback.
"""

    return {
        **state,
        "trends": trends
    }