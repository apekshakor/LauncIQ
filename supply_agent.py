from utils.llm import logic_llm


def supply_agent(state):
    idea = state.get("idea", "")
    location = state.get("location", "")

    try:
        response = logic_llm.invoke(f"""
For this business:

{idea}

Location: {location}

Suggest:
- raw material sources
- suppliers
- logistics issues
""")

        supply_info = response.content

    except Exception as e:
        print("⚠️ supply LLM failed:", e)

        supply_info = f"""
### Supply Chain

For **{idea}** in **{location}**, start with local wholesale markets, local vendors, online B2B suppliers, and nearby distributors.

Key logistics concerns:
- reliable supplier availability
- transport cost
- storage requirements
- quality consistency
- seasonal price changes
"""

    return {
        **state,
        "supply_info": supply_info
    }