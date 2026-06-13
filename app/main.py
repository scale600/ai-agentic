import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.agent_client import run_agent
from config.settings import GCP_PROJECT_ID

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Agentic — GCP IAM Audit",
    page_icon="🔐",
    layout="wide",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🔐 AI Agentic")
    st.caption("GCP IAM Audit Agent · Google ADK + Gemini on Vertex AI")
    st.divider()

    project_id = st.text_input(
        "GCP Project ID",
        value=GCP_PROJECT_ID,
        placeholder="your-project-id",
    )

    st.markdown("**Example prompts**")
    examples = [
        "Audit IAM policies and generate a full security report",
        "Find service accounts with excessive permissions",
        "Check for public access (allUsers) in IAM bindings",
    ]
    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.pending_prompt = example

    st.divider()
    st.markdown(
        "**Stack:** Google ADK 2.2 · Gemini 2.5 Flash · Vertex AI · LangChain\n\n"
        "[![GitHub](https://img.shields.io/badge/GitHub-scale600/ai--agentic-181717?logo=github)](https://github.com/scale600/ai-agentic)"
    )

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# ── Main area ─────────────────────────────────────────────────────────────────
st.title("GCP IAM Audit Agent")
st.caption(
    f"Connected to project **`{project_id}`** · "
    "Powered by Google ADK + Gemini 2.5 Flash on Vertex AI"
)

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("is_report"):
            st.markdown(msg["content"])
        else:
            st.write(msg["content"])

# ── Input handling ────────────────────────────────────────────────────────────
prompt = st.chat_input("Ask the agent to audit your GCP IAM policies...")

# Sidebar button overrides chat input
if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Run agent and stream UI
    with st.chat_message("assistant"):
        status_box = st.status("Agent is working...", expanded=True)
        report_placeholder = st.empty()

        with status_box:
            st.write(f"**Project:** `{project_id}`")
            st.write(f"**Request:** {prompt}")
            st.divider()

            trace_steps, final_report = run_agent(prompt, project_id)

            for author, text in trace_steps:
                label = "🤖 Supervisor" if author == "supervisor" else "🔍 IAM Audit Agent"
                with st.expander(f"{label}", expanded=False):
                    st.markdown(text[:500] + ("…" if len(text) > 500 else ""))

        status_box.update(label="✅ Audit complete", state="complete", expanded=False)

        if final_report:
            report_placeholder.markdown(final_report)
            st.session_state.messages.append(
                {"role": "assistant", "content": final_report, "is_report": True}
            )
        else:
            fallback = "Agent completed but returned no report. Please try again."
            report_placeholder.warning(fallback)
            st.session_state.messages.append(
                {"role": "assistant", "content": fallback}
            )
