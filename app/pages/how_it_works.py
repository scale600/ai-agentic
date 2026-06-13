import streamlit as st

st.title("How it Works")
st.caption("Architecture and agent flow explained")

# ── Architecture ──────────────────────────────────────────────────────────────
st.header("Architecture")

st.code("""
┌─────────────────────────────────────────────────────┐
│                  Streamlit Chat UI                   │
│         Natural language in · Report out             │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              Supervisor LlmAgent                     │
│         Google ADK 2.2 · ReAct pattern              │
│         Gemini 2.5 Flash via Vertex AI              │
│                                                      │
│   "What tools do I need? In what order?"            │
└───────────┬─────────────────────────────────────────┘
            │  delegates to sub_agent
┌───────────▼─────────────────────────────────────────┐
│              IAM Audit Agent                         │
│  ┌──────────────────────────────────────────────┐   │
│  │  get_iam_policy(project_id)                  │──▶ Cloud Resource Manager API
│  │  list_service_accounts(project_id)           │──▶ IAM API
│  │  analyze_permissions(policy, service_accts)  │   │
│  │  generate_audit_report(findings)             │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
""", language="text")

# ── ReAct Loop ────────────────────────────────────────────────────────────────
st.header("ReAct Pattern")
st.markdown("The agent follows a **Think → Act → Observe** loop until it has enough information to answer.")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### 🧠 Think")
    st.markdown("""
Gemini reasons about the request:
- What do I need to know?
- Which tool answers that?
- What order makes sense?
""")
with col2:
    st.markdown("#### ⚡ Act")
    st.markdown("""
Calls a GCP API tool:
- `get_iam_policy`
- `list_service_accounts`
- `analyze_permissions`
""")
with col3:
    st.markdown("#### 👁 Observe")
    st.markdown("""
Reads the result and decides:
- Is this enough?
- Do I need another tool?
- What did I find?
""")

# ── Step-by-step ──────────────────────────────────────────────────────────────
st.header("Step-by-step Flow")

steps = [
    ("1. User input", "You type a natural language request in the chat, e.g. *\"Find overprivileged service accounts in project my-project-123\"*"),
    ("2. Supervisor receives request", "The Supervisor LlmAgent (Gemini 2.5 Flash) reads the request and decides to delegate to the IAM Audit Agent."),
    ("3. IAM Audit Agent starts ReAct loop", "The sub-agent plans its approach: first fetch the IAM policy, then list service accounts, then cross-reference for excessive permissions."),
    ("4. Tool calls to GCP APIs", "Real GCP API calls are made using your project's credentials:\n- `resourcemanager.projects.getIamPolicy`\n- `iam.serviceAccounts.list`"),
    ("5. Analysis", "`analyze_permissions` cross-checks each binding against a risk ruleset: owner/editor roles, allUsers, primitive roles, etc."),
    ("6. Report generation", "`generate_audit_report` formats findings into a Markdown report with severity levels and remediation steps."),
    ("7. Displayed in UI", "The report renders in the chat with the agent's full reasoning trace visible in the expandable status box."),
]

for title, body in steps:
    with st.expander(title, expanded=False):
        st.markdown(body)

# ── Tools ─────────────────────────────────────────────────────────────────────
st.header("Tools")

st.markdown("""
| Tool | GCP API | What it returns |
|------|---------|----------------|
| `get_iam_policy` | Cloud Resource Manager | All IAM bindings (role → members) for the project |
| `list_service_accounts` | IAM API | All service accounts with metadata |
| `analyze_permissions` | — (local logic) | Risk-scored findings: primitive roles, allUsers, cross-project SAs |
| `generate_audit_report` | — (local logic) | Markdown report with severity, findings, and recommendations |
""")

# ── Auth ──────────────────────────────────────────────────────────────────────
st.header("Authentication & Security")

st.markdown("""
No service account key files are used anywhere in this system.

| Environment | Method |
|------------|--------|
| Local dev | `gcloud auth application-default login` (ADC) |
| Cloud Run | Attached service account (Workload Identity) |
| GitHub Actions CI/CD | Workload Identity Federation (OIDC, keyless) |
""")
