import pandas as pd


def clean_data(df, issues):
    cleaned_df = df.copy()
    issue_types = [issue["issue_type"] for issue in issues]

    if "Duplicate Primary Key" in issue_types:
        cleaned_df = cleaned_df.drop_duplicates(
            subset=["appointment_id"],
            keep="first"
        )

    if "Missing Required Values" in issue_types:
        cleaned_df = cleaned_df.dropna(subset=["patient_id"])

    if "Invalid Date Format" in issue_types:
        cleaned_df["appointment_date"] = pd.to_datetime(
            cleaned_df["appointment_date"],
            errors="coerce"
        )
        cleaned_df = cleaned_df.dropna(subset=["appointment_date"])

    if "Datatype Mismatch" in issue_types:
        cleaned_df["amount"] = pd.to_numeric(
            cleaned_df["amount"],
            errors="coerce"
        )
        cleaned_df = cleaned_df.dropna(subset=["amount"])

    if "Invalid Category" in issue_types:
        valid_status = ["Approved", "Pending", "Denied"]
        cleaned_df = cleaned_df[
            cleaned_df["auth_status"].isin(valid_status)
        ]

    return cleaned_df