import pandas as pd


EXPECTED_COLUMNS = [
    "appointment_id",
    "patient_id",
    "appointment_date",
    "payer_name",
    "auth_status",
    "amount",
    "therapy_type",
    "center_id",
]


VALID_AUTH_STATUS = ["Approved", "Pending", "Denied"]


def validate_data(df):
    issues = []

    # 1. Schema check
    missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    extra_columns = [col for col in df.columns if col not in EXPECTED_COLUMNS]

    if missing_columns:
        issues.append({
            "issue_type": "Schema Drift",
            "severity": "High",
            "details": f"Missing expected columns: {missing_columns}",
            "affected_column": ", ".join(missing_columns),
        })

    if extra_columns:
        issues.append({
            "issue_type": "Unexpected Columns",
            "severity": "Medium",
            "details": f"Unexpected columns found: {extra_columns}",
            "affected_column": ", ".join(extra_columns),
        })

    # Stop deeper checks if schema is missing required columns
    if missing_columns:
        return issues

    # 2. Missing patient_id
    missing_patient_count = df["patient_id"].isna().sum()
    if missing_patient_count > 0:
        issues.append({
            "issue_type": "Missing Required Values",
            "severity": "High",
            "details": f"{missing_patient_count} rows have missing patient_id",
            "affected_column": "patient_id",
        })

    # 3. Duplicate appointment_id
    duplicate_count = df["appointment_id"].duplicated().sum()
    if duplicate_count > 0:
        issues.append({
            "issue_type": "Duplicate Primary Key",
            "severity": "High",
            "details": f"{duplicate_count} duplicate appointment_id values detected",
            "affected_column": "appointment_id",
        })

    # 4. Invalid appointment_date
    parsed_dates = pd.to_datetime(df["appointment_date"], errors="coerce")
    invalid_date_count = parsed_dates.isna().sum()
    if invalid_date_count > 0:
        issues.append({
            "issue_type": "Invalid Date Format",
            "severity": "High",
            "details": f"{invalid_date_count} rows have invalid appointment_date values",
            "affected_column": "appointment_date",
        })

    # 5. Invalid auth_status
    invalid_status_count = (~df["auth_status"].isin(VALID_AUTH_STATUS)).sum()
    if invalid_status_count > 0:
        issues.append({
            "issue_type": "Invalid Category",
            "severity": "Medium",
            "details": f"{invalid_status_count} rows have invalid auth_status values",
            "affected_column": "auth_status",
        })

    # 6. Non-numeric amount
    parsed_amount = pd.to_numeric(df["amount"], errors="coerce")
    invalid_amount_count = parsed_amount.isna().sum()
    if invalid_amount_count > 0:
        issues.append({
            "issue_type": "Datatype Mismatch",
            "severity": "High",
            "details": f"{invalid_amount_count} rows have non-numeric amount values",
            "affected_column": "amount",
        })

    return issues