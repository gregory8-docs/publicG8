import streamlit as st
import os
import json
from datetime import datetime

# Define checklist items for each category
main_options = [
    "Medical Device FDA Compliance Checker",
    "Regulatory document summary",
    "Patient interactive chat",
    "Recruiting email",
    "Query test cases",
    "Review hallucination risk",
    "Stakeholder sign-off",
]

deploy_options = [
    "Security audit",
    "Deploy endpoint",
    "Monitor post-deployment"
]

additional_options = [
    "User training",
    "Documentation update",
    "Feedback collection"
]

# Task link mapping (only for the first main option)
task_links = {
    "Medical Device FDA Compliance Checker": "https://app.writer.com/organization/923431/team/838940/document/1?mode=coWrite&currentTemplateId=8b8089bb-03d6-453a-b9b8-dbb9fed5db93",

    "Regulatory document summary": "https://app.writer.com/organization/923431/team/838940/document/1?mode=coWrite&currentTemplateId=8c963413-d722-4104-b5f3-bb10cb6236bd",

    "Patient interactive chat": "http://127.0.0.1:3005/",

    "Recruiting email": "https://app.writer.com/organization/923431/team/838940/document/1?mode=coWrite&currentTemplateId=373678cc-8c08-468b-aff9-a8e09b2807aa"

}

# Paths
json_dir = os.path.join(os.getcwd(), "json")
json_path = os.path.join(json_dir, "selected_agents.json")
intake_dir = os.path.join(os.getcwd(), "intake")
mdx_path = os.path.join(intake_dir, "selected_agents.mdx")

# Load previous selections if available
if os.path.exists(json_path):
    with open(json_path, "r") as jf:
        prev = json.load(jf)
    prev_main = set(prev.get("selected_main", []))
    prev_deploy = set(prev.get("selected_deploy", []))
    prev_additional = set(prev.get("selected_additional", []))
else:
    prev_main, prev_deploy, prev_additional = set(), set(), set()

# Heading
st.markdown("## Select Your Tasks")
st.info("Select some tasks then click Save. Uncheck to clear selections.")

# Category 1: Main Tasks
st.markdown("#### Main Tasks")
selected_main = [opt for opt in main_options if st.checkbox(opt, key=f"main_{opt}", value=opt in prev_main)]

# Category 2: Deployment Tasks
st.markdown("#### Deployment Tasks")
selected_deploy = [opt for opt in deploy_options if st.checkbox(opt, key=f"deploy_{opt}", value=opt in prev_deploy)]

# Category 3: Additional Tasks
st.markdown("#### Additional Tasks")
selected_additional = [opt for opt in additional_options if st.checkbox(opt, key=f"additional_{opt}", value=opt in prev_additional)]

st.markdown("---")

# Save button only
save_clicked = st.button("💾 Save")

# Handle Save logic
if save_clicked:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Main tasks: link only for "Medical Device FDA Compliance Checker"
    def main_task_line(item):
        if item in ["Medical Device FDA Compliance Checker", "Regulatory document summary", "Patient interactive chat", "Recruiting email"]:
            url = task_links[item]
            return f"- [{item}]({url})"
        else:
            return f"- {item}"

    # MDX content with link for the first main task only
    mdx_content = (
        "---\n"
        "title: Selected Agents\n"
        "description: A checklist of selected agents\n"
        "icon: book\n"
        "---\n\n"
        "These are the agents you have selected. [Return to the checklist app to make changes](http://localhost:8501)\n\n"
        "## Main Tasks\n\n"
        + ("\n".join(main_task_line(item) for item in selected_main) if selected_main else "_None selected_")
        + "\n\n## Deployment Tasks\n\n"
        + ("\n".join(f"- {item}" for item in selected_deploy) if selected_deploy else "_None selected_")
        + "\n\n## Additional Tasks\n\n"
        + ("\n".join(f"- {item}" for item in selected_additional) if selected_additional else "_None selected_")
        + f"\n\n_Last updated: {timestamp}_"
    )

    # Save MDX
    os.makedirs(intake_dir, exist_ok=True)
    with open(mdx_path, "w") as f:
        f.write(mdx_content)
    os.utime(mdx_path, None)

    # Save JSON
    os.makedirs(json_dir, exist_ok=True)
    json_content = {
        "selected_main": selected_main,
        "selected_deploy": selected_deploy,
        "selected_additional": selected_additional,
        "timestamp": timestamp
    }
    with open(json_path, "w") as jf:
        json.dump(json_content, jf, indent=2)
    os.utime(json_path, None)

    st.success("Selections saved. Uncheck boxes to clear selections and click Save again.")
