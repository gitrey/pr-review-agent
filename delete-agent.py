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

"""Script to safely delete/unregister a custom agent from Agent Platform.

This script initializes the Google GenAI client and attempts to delete
the custom agent defined by the AGENT_ID environment variable.
"""

import os
from google import genai

# Read the environment configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_GCP_PROJECT_ID")
AGENT_ID = os.environ.get("AGENT_ID", "pr-review-agent")

# Initialize the Agent Platform Client
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location="global",
)

# Unregister the agent
try:
    client.agents.delete(id=AGENT_ID)
    print(f"Deleted '{AGENT_ID}' agent.")
except Exception as e:
    # Safely ignore or log if the agent does not exist
    print(f"{AGENT_ID} agent deletion skipped or failed: {e}")