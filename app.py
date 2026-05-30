import streamlit as st
import pandas as pd
from src.profiler import profile_data
from src.remediation_agent import generate_remediation_plan
from src.root_cause_agent import analyze_root_cause
from src.risk_score import calculate_risk_score
from src.code_generator import generate_cleaning_code
from src.report_generator import generate_report
from src.cleaner import clean_data

from src.validator import validate_data


st.set_page_config(
    page_title="CleanFlow Agent",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 CleanFlow Agent")
st.subheader("Agentic Data Quality & Pipeline Remediation Assistant")

st.write(
    "Enter a CSV file path or upload a CSV. CleanFlow simulates a pipeline validation check "
    "and activates the remediation agent when data quality issues are found."
)

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

csv_path = st.text_input(
    "Or enter CSV file path",
    value="data/broken_appointments.csv"
)

df = None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

elif csv_path:
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        st.error(f"Could not read file from path: {e}")

if df is not None:
    st.subheader("Data Preview")
    st.dataframe(df.head(20), use_container_width=True)
    profile = profile_data(df)

    with st.expander("View Data Profile"):
        st.json(profile)

    if st.button("Run Pipeline Check"):
        issues = validate_data(df)

        if not issues:
            st.success("✅ Pipeline validation passed. No remediation needed.")
        else:
            st.error("🚨 Pipeline validation failed. CleanFlow Agent activated.")

            st.subheader("Detected Issues")
            issues_df = pd.DataFrame(issues)
            st.dataframe(issues_df, use_container_width=True)
            risk = calculate_risk_score(issues)

            st.subheader("Pipeline Risk Score")

            st.metric(
                label="Pipeline Risk Level",
                value=risk["risk_level"],
                delta=f"{risk['score']} / {risk['max_score']} points"
            )

            st.progress(int(risk["risk_percentage"]))

            st.write(f"Risk Percentage: **{risk['risk_percentage']}%**")
            remediation_plan = generate_remediation_plan(issues)

            st.subheader("Agent Remediation Plan")
            st.dataframe(remediation_plan, use_container_width=True)

            root_cause = analyze_root_cause(issues)

            st.subheader("Root Cause Investigation")

            st.write(
                f"### Primary Root Cause\n"
                f"{root_cause['primary_root_cause']}"
            )

            st.write(
                f"**Confidence:** {root_cause['confidence']}"
            )

            st.write("### Evidence")

            for item in root_cause["evidence"]:
                st.write(f"✓ {item}")

            st.write("### Secondary Findings")

            for item in root_cause["secondary_findings"]:
                st.write(f"• {item}")

            st.write("### Recommended Escalation")
            st.write(root_cause["escalation"])

            cleaning_code = generate_cleaning_code(issues)

            st.subheader("Generated Cleaning Code")
            st.code(cleaning_code, language="python")
            
            report = generate_report(
                issues,
                remediation_plan,
                root_cause,
                risk,
                cleaning_code
            )

            st.subheader("Download Outputs")

            cleaned_df = clean_data(df, issues)
            csv_data = cleaned_df.to_csv(index=False)

            st.download_button(
                label="Download Cleaned CSV",
                data=csv_data,
                file_name="cleaned_appointments.csv",
                mime="text/csv"
            )

            st.download_button(
                label="Download Readable Text Report",
                data=report,
                file_name="cleanflow_remediation_report.txt",
                mime="text/plain"
            )

            st.subheader("Agent Summary")

            high_count = sum(1 for issue in issues if issue["severity"] == "High")
            medium_count = sum(1 for issue in issues if issue["severity"] == "Medium")

            st.write(
                f"""
                CleanFlow Agent detected **{len(issues)} data quality issues** in the file.

                - **High severity issues:** {high_count}
                - **Medium severity issues:** {medium_count}

                The simulated pipeline should be paused for review because critical fields such as
                appointment ID, patient ID, appointment date, and payment amount may impact downstream
                reporting, billing validation, and operational dashboards.
                """
            )