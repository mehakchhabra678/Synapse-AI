def make_decision(insights: list) -> dict:
    """
    Generate a risk decision from the insights produced by the
    dataset-driven insight engine.

    The score is based on the type of business signals detected
    rather than hardcoded dataset column names.
    """

    risk_score = 0
    reasons = []

    for insight in insights:

        text = insight.lower()

        # ----------------------------------------------------
        # NEGATIVE / OPERATIONAL SIGNALS
        # ----------------------------------------------------

        if any(word in text for word in [
            "declining",
            "decrease",
            "decreased",
            "decline",
            "drop",
            "falling",
            "deterioration"
        ]):

            risk_score += 25

            reasons.append(
                "Negative performance trend detected"
            )

        # ----------------------------------------------------
        # COST / EXPENSE SIGNALS
        # ----------------------------------------------------

        if any(word in text for word in [
            "cost",
            "expense",
            "expenses"
        ]):

            risk_score += 20

            reasons.append(
                "Cost or expense variation detected"
            )

        # ----------------------------------------------------
        # DELAY / SERVICE SIGNALS
        # ----------------------------------------------------

        if any(word in text for word in [
            "late",
            "delay",
            "delayed",
            "absenteeism"
        ]):

            risk_score += 25

            reasons.append(
                "Operational or service issue detected"
            )

        # ----------------------------------------------------
        # GENERAL VARIATION
        # ----------------------------------------------------

        if "varies by approximately" in text:

            risk_score += 10

        # ----------------------------------------------------
        # WORKFORCE / CUSTOMER SIGNALS
        # ----------------------------------------------------

        if any(word in text for word in [
            "turnover",
            "churn",
            "satisfaction"
        ]):

            risk_score += 20

            reasons.append(
                "People or customer health indicator detected"
            )

    # Remove duplicate reasons
    reasons = list(dict.fromkeys(reasons))

    # Keep score within 0–100
    risk_score = min(risk_score, 100)

    # --------------------------------------------------------
    # RISK CLASSIFICATION
    # --------------------------------------------------------

    if risk_score >= 70:

        risk_level = "HIGH"

        action = (
            "Immediate operational review recommended"
        )

    elif risk_score >= 40:

        risk_level = "MEDIUM"

        action = (
            "Management review recommended"
        )

    else:

        risk_level = "LOW"

        action = "Continue monitoring"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "recommended_action": action,
        "reasons": reasons
    }