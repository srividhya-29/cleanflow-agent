def generate_cleaning_code(issues):
    issue_types = [issue["issue_type"] for issue in issues]

    code_lines = [
        "import pandas as pd",
        "",
        "df = pd.read_csv('data/broken_appointments.csv')",
        "",
        "# CleanFlow generated remediation logic",
    ]

    if "Duplicate Primary Key" in issue_types:
        code_lines.append("df = df.drop_duplicates(subset=['appointment_id'], keep='first')")

    if "Missing Required Values" in issue_types:
        code_lines.append("df = df.dropna(subset=['patient_id'])")

    if "Invalid Date Format" in issue_types:
        code_lines.append("df['appointment_date'] = pd.to_datetime(df['appointment_date'], errors='coerce')")
        code_lines.append("df = df.dropna(subset=['appointment_date'])")

    if "Datatype Mismatch" in issue_types:
        code_lines.append("df['amount'] = pd.to_numeric(df['amount'], errors='coerce')")
        code_lines.append("df = df.dropna(subset=['amount'])")

    if "Invalid Category" in issue_types:
        code_lines.append("valid_status = ['Approved', 'Pending', 'Denied']")
        code_lines.append("df = df[df['auth_status'].isin(valid_status)]")

    code_lines.append("")
    code_lines.append("df.to_csv('reports/cleaned_appointments.csv', index=False)")

    return "\n".join(code_lines)