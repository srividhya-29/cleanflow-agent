"""
This is the "agentic" component.
It:

investigates issues
determines likely causes
suggests fixes
"""
def generate_remediation_plan(issues):
    remediation_steps = []

    for issue in issues:
        issue_type = issue["issue_type"]
        column = issue["affected_column"]

        if issue_type == "Missing Required Values":
            remediation_steps.append({
                "issue_type": issue_type,
                "recommended_action": f"Quarantine rows where {column} is missing and request source-system correction.",
                "root_cause": "Likely incomplete upstream feed or missing patient mapping.",
                "business_impact": "May prevent accurate patient-level reporting and appointment reconciliation."
            })

        elif issue_type == "Duplicate Primary Key":
            remediation_steps.append({
                "issue_type": issue_type,
                "recommended_action": f"Deduplicate records using {column} and keep the latest valid record.",
                "root_cause": "Possible duplicate extract, retry job, or source-system resend.",
                "business_impact": "Can cause double counting in scheduling, billing, and operational dashboards."
            })

        elif issue_type == "Invalid Date Format":
            remediation_steps.append({
                "issue_type": issue_type,
                "recommended_action": f"Convert {column} to standard YYYY-MM-DD format and reject unparseable records.",
                "root_cause": "Date format inconsistency or malformed source values.",
                "business_impact": "Can break time-based reporting, forecasting, and appointment trend analysis."
            })

        elif issue_type == "Invalid Category":
            remediation_steps.append({
                "issue_type": issue_type,
                "recommended_action": f"Map invalid {column} values to approved categories or flag for manual review.",
                "root_cause": "Source system introduced a new status value not yet supported by downstream rules.",
                "business_impact": "Can distort authorization status reporting and workflow prioritization."
            })

        elif issue_type == "Datatype Mismatch":
            remediation_steps.append({
                "issue_type": issue_type,
                "recommended_action": f"Coerce {column} to numeric and quarantine rows that cannot be converted.",
                "root_cause": "Amount field may contain text, symbols, or inconsistent formatting.",
                "business_impact": "Can break payment calculations, billing analytics, and financial dashboards."
            })

        else:
            remediation_steps.append({
                "issue_type": issue_type,
                "recommended_action": "Review affected records and update validation rules.",
                "root_cause": "Unknown data quality issue.",
                "business_impact": "May affect downstream analytics reliability."
            })

    return remediation_steps