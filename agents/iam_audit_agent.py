"""
IAM Audit Sub-Agent — handles GCP IAM auditing tasks.
Receives delegation from the Supervisor and calls IAM tools via ReAct.
"""

from google.adk.agents import LlmAgent
from tools.gcp_iam_tools import get_iam_policy, list_service_accounts, analyze_permissions
from tools.report_tools import generate_audit_report
from config.settings import GEMINI_MODEL

iam_audit_agent = LlmAgent(
    name="iam_audit_agent",
    model=GEMINI_MODEL,
    description=(
        "Specialist agent for GCP IAM auditing. "
        "Fetches IAM policies, lists service accounts, analyzes permissions for violations, "
        "and generates a structured Markdown audit report."
    ),
    instruction="""
You are a GCP IAM security auditor. When given a project ID (or use the default project):

1. Call get_iam_policy() to fetch all IAM bindings.
2. Call list_service_accounts() to enumerate service accounts.
3. Call analyze_permissions() to detect violations (CRITICAL / HIGH / MEDIUM).
4. Call generate_audit_report() with the analysis result to produce a Markdown report.

Always complete all four steps and return the full Markdown report as your final response.
Never skip a step. If a project_id is not specified, use the default configured project.
""",
    tools=[
        get_iam_policy,
        list_service_accounts,
        analyze_permissions,
        generate_audit_report,
    ],
)
