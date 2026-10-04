def _find_column(numeric: dict, keywords: list[str]):
    """
    Find a numeric column using business-related keywords.
    """
    for column in numeric:
        column_lower = column.lower()

        for keyword in keywords:
            if keyword in column_lower:
                return column

    return None


def _percentage_change(min_value, max_value):
    """
    Calculate percentage difference safely.
    """
    if min_value == 0:
        return None

    return abs((max_value - min_value) / min_value * 100)


def generate_insights(data: dict) -> list:
    """
    Generate dataset-driven business insights.

    The engine dynamically detects relevant business metrics
    instead of assuming that a specific CSV schema is present.

    No LLM/API required.
    """

    insights = []

    numeric = data.get("numeric_summary", {})

    if not numeric:
        return [
            "No numeric business metrics were detected in the uploaded dataset."
        ]

    # --------------------------------------------------------
    # REVENUE
    # --------------------------------------------------------

    revenue_column = _find_column(
        numeric,
        ["revenue", "sales", "income", "turnover"]
    )

    if revenue_column:

        minimum = numeric[revenue_column]["min"]
        maximum = numeric[revenue_column]["max"]

        change = _percentage_change(minimum, maximum)

        if change is not None and maximum > minimum:

            insights.append(
                f"{revenue_column.replace('_', ' ').title()} varies "
                f"by approximately {change:.1f}% across the dataset."
            )

    # --------------------------------------------------------
    # COST / EXPENSE
    # --------------------------------------------------------

    cost_column = _find_column(
        numeric,
        ["operating_cost", "operating cost", "cost", "expense", "expenses"]
    )

    if cost_column:

        minimum = numeric[cost_column]["min"]
        maximum = numeric[cost_column]["max"]

        change = _percentage_change(minimum, maximum)

        if change is not None and maximum > minimum:

            insights.append(
                f"{cost_column.replace('_', ' ').title()} varies "
                f"by approximately {change:.1f}% across the dataset."
            )

    # --------------------------------------------------------
    # ORDERS / DELAYS
    # --------------------------------------------------------

    late_column = _find_column(
        numeric,
        [
            "late_orders",
            "late order",
            "late",
            "delayed_orders",
            "delayed order",
            "delay"
        ]
    )

    if late_column:

        minimum = numeric[late_column]["min"]
        maximum = numeric[late_column]["max"]

        change = _percentage_change(minimum, maximum)

        if change is not None and maximum > minimum:

            insights.append(
                f"{late_column.replace('_', ' ').title()} varies "
                f"by approximately {change:.1f}% across the dataset."
            )

    # --------------------------------------------------------
    # CUSTOMER / USER VOLUME
    # --------------------------------------------------------

    customer_column = _find_column(
        numeric,
        [
            "customers",
            "customer",
            "users",
            "users_count",
            "clients",
            "accounts"
        ]
    )

    if customer_column:

        minimum = numeric[customer_column]["min"]
        maximum = numeric[customer_column]["max"]

        if maximum > minimum:

            insights.append(
                f"{customer_column.replace('_', ' ').title()} ranges "
                f"from {minimum:.0f} to {maximum:.0f}."
            )

    # --------------------------------------------------------
    # GENERIC NUMERIC METRICS
    # --------------------------------------------------------

    known_columns = {
        column
        for column in [
            revenue_column,
            cost_column,
            late_column,
            customer_column
        ]
        if column
    }

    for column, stats in numeric.items():

        if column in known_columns:
            continue

        minimum = stats["min"]
        maximum = stats["max"]
        mean = stats["mean"]

        if mean != 0:

            variation = (
                abs(maximum - minimum) / abs(mean)
            ) * 100

            insights.append(
                f"{column.replace('_', ' ').title()} ranges from "
                f"{minimum:.2f} to {maximum:.2f}, "
                f"with an average of {mean:.2f}."
            )

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    if not insights:

        insights.append(
            "The dataset was analyzed successfully, but no "
            "specific business patterns were detected."
        )

    return insights