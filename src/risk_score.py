SEVERITY_POINTS = {
    "High": 10,
    "Medium": 5,
    "Low": 2,
}


def calculate_risk_score(issues):
    total_score = 0

    for issue in issues:
        severity = issue["severity"]
        total_score += SEVERITY_POINTS.get(severity, 0)

    max_score = len(issues) * 10
    risk_percentage = round((total_score / max_score) * 100, 1) if max_score else 0

    if risk_percentage >= 80:
        risk_level = "Critical"
    elif risk_percentage >= 60:
        risk_level = "High"
    elif risk_percentage >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "score": total_score,
        "max_score": max_score,
        "risk_percentage": risk_percentage,
        "risk_level": risk_level,
    }