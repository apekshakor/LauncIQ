from langgraph.graph import StateGraph, END
from graph.state import StartupState

from agents.idea_refiner import idea_refiner
from agents.location_agent import location_agent
from agents.data_agent import data_agent
from agents.supply_agent import supply_agent
from agents.trends_agent import trends_agent
from agents.critic import critic_agent
from agents.marketing import marketing_agent
from agents.report import final_report


def build_graph():
    graph = StateGraph(StartupState)

    graph.add_node("refine", idea_refiner)
    graph.add_node("location", location_agent)
    graph.add_node("data", data_agent)
    graph.add_node("supply", supply_agent)
    graph.add_node("trends", trends_agent)
    graph.add_node("critic", critic_agent)
    graph.add_node("marketing", marketing_agent)
    graph.add_node("report", final_report)

    graph.set_entry_point("refine")

    graph.add_edge("refine", "location")
    graph.add_edge("location", "data")
    graph.add_edge("data", "supply")
    graph.add_edge("supply", "trends")
    graph.add_edge("trends", "critic")
    graph.add_edge("critic", "marketing")
    graph.add_edge("marketing", "report")
    graph.add_edge("report", END)

    return graph.compile()