# sync-forced-2025
# sync-forced-2025
import os
import requests

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def test_health():
    r = requests.get(f"{BASE}/health", timeout=10)
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
