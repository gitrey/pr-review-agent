# PR Review Agent

An autonomous Vertex AI Custom Agent designed to automatically review GitHub Pull Requests for code quality, strict TypeScript typing contract compliance, dependencies, and compilation correctness.

## 🚀 Overview

This repository contains Python scripts to configure, run, and manage a specialized AI agent on Google Cloud Vertex AI (using the new `google-genai` SDK).

The agent has access to a secure, remote code-execution sandbox to fetch and inspect PR branches, perform builds, run tests, and generate detailed engineering reviews.

---

## 📂 Project Structure

*   **[create-agent.py](file:///Users/andreyshakirov/work/github/gitrey/pr-review-agent/create-agent.py)**: Registers the agent on Vertex AI with customized system instructions, model parameters, and code execution capabilities.
*   **[invoke-agent.py](file:///Users/andreyshakirov/work/github/gitrey/pr-review-agent/invoke-agent.py)**: Runs a streaming interaction with the agent requesting a review of a specified PR, writes console output in real-time, and saves the final result to a timestamped Markdown report.
*   **[list-agents.py](file:///Users/andreyshakirov/work/github/gitrey/pr-review-agent/list-agents.py)**: Lists all active agents configured in your Vertex AI project and location.
*   **[delete-agent.py](file:///Users/andreyshakirov/work/github/gitrey/pr-review-agent/delete-agent.py)**: Unregisters/deletes the agent from the GCP project.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
*   A Google Cloud Platform (GCP) project with the **Vertex AI API** enabled.
*   Authenticated gcloud credentials on your machine.

### 2. Configure Environment Variables
Set the Google Cloud Project ID and optional override agent ID:
```bash
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export AGENT_ID="pr-review-agent" # Optional, defaults to pr-review-agent
```

### 3. Installation
Create a Python virtual environment and install the required dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 📖 Usage Guide

### Step 1: Create the Agent
Register your agent in Vertex AI. This configures the agent's identity ("You are a principal software engineer") and grants it the remote `code_execution` environment capability:
```bash
python create-agent.py
```

### Step 2: Invoke a Pull Request Review
Trigger a code review. You can customize the prompt/PR URL in `invoke-agent.py`. The review runs asynchronously in the cloud sandbox, outputs live progress/actions to your console, and automatically saves a file:
```bash
python invoke-agent.py
```
Outputs are written to timestamped files in the format:
`review-feedback-MM-DD-YYYY-HHMMSS.md`

### Step 3: Manage Agents
You can list your active agents or unregister them using:
```bash
# List agents
python list-agents.py

# Delete agent
python delete-agent.py
```
