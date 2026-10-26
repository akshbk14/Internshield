def calculate_risk(findings: list[dict], description: str) -> dict:
    # Keep the highest score for duplicate IDs, so the same signal is not counted twice.
    unique = {}
    for finding in findings:
        key = finding["id"]
        if key not in unique or finding["points"] > unique[key]["points"]:
            unique[key] = finding

    clean_findings = sorted(unique.values(), key=lambda item: item["points"], reverse=True)
    score = min(100, sum(item["points"] for item in clean_findings))

    if len(description.strip()) < 80:
        category = "Insufficient Information"
        insufficient = True
    else:
        insufficient = False
        if score <= 24:
            category = "Low Risk"
        elif score <= 49:
            category = "Moderate Risk"
        elif score <= 74:
            category = "High Risk"
        else:
            category = "Very High Risk"

    return {
        "score": score,
        "category": category,
        "findings": clean_findings,
        "insufficient_information": insufficient,
        "summary": _summary(category, len(clean_findings))
    }


def _summary(category: str, count: int) -> str:
    if category == "Insufficient Information":
        return "There is not enough advertisement text for a meaningful assessment. Add more details and review the offer independently."
    if count == 0:
        return "No configured warning patterns were detected. This does not establish that the internship is genuine."
    if category in ("High Risk", "Very High Risk"):
        return f"The assessment found {count} warning signal(s). Pause and verify the offer independently before proceeding."
    if category == "Moderate Risk":
        return f"The assessment found {count} warning signal(s). Review the findings and verify the details before proceeding."
    return f"The assessment found {count} configured warning signal(s). A low score is not proof of legitimacy."
