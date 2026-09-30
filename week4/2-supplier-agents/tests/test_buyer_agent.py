from agents.buyer_agent import check_risks


def test_check_risks_flags_quantity_violations():
    warnings = check_risks(
        "I recommend Kestrel Industrial because it is the best fit.",
        "The factory needs 700 units within 6 days.",
        "Required quantity: 700 units. Deadline: 6 days.",
    )

    assert any("capacity" in warning.lower() for warning in warnings)


def test_check_risks_flags_deadline_violations():
    warnings = check_risks(
        "I recommend NorthForge Components because it is the best fit.",
        "The factory needs 700 units within 6 days.",
        "Required quantity: 700 units. Deadline: 6 days.",
    )

    assert any("deadline" in warning.lower() for warning in warnings)


def test_check_risks_allows_valid_supplier():
    warnings = check_risks(
        "I recommend Verinox Supply because it meets the request.",
        "The factory needs 700 units within 6 days.",
        "Required quantity: 700 units. Deadline: 6 days.",
    )

    assert warnings == []
