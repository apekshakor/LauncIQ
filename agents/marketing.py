from utils.llm import creative_llm


def marketing_agent(state):
    idea = state.get("idea", "")
    location = state.get("location", "")
    target_customers = state.get("target_customers", "")

    try:
        response = creative_llm.invoke(f"""
Create a marketing strategy for:

Business: {idea}
Location: {location}
Target customers: {target_customers}

Give:
- brand name ideas
- tagline ideas
- Instagram captions
- ad campaign idea
- image generation prompts
""")

        marketing = response.content

    except Exception as e:
        print("⚠️ marketing LLM failed:", e)

        marketing = f"""
### Marketing Strategy

**Brand Positioning:** A local, customer-friendly {idea} in {location}.

**Target Audience:** {target_customers}

**Campaign Idea:** Launch with a neighborhood-focused offer and promote through Instagram reels, Google Business Profile, WhatsApp groups, and local collaborations.

**Sample Tagline:** Built for {target_customers}, made for {location}.

**Image Prompt:** Create a modern promotional poster for a {idea} in {location}, targeting {target_customers}, clean design, premium but approachable.
"""

    return {
        **state,
        "marketing": marketing
    }