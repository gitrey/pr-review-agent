# Code review with Managed Antigravity Agents

## Overview

Managed Agents API on Agent Platform lets you build managed, autonomous agents
with a single API call. Powered by the Antigravity harness, each agent runs in a
sandbox environment where it reasons, plans, uses agent skills, executes code,
searches the web, and reads and writes files.

Managed Agents API on Agent Platform leverages two key interfaces:

- **Agents API:** The control plane for managing agents. Use it to create agents
  from configurations and configure their execution environments, including
  mounting external data sources and defining network allowlists. The system
  applies these configurations to the agent's sandbox execution environment.
- **Interactions API:** This is the data plane, serving as the primary interface
  to communicate and interact with your deployed agents at runtime. It connects
  to the agent created using agents API.

### What you will learn

In this lab, you will learn how to do the following:

- How to build and deploy managed agents
- How to automate code review tasks

### Prerequisites

- This lab assumes familiarity with the Cloud Console and Cloud Shell
  environments.

## Setup and Requirements

## Setup the workspace

Activate Cloud Shell by clicking on the icon to the right of the search bar.

Click “Continue”:

If prompted to authorize, click “Authorize” to continue.

In the terminal, run the command to enable Agent Platform APIs.

```bash
gcloud services enable aiplatform.googleapis.com
```

If you encounter terminal errors, search for “Agent Platform” in the Cloud
Console and enable the required APIs from the product page.

Run the commands below to create a new folder.

```bash
mkdir managed-agents
```

Click “Cloud Shell Editor”.

Open the “managed-agents” folder.

Start a new terminal in the Cloud Shell Editor.

Your environment should look similar to the screenshot below.

Set required environment variables:

```bash
# Managed Agents API Skill
export PROJECT_ID="YOUR_PROJECT_ID"
export LOCATION="global"
export ACCESS_TOKEN=$(gcloud auth print-access-token)

# Gemini Interactions API Skill
export GOOGLE_GENAI_USE_ENTERPRISE=true
export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
export GOOGLE_CLOUD_LOCATION="global"
```

## Install CLI skills

Developers can install specialized skills in their CLI of choice to
programmatically manage agents and interactions:

- Gemini Enterprise Agent Platform - Managed Agents API Skill
  ([SKILL.md](https://github.com/google/skills/blob/main/skills/cloud/gemini-agents-api/SKILL.md))
- Gemini Interactions API Skill ([SKILL.md](http://skill.md/))

Run the following command in the terminal:

```bash
npx skills add google/skills
```

Select two skills from the list:

- `gemini-agents-api` (Manages custom Agent resources on Gemini Enterprise…)
- `gemini-interactions-api` (Guides the usage of Gemini Interactions API…)

Once you have completed these steps, please install find-skills when prompted.

## Antigravity CLI

The Antigravity [CLI](https://antigravity.google/docs/cli-overview) is the
lightweight Terminal User Interface surface of
[Antigravity](https://antigravity.google/). It brings the same core agentic
capabilities as Antigravity, such as multi-step reasoning, multi-file editing,
tool calling, and conversation history, directly to your terminal. It allows
developers to perform various tasks directly from their terminal, such as
understanding codebases, generating documentation and unit tests, and
refactoring code.

The key benefit of Antigravity CLI is its ability to streamline development
workflows by bringing the power of Gemini directly into the developer's
command-line environment, reducing context switching and accelerating
productivity.

Navigate to the root of the project folder:

```bash
cd ~/managed-agents
```

Start Antigravity CLI:

```bash
agy
```

To sign in, select “Use a Google Cloud project” option:

Click “Click here to authenticate” or select the complete url, copy it and open
it in a new browser tab, follow the steps to generate the code. Return to the
terminal to paste the code and set the Google Cloud project.

Set Google Cloud Location to “global”.

Set your favorite color scheme and click “Next” to continue.

Accept Terms of Service & Data Use:

To verify your setup, run following command:

```bash
/config
```

Select or type “Color Scheme”, confirm your new selection.

Run following command to verify available models:

```bash
/model
```

## Creating an agent

Use a natural language description to provision a stateful agent container
configured for static code analysis.

```text
Create a new custom agent with the ID "pr-review-agent" using the latest antigravity-preview-05-2026 base model. Set its system instruction to act as a principal software engineer specializing in security audits and code optimizations. Equip it with code execution, filesystem.
```

Review the output.

## List agents

Send the following prompt to view available agents:

```text
List all the custom managed agents currently configured under my active Google Cloud project.
```

Review the output.

## Modifying an agent's behavior

Update your agent's behavior dynamically without destroying the container.

```text
Update the system instruction for my "pr-review-agent" agent. Change it to: "You are a principal security engineer. Focus your reviews exclusively on identifying OWASP Top 10 vulnerabilities, race conditions, and memory leaks." Make sure to apply the system_instruction update mask so we don't overwrite the other settings.
```

Review the output.

## Interacting with the agent

Once the control plane(Agents API) configures your agent, switch to the data
plane(Interactions API) to kick off a code assessment.

```text
Ask pr-review-agent to review GitHub PR #3 in https://github.com/gitrey/widget-types and provide feedback on any potential security vulnerabilities.
```

Review the output.

```text
Ask pr-review-agent to review GitHub PR #45 in https://github.com/gitrey/cymbal-eats and list changed files with their summaries.
```

Review the output.

## Save agent configuration locally

Save the agent configuration locally.

```text
Save the source code for the pr-review-agent in pr-review-agent.py locally.
```

Review the output.

Open saved file in the editor for review.

## Cleaning up resources

Free up backend workspace containers when you are done testing the flow.

```text
Delete the custom agent "pr-review-agent" from my project to clean up the backend workspace containers.
```

Review the output.

Exit from the Antigravity session by pressing Ctrl+C twice.

## Create and invoke agent programmatically

Clone the repository and review existing code:

```bash
git clone https://github.com/gitrey/pr-review-agent.git && cd pr-review-agent
```

Set up and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set Google Cloud Project and Agent ID(optional):

```bash
export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
export AGENT_ID=pr-review-agent
```

Create a new agent:

```bash
python create-agent.py
```

Review agent creation code:

```python
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location="global",
)
..
agent = client.agents.create(
    id=AGENT_ID,
    base_agent="antigravity-preview-05-2026",
    system_instruction="You are a principal software engineer.",
    tools=[{"type": "code_execution"}],
    base_environment={
        "type": "remote",
        "network": {"allowlist": [{"domain": "*"}]},
    },
)
```

List existing agents:

```bash
python list-agents.py
```

Sample output:

```text
Agent ID: pr-review-agent (Base: antigravity-preview-05-2026)
```

Invoke PR review agent:

```bash
python invoke-agent.py
```

Review agent invocation code:

```python
response_stream = client.interactions.create(
    agent=AGENT_ID,
    input="Review GitHub Pull Request #3 in https://github.com/gitrey/widget-types and provide your feedback",
    environment="remote",
    stream=True,
    background=True,
    timeout=120,
)
```

Outputs are written to timestamped files in the format:
`review-feedback-MM-DD-YYYY-HHMMSS.md`. Open the generated file in the Cloud
Shell Editor for review.

Delete PR review agent:

```bash
python delete-agent.py
```

## Configure JIRA and GitHub MCP servers (Optional section)

This section explains how to configure the JIRA and GitHub MCP servers. You will
need access to a JIRA instance to create a personal access token, as well as a
GitHub account with a configured personal access token for your repository.

Switch to the branch with MCP configuration:

```bash
git checkout feature/jira-mcp-config
```

Review agent creation code(create-agent.py) and MCP servers configuration.
Update with your JIRA instance details.

```python
agent = client.agents.create(
    id=AGENT_ID,
    base_agent="antigravity-preview-05-2026",
    system_instruction="You are a principal software engineer. When required, You can pull requirements from JIRA instance: <UPDATE-WITH-YOUR-JIRA-INSTANCE>.atlassian.net",
    tools=[
        {
                "type": "mcp_server",
                "url": "https://mcp.atlassian.com/v1/mcp",
                "name": "atlassian",
                "headers": {"Authorization": f"Basic {JIRA_SERVICE_ACCOUNT_API_KEY}"},
        },
        {
                "type": "mcp_server",
                "url": "https://api.githubcopilot.com/mcp/",
                "name": "github",
                "headers": {"Authorization": f"Bearer {GITHUB_PERSONAL_ACCESS_TOKEN}"},
        },
    ],
    base_environment={
        "type": "remote",
        "network": {"allowlist": [{"domain": "*"}]},
    },
)
```

Configure personal access tokens for
[JIRA](https://id.atlassian.com/manage-profile/security/api-tokens).

Permissions:

- read/write:jira-work
- read/write:comment:jira
- read:jira-user

Create a [GitHub](https://github.com/settings/tokens) personal access token.

Permissions:

- Read and Write access to code and pull requests
- Read metadata

Set required environment variables:

```bash
export ATLASSIAN_USER_EMAIL=YOUR-JIRA-EMAIL
export ATLASSIAN_API_TOKEN=YOUR-JIRA-API-TOKEN
export JIRA_SERVICE_ACCOUNT_API_KEY=$(echo -n "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" | base64 -w 0)
export GITHUB_PERSONAL_ACCESS_TOKEN=YOUR_GITHUB_PAT
```

Create a new agent:

```bash
python create-agent.py
```

Sample output:

```text
Agent ID: pr-review-agent (Base: antigravity-preview-05-2026)
```

Review agent invocation code(invoke-agent.py). Update with your existing JIRA
issue and GitHub userid, repository name:

```python
INPUT_PROMPT = """Review requirements and acceptance criteria in the <YOUR-JIRA-PROJECT-KEY-1> JIRA issue.
Verify that all requirements and ACs are implemented in the GitHub Pull Request
https://github.com/<YOUR_GITHUB_USERID>/<YOUR_REPO>/pull/1.
Provide detailed analysis and recommendations.
Update JIRA issue - add comment with your feedback."""
..
response_stream = client.interactions.create(
    agent=AGENT_ID,
    input=INPUT_PROMPT,
    environment="remote",
    stream=True,
    background=True,
    timeout=120,
)
```

Invoke PR review agent:

```bash
python invoke-agent.py
```

Review the generated file locally. Check for new comments on the JIRA issue you
configured during the agent invocation.

## Congratulations!

You have successfully completed the Managed Antigravity Agents lab.

In this lab, you experienced firsthand how the Managed Agents API and the Agent
Platform streamline the creation and deployment of autonomous agents. By
leveraging the Antigravity CLI, you were able to bring the power of Gemini
directly into your development environment, minimizing context switching and
enhancing productivity.

### What we’ve covered:

- **Environment Setup:** You configured your Cloud Shell environment and enabled
  the necessary Agent Platform APIs.
- **Antigravity CLI:** You installed, authenticated, and configured the
  Antigravity CLI, turning your terminal into an AI-powered workspace.
- **Skill Management:** You installed specialized CLI skills to manage agents
  and their interactions programmatically.
- **Agent Creation & Modification:** You used natural language via the Agents
  API to provision a custom agent (pr-review-agent) for static code analysis,
  and dynamically updated its system instructions to focus on specific security
  vulnerabilities.
- **Agent Interaction:** You utilized the Interactions API to instruct your
  agent to perform automated code reviews on real GitHub Pull Requests,
  demonstrating its ability to reason, analyze code, and provide actionable
  feedback.
- **Resource Management:** You saved your agent's configuration locally and
  learned how to clean up backend workspace containers when finished.

### What’s next:

- More hands-on sessions are coming!
- Review
  [documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/managed-agents).

## Clean up

To avoid incurring charges to your Google Cloud account for the resources used
in this tutorial, either delete the project that contains the resources, or keep
the project and delete the individual resources.
