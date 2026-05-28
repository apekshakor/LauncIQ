from typing import TypedDict, Optional, List, Dict, Any


class StartupState(TypedDict, total=False):

    # -------- USER INPUT --------
    idea: str
    location: str
    business_type: str
    budget: str
    target_customers: str
    experience: str
    time_commitment: str
    radius: int

    # -------- IDEA OUTPUTS --------
    refined_idea: Optional[str]
    variations: Optional[List[str]]
    best_idea: Optional[str]

    # -------- LOCATION + COMPETITION --------
    coordinates: Optional[Dict[str, float]]
    places: Optional[List[Dict[str, Any]]]
    competitor_profile: Optional[Dict[str, Any]]

    # -------- ANALYSIS OUTPUTS --------
    analyses: Optional[Dict[str, Any]]
    scores: Optional[Dict[str, Any]]
    justification: Optional[str]

    # -------- OTHER AGENTS --------
    trends: Optional[str]
    supply_info: Optional[str]
    marketing: Optional[str]
    report: Optional[str]