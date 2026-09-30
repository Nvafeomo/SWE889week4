"""Supplier Analysis Agent.

Goal: compare the available suppliers and recommend one.
Tool: the Supplier Information Tool.
It does not talk to the user. It is called by the Buyer Agent.
"""

from common import ask, banner
from tools.supplier_tool import supplier_information

ANALYSIS_PROMPT = """You are the Supplier Analysis Agent for a factory.

Factory request:
{request}

Criteria identified by the Buyer Agent:
{criteria}

Supplier information:
{suppliers}

Apply the following decision logic exactly:
1. Extract the required quantity and deadline from the request.
2. Reject any supplier whose capacity is below the required quantity.
3. Reject any supplier whose delivery time is greater than the deadline.
4. Among the remaining suppliers, compare price_per_unit (lower is better),
   delivery_days (shorter is better), reliability_score (higher is better),
   and capacity_units (higher is better but only after meeting the quantity limit).
5. Recommend the best feasible supplier; if none are feasible, state clearly that
   no supplier meets the factory's quantity and deadline constraints.
6. Return a short answer with: Selected supplier, Why it was chosen, and
   any trade-offs or warnings.
"""


def analyze(llm, request: str, criteria: str) -> str:
    """Reads the supplier catalogue through the tool, then recommends one."""
    banner("Supplier Analysis Agent  ->  Supplier Information Tool")
    suppliers = supplier_information.invoke({})
    print(suppliers)

    banner("Supplier Analysis Agent: recommending")
    recommendation = ask(
        llm,
        ANALYSIS_PROMPT.format(
            request=request, criteria=criteria, suppliers=suppliers
        ),
    )
    print(recommendation)
    return recommendation
