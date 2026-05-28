from utils.llm import logic_llm


def critic_agent(state):
    analyses = state.get("analyses", {})
    analysis_text = analyses.get("main", "")

    try:
        response = logic_llm.invoke(f"""
Evaluate this business idea using the competitor analysis below:

{analysis_text}

Also consider:
- Budget: {state.get("budget")}
- Target customers: {state.get("target_customers")}
- Experience level: {state.get("experience")}
- Time commitment: {state.get("time_commitment")}

Give:
- Score out of 10
- Short justification
- Key risk
- Key opportunity
""")

        evaluation = response.content

    except Exception as e:
        print("⚠️ critic LLM failed:", e)

        direct_count = analyses.get("direct_count", 0)
        indirect_count = analyses.get("indirect_count", 0)
        competition_level = analyses.get("competition_level", "Unknown")

        if direct_count == 0 and indirect_count > 0:
            score = 7
        elif direct_count <= 3:
            score = 7
        else:
            score = 5

        evaluation = f"""
### Score: {score}/10

### Justification
The business has **{competition_level}** competition based on mapped data, with **{direct_count} direct competitors** and **{indirect_count} indirect competitors**.

### Key Risk
Real-world competitor data may be incomplete because OpenStreetMap does not capture every business.

### Key Opportunity
Strong positioning, local branding, and differentiated customer experience can improve success chances.
"""

    return {
        **state,
        "scores": {
            "main": evaluation
        },
        "best_idea": state.get("refined_idea"),
        "justification": evaluation
    }