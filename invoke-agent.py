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

import os
from datetime import datetime
from google import genai
from google.genai import types

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_GCP_PROJECT_ID")
AGENT_ID = os.environ.get("AGENT_ID", "pr-review-agent")

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location="global",
)

# Create an asynchronous background interaction with streaming enabled
response_stream = client.interactions.create(
    agent=AGENT_ID,  # Calls the custom agent ID
    input="Review GitHub Pull Request #3 in https://github.com/gitrey/widget-types and provide your feedback",
    environment="remote",  # Run inside the remote environment configured for the agent
    stream=True,
    background=True,
    timeout=120,
)

print("Connecting to secure remote sandbox and listening to execution stream...\n")

feedback = []
for event in response_stream:
    event_type = getattr(event, "event_type", None)
    if event_type == "step.delta":
        delta = getattr(event, "delta", None)
        if delta and getattr(delta, "type", None) == "text":
            print(delta.text, end="", flush=True)
            feedback.append(delta.text)

timestamp = datetime.now().strftime("%m-%d-%Y-%H%M%S")
filename = f"review-feedback-{timestamp}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write("".join(feedback))
