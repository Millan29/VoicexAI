"""Simple connectivity test for AgentVerse API using AGENTVERSE_TOKEN env var.

Usage:
  python tools/test_agentverse.py

It will print the HTTP status and JSON response (if any).
"""

import os
import requests


def main():
    api_url = os.environ.get("AGENTVERSE_API_URL", "https://api.agentverse.ai")
    token = os.environ.get("AGENTVERSE_TOKEN")

    if not token:
        print("AGENTVERSE_TOKEN not set. Set the environment variable and try again.")
        return

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        r = requests.get(f"{api_url}/whoami", headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        try:
            print(r.json())
        except Exception:
            print(r.text)
    except Exception as e:
        print(f"Request failed: {e}")


if __name__ == "__main__":
    main()
