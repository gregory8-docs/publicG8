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


---

Here is a detailed, step-by-step procedure for enabling your deployed Streamlit app to update an MDX file in your GitHub repository based on user selections, thereby triggering Mintlify to redeploy your documentation site.

---

# **Automating MDX File Updates from a Deployed Streamlit App**

## **Overview**

This guide describes how to configure a deployed Streamlit application to update an MDX file in a GitHub repository based on user input. This workflow is ideal for teams using Mintlify to host documentation, as each update to the MDX file in GitHub will automatically trigger a redeployment of the Mintlify documentation site.

---

## **Prerequisites**

- A GitHub repository containing your MDX documentation files.
- A Mintlify project connected to your GitHub repository.
- A deployed Streamlit app (e.g., on Streamlit Cloud).
- Basic familiarity with Python and GitHub.
- Administrative access to your GitHub repository.

---

## **Procedure**

### **1. Generate a GitHub Personal Access Token**

1. Log in to your GitHub account.
2. Navigate to **Settings** > **Developer settings** > **Personal access tokens**.
3. Click **Generate new token**.
4. Give the token a descriptive name (e.g., `StreamlitMDXUpdater`).
5. Select the following scopes:
    - `repo` (for private repositories)
    - `public_repo` (for public repositories)
6. Click **Generate token** and **copy** the token value.  
   **Note:** This is the only time you will be able to see the token.

---

### **2. Store the Token in Streamlit Cloud Secrets**

1. Go to your [Streamlit Cloud dashboard](https://streamlit.io/cloud).
2. Select your deployed app.
3. Click **Settings** > **Secrets**.
4. Add your token as a secret, for example:
    ```
    GITHUB_TOKEN = your_generated_token_here
    ```

---

### **3. Update Your Streamlit App to Push Changes to GitHub**

1. Install the `PyGithub` library in your app’s environment:
    ```python
    # requirements.txt
    PyGithub
    ```

2. In your Streamlit script, add the following code to handle MDX file updates:

    ```python
    import streamlit as st
    from github import Github

    # Get user selections and generate new_mdx_content as needed
    # Example: new_mdx_content = generate_mdx_content(selections)

    # GitHub configuration
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    REPO_NAME = "yourusername/yourrepo"
    MDX_PATH = "docs/selected_agents.mdx"  # Path to your MDX file in the repo

    def update_mdx_in_github(new_content):
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents(MDX_PATH)
        repo.update_file(
            path=MDX_PATH,
            message="Update selected_agents.mdx from Streamlit app",
            content=new_content,
            sha=file.sha
        )

    # Call this function when the user clicks "Save"
    if st.button("Save"):
        try:
            update_mdx_in_github(new_mdx_content)
            st.success("MDX file updated in GitHub! Mintlify will redeploy your docs shortly.")
        except Exception as e:
            st.error(f"Failed to update MDX file: {e}")
    ```

    **Notes:**
    - Replace `yourusername/yourrepo` and `docs/selected_agents.mdx` with your actual repository and file path.
    - Ensure `new_mdx_content` contains the updated MDX content based on user selections.

---

### **4. Test the Integration**

1. Deploy or redeploy your Streamlit app with the updated code.
2. Open your app in the browser.
3. Make some selections and click **Save**.
4. Check your GitHub repository for a new commit updating the MDX file.
5. Mintlify will automatically detect the change and redeploy your documentation site (this may take a minute or two).
6. Visit your Mintlify docs site to confirm the update is reflected.

---

## **Troubleshooting**

- **Permission errors:** Ensure your GitHub token has the correct scopes and is stored correctly in Streamlit secrets.
- **File not found:** Double-check the MDX file path in your repository.
- **Mintlify not updating:** Confirm that your Mintlify project is connected to the correct repository and branch.

---

## **Security Considerations**

- Never hard-code your GitHub token in your source code.
- Always use Streamlit’s secrets management to store sensitive credentials.

---

## **Summary**

By following this procedure, your deployed Streamlit app will be able to update MDX files in your GitHub repository based on user input. Each update will trigger Mintlify to redeploy your documentation, ensuring your docs are always in sync with user-driven changes.

---

**References:**  
- [Mintlify: Connect your GitHub repo](https://mintlify.com/docs/github-integration)  
- [PyGithub documentation](https://pygithub.readthedocs.io/en/latest/introduction.html)  
- [Streamlit Cloud: Secrets management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

---

If you need a sample `generate_mdx_content` function or further customization, let me know!