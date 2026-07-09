# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script to invoke the custom PR review agent and process its real-time response.

This script initiates a streaming session with the custom agent in Agent Platform to perform
a code review of a specified pull request. The agent's output is printed chunk-by-chunk
as it streams from the server and is written to a local timestamped markdown file at the end.
"""

import os
from datetime import datetime
from google import genai
from google.genai import types

# Read the environment configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_GCP_PROJECT_ID")
AGENT_ID = os.environ.get("AGENT_ID", "pr-review-agent")

# Initialize the Agent Platform Client
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location="global",
)

# Start a streaming interaction with the target agent.
# - stream=True: Enables Server-Sent Events (SSE) streaming for real-time output.
# - background=True: Runs the agent execution asynchronously.
# - timeout=120: Client HTTP read timeout (in seconds) to accommodate long execution times.
response_stream = client.interactions.create(
    agent=AGENT_ID,
    input="Review GitHub Pull Request #3 in https://github.com/gitrey/widget-types and provide your feedback",
    environment="remote",
    stream=True,
    background=True,
    timeout=120,
)

print("Connecting to secure remote sandbox and listening to execution stream...\n")

feedback = []

# Listen to the SSE event stream and process events
for event in response_stream:
    event_type = getattr(event, "event_type", None)
    
    # Process text delta events representing parts of the generated review
    if event_type == "step.delta":
        delta = getattr(event, "delta", None)
        if delta and getattr(delta, "type", None) == "text":
            # Print each chunk of text immediately to stdout
            print(delta.text, end="", flush=True)
            feedback.append(delta.text)

# Save the full review feedback to a timestamped Markdown report
timestamp = datetime.now().strftime("%m-%d-%Y-%H%M%S")
filename = f"review-feedback-{timestamp}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write("".join(feedback))
