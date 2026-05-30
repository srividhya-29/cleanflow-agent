"""
Creates final business-friendly report.
"""
def generate_report(issues, remediation_plan, root_cause, risk, cleaning_code):
    report = []
    
    report.append("# CleanFlow Agent Remediation Report\n")
    
    report.append("## Pipeline Risk Summary\n")
    report.append(f"- Risk Level: {risk['risk_level']}")
    report.append(f"- Risk Score: {risk['score']} / {risk['max_score']}")
    report.append(f"- Risk Percentage: {risk['risk_percentage']}%\n")
    
    report.append("## Detected Issues\n")
    for issue in issues:
        report.append(f"- {issue['issue_type']} | Severity: {issue['severity']} | Column: {issue['affected_column']} | Details: {issue['details']}")
    
    report.append("\n## Root Cause Investigation\n")
    report.append(f"- Primary Root Cause: {root_cause['primary_root_cause']}")
    report.append(f"- Confidence: {root_cause['confidence']}")
    report.append(f"- Recommended Escalation: {root_cause['escalation']}")
    
    report.append("\n## Evidence\n")
    for item in root_cause["evidence"]:
        report.append(f"- {item}")
    
    report.append("\n## Secondary Findings\n")
    for item in root_cause["secondary_findings"]:
        report.append(f"- {item}")

    report.append("\n## Agent Remediation Plan\n")
    for step in remediation_plan:
        report.append(f"- Issue: {step['issue_type']}")
        report.append(f"  - Root Cause: {step['root_cause']}")
        report.append(f"  - Recommended Action: {step['recommended_action']}")
        report.append(f"  - Business Impact: {step['business_impact']}")
    
    report.append("\n## Generated Cleaning Code\n")
    report.append("```python")
    report.append(cleaning_code)
    report.append("```")
    
    return "\n".join(report)