def analyze_root_cause(issues):

    issue_types = [issue["issue_type"] for issue in issues]

    evidence = []
    secondary_findings = []

    primary_root_cause = "Mixed data quality anomalies detected."
    confidence = "Low"
    escalation = "Manual review recommended."

    if "Schema Drift" in issue_types or "Unexpected Columns" in issue_types:
     primary_root_cause = (
        "Upstream schema drift detected between the incoming file and expected pipeline contract."
    )
     confidence = "High"
     escalation = (
        "Review source file contract, update ingestion mapping, and confirm whether the upstream column change was intentional."
    )
    if "Schema Drift" in issue_types:
     evidence.append("Expected column missing from incoming file")

    if "Unexpected Columns" in issue_types:
     evidence.append("Unexpected column received in incoming file")

    if "Missing Required Values" in issue_types:
        evidence.append("Missing patient_id values")

    if "Duplicate Primary Key" in issue_types:
        evidence.append("Duplicate appointment_id values")

    if "Invalid Date Format" in issue_types:
        evidence.append("Invalid appointment_date values")

    if "Invalid Category" in issue_types:
        secondary_findings.append("Invalid auth_status category")

    if "Datatype Mismatch" in issue_types:
        secondary_findings.append("Non-numeric amount values")

    if (
        "Missing Required Values" in issue_types
        and "Duplicate Primary Key" in issue_types
    ):
        primary_root_cause = (
            "Likely upstream source-system extract issue."
        )
        confidence = "High"
        escalation = (
            "Notify source application owner and quarantine today's feed."
        )

    elif (
        "Invalid Date Format" in issue_types
        and "Datatype Mismatch" in issue_types
    ):
        primary_root_cause = (
            "Likely schema or formatting drift from source system."
        )
        confidence = "Medium"
        escalation = (
            "Review source file specifications and update ingestion mappings."
        )

    return {
        "primary_root_cause": primary_root_cause,
        "confidence": confidence,
        "escalation": escalation,
        "evidence": evidence,
        "secondary_findings": secondary_findings,
    }