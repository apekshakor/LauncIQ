from langchain_core.prompts import ChatPromptTemplate
from utils.llm import creative_llm


def idea_refiner(state):
    idea = state.get("idea", "")
    location = state.get("location", "")
    budget = state.get("budget", "")
    target_customers = state.get("target_customers", "")

    prompt = ChatPromptTemplate.from_template(
        """
Refine this startup idea without changing the domain.

Idea: {idea}
Location: {location}
Budget: {budget}
Target Customers: {target_customers}

Provide:
- Problem
- Solution
- Target Users
- Unique Value
"""
    )

    try:
        response = creative_llm.invoke(
            prompt.format_messages(
                idea=idea,
                location=location,
                budget=budget,
                target_customers=target_customers
            )
        )

        refined = response.content

    except Exception as e:
        print("⚠️ idea_refiner LLM failed:", e)

        refined = f"""
### Refined Startup Idea

**Idea:** {idea}

**Location:** {location}

**Budget:** {budget}

**Target Customers:** {target_customers}

---

### Problem
Customers in {location} may have unmet needs related to {idea}.

---

### Solution
Build a localized {idea} business designed around the needs of {target_customers}.

---

### Target Users
{target_customers}

---

### Unique Value
Focus on convenience, local positioning, customer experience, and affordable execution.
"""

    return {
        **state,
        "refined_idea": refined,
        "best_idea": refined
    }