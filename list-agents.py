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

"""Script to query and list all custom agents registered in your Agent Platform project.

This script fetches the active agent resource definitions from Google Cloud Platform
and prints their unique identifiers and base model configurations.
"""

import os
from google import genai

# Read the environment configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_GCP_PROJECT_ID")

# Initialize the Agent Platform Client
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location="global",
)

# Retrieve list of all custom agents from the project
agents = client.agents.list()

agents_list = agents.agents or []

print(f"Found {len(agents_list)} Antigravity agents:")
for a in agents_list:
    print(f"Agent ID: {a.id} (Base: {a.base_agent})")