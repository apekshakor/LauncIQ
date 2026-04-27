from graph.workflow import build_graph

app = build_graph()

idea = input("Enter your startup idea: ")
location = input("Enter the location: ")
business_type = input("Enter the business type: ")
budget = input("Enter your budget: ")
target_customers = input("Describe your target customers: ")
experience = input("Describe your experience in this domain: ")
time_commitment = input("How much time can you commit? ")

initial_state = {
    # raw inputs
    "idea": idea,
    "location": location,
    "business_type": business_type,
    "budget": budget,
    "target_customers": target_customers,
    "experience": experience,
    "time_commitment": time_commitment,

    # safe defaults (IMPORTANT)
    "best_idea": idea,
    "analyses": {},
    "scores": {},
    "justification": "Not generated yet",
    "marketing": "Not generated yet"
}

result = app.invoke(initial_state)

print(result.get("final_report", "No report generated"))