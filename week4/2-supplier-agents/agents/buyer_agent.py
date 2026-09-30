"""Buyer Agent.

Goal: receive the factory request, identify the decision criteria,
coordinate the workflow, and present the final answer to the user.
It is the only agent that talks to the user.
"""

import re

from agents.supplier_analysis_agent import analyze
from common import ask, banner
from tools.supplier_tool import find_supplier

CRITERIA_PROMPT = """You are the Buyer Agent for a factory.

Read the factory request below and extract the factory's hard requirements.
Return exactly five lines in this format:

Required quantity: <number> units
Deadline: <number> days
Decision priority: price_per_unit, delivery_days, reliability_score, capacity_units
Hard constraint: the selected supplier must meet both the quantity and the deadline.
Risk check: exclude any supplier that cannot satisfy the quantity or the deadline.

Factory request:
{request}
"""


def _extract_first_number(text: str, patterns: list[str]) -> int:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
    return 0


def _parse_request_details(request: str, criteria: str) -> tuple[int, int]:
    request_text = f"{request} {criteria}".lower()
    quantity = _extract_first_number(
        request_text,
        [
            r"required quantity:\s*(\d+)",
            r"quantity:\s*(\d+)",
            r"needs?\s*(\d+)\s*(?:units?|qty)",
            r"(\d+)\s*(?:units?|qty)\s*(?:required|needed)",
            r"(\d+)\s*(?:units?|qty)",
        ],
    )
    deadline = _extract_first_number(
        request_text,
        [
            r"deadline:\s*(\d+)",
            r"within\s*(\d+)\s*(?:days?|d)",
            r"in\s*(\d+)\s*(?:days?|d)",
            r"by\s*(\d+)\s*(?:days?|d)",
        ],
    )
    return quantity, deadline


def extract_criteria(llm, request: str) -> str:
    banner("Buyer Agent: identifying the decision criteria")
    criteria = ask(llm, CRITERIA_PROMPT.format(request=request))
    print(criteria)
    return criteria


def check_risks(recommendation: str, request: str, criteria: str) -> list[str]:
    """Flags a recommendation that cannot actually be met."""
    warnings: list[str] = []
    supplier = find_supplier(recommendation)
    quantity, deadline = _parse_request_details(request, criteria)

    if supplier is None:
        warnings.append(
            "The recommendation names a supplier that is not in the supplier catalogue."
        )
        return warnings

    if quantity and supplier.get("capacity_units", 0) < quantity:
        warnings.append(
            f"{supplier['name']} cannot meet the quantity requirement: "
            f"capacity {supplier['capacity_units']} units is below the requested {quantity} units."
        )

    if deadline and supplier.get("delivery_days", 0) > deadline:
        warnings.append(
            f"{supplier['name']} cannot meet the deadline: "
            f"delivery {supplier['delivery_days']} days exceeds the requested {deadline}-day limit."
        )

    if supplier.get("reliability_score", 1.0) < 0.80:
        warnings.append(
            f"{supplier['name']} reliability score {supplier['reliability_score']:.2f} is below the minimum acceptable threshold of 0.80."
        )

    return warnings


def format_response(recommendation: str, warnings: list[str]) -> str:
    """Builds the answer the user sees with a predictable structure."""
    supplier = find_supplier(recommendation)
    supplier_name = supplier["name"] if supplier else "Unclear"

    parts = [
        f"Selected supplier: {supplier_name}",
        "Decision summary:",
        recommendation.strip(),
    ]
    if warnings:
        parts.append("Warnings:")
        parts.extend(f"  - {warning}" for warning in warnings)
    return "\n".join(parts)


def handle_request(llm, request: str) -> str:
    """The coordination strategy: a sequential handoff, orchestrated here."""
    banner("Factory user  ->  Buyer Agent")
    print(request)

    criteria = extract_criteria(llm, request)
    recommendation = analyze(llm, request, criteria)
    warnings = check_risks(recommendation, request, criteria)

    banner("Buyer Agent  ->  Factory user")
    answer = format_response(recommendation, warnings)
    print(answer)
    return answer
