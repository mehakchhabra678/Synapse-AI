def generate_actions(decision: dict) -> list:
    """
    Generate business actions dynamically based on the
    risk assessment produced by the decision engine.
    """

    actions = []

    risk_level = decision.get("risk_level", "LOW")
    reasons = decision.get("reasons", [])

    # --------------------------------------------------------
    # HIGH RISK
    # --------------------------------------------------------

    if risk_level == "HIGH":

        for reason in reasons:

            if "operational" in reason.lower():
                actions.append({
                    "action": "Investigate operational performance",
                    "reason": reason,
                    "priority": "HIGH"
                })

            elif "cost" in reason.lower():
                actions.append({
                    "action": "Review cost and expense drivers",
                    "reason": reason,
                    "priority": "HIGH"
                })

            elif "negative" in reason.lower():
                actions.append({
                    "action": "Investigate negative business trends",
                    "reason": reason,
                    "priority": "HIGH"
                })

            elif "people" in reason.lower() or "customer" in reason.lower():
                actions.append({
                    "action": "Review customer and workforce indicators",
                    "reason": reason,
                    "priority": "HIGH"
                })

        # Fallback
        if not actions:
            actions.append({
                "action": "Conduct immediate business performance review",
                "reason": "Multiple risk indicators were detected.",
                "priority": "HIGH"
            })

    # --------------------------------------------------------
    # MEDIUM RISK
    # --------------------------------------------------------

    elif risk_level == "MEDIUM":

        for reason in reasons:

            if "operational" in reason.lower():
                actions.append({
                    "action": "Review operational performance",
                    "reason": reason,
                    "priority": "MEDIUM"
                })

            elif "cost" in reason.lower():
                actions.append({
                    "action": "Monitor cost and expense trends",
                    "reason": reason,
                    "priority": "MEDIUM"
                })

            elif "negative" in reason.lower():
                actions.append({
                    "action": "Investigate negative performance indicators",
                    "reason": reason,
                    "priority": "MEDIUM"
                })

            elif "people" in reason.lower() or "customer" in reason.lower():
                actions.append({
                    "action": "Review customer or workforce indicators",
                    "reason": reason,
                    "priority": "MEDIUM"
                })

        if not actions:
            actions.append({
                "action": "Conduct management review",
                "reason": "Business indicators require monitoring.",
                "priority": "MEDIUM"
            })

    # --------------------------------------------------------
    # LOW RISK
    # --------------------------------------------------------

    else:

        actions.append({
            "action": "Continue monitoring business performance",
            "reason": "Current indicators do not show significant risk.",
            "priority": "LOW"
        })

    return actions