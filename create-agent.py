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
from google import genai
from google.genai import types

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_GCP_PROJECT_ID")
AGENT_ID = os.environ.get("AGENT_ID", "pr-review-agent")

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location="global",
)

try:
    client.agents.delete(id=AGENT_ID)
except Exception:
    pass


# Create a custom agent configuration
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

print(f"Initiating agent creation: {AGENT_ID}")
