# publicG8

Streamlit deploy
https://publicg8-5u5tu2qrcg3afdr57hffhd.streamlit.app/

When your Streamlit app is deployed (e.g., at `https://publicg8-5u5tu2qrcg3afdr57hffhd.streamlit.app/`), and a user makes selections, **those selections are not automatically pushed to the MDX file in GitHub unless you explicitly add code to do so**. Here’s how the process works and how to implement it:

---

## **How It Works (Default Behavior)**
- The deployed Streamlit app runs in its own cloud environment.
- When a user interacts (e.g., checks boxes), the app can update files in its own temporary file system.
- However, these changes **do not sync back to your GitHub repo or your Mintlify-hosted MDX files automatically**[2].

---

## **How to Enable Automatic Updates to the MDX File in GitHub**

To push user selections into the MDX file in GitHub (which then triggers Mintlify to redeploy your docs), you need to:

1. **Collect the user selections** in your Streamlit app (which you already do).
2. **Generate the new MDX file content** based on those selections.
3. **Authenticate to GitHub** using a Personal Access Token (stored securely in Streamlit secrets).
4. **Use the GitHub API** (e.g., via the `PyGithub` library) to:
    - Fetch the current MDX file from the repo.
    - Update it with the new content.
    - Commit and push the change back to the repo.

**Example Python snippet (using PyGithub):**
```python
from github import Github
import streamlit as st

# Store your GitHub token in Streamlit secrets
g = Github(st.secrets["GITHUB_TOKEN"])
repo = g.get_repo("yourusername/yourrepo")
file = repo.get_contents("docs/selected_agents.mdx")  # Path to your MDX file

# new_mdx_content is the string with the updated content
repo.update_file(
    file.path,
    "Update selected_agents.mdx from Streamlit app",
    new_mdx_content,
    file.sha
)
st.success("MDX file updated in GitHub!")
```
- This code runs when the user clicks "Save" in your app.
- The commit to GitHub triggers Mintlify to redeploy your docs site with the updated MDX file.

---

## **Key Points**

- **You must add code to your Streamlit app to push changes to GitHub.**
- **Streamlit Cloud does not sync file changes to GitHub automatically**—it only pulls code from GitHub, not the other way around[2].
- **Once the MDX file is updated in GitHub, Mintlify automatically redeploys your docs site.**

---

## **References**
- [Streamlit Cloud does not push file changes to GitHub automatically][2].
- [PyGithub documentation for updating files in a repo][1].

---

**Summary:**  
To push user selections from your deployed Streamlit app into the MDX file in GitHub, your app must authenticate to GitHub and programmatically update the file using the GitHub API. This triggers Mintlify to redeploy your documentation with the new content. Without this explicit integration, changes made by users in the deployed app will not update your GitHub repo or live docs[2].

[1] https://github.com/whitphx/streamlit-docs
[2] https://discuss.streamlit.io/t/update-github-csv-with-new-input-entries/38324
[3] https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/README.md
[4] https://github.com/streamlit/streamlit/issues/5178
[5] https://github.com/streamlit/streamlit/issues/10519
[6] https://www.youtube.com/watch?v=t4Z4XQuFviM
[7] https://www.youtube.com/watch?v=5uEbrc_rnYM
[8] https://github.com/liara-cloud/docs/blob/master/src/pages/paas/docker/related-apps/streamlit.mdx