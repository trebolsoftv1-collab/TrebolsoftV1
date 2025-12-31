# sync-forced-2025
import os
import requests
import random
import time

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def unique_username():
    return f"testuser_{int(time.time())}_{random.randint(1000,9999)}"


def test_register_login_and_get_user():
    username = unique_username()
    payload = {
        "username": username,
        "full_name": "Test User",
        "role": "collector",
        "password": "TestPass123!"
    }

    # Register
    r = requests.post(f"{BASE}/api/v1/auth/register", json=payload, timeout=10)
    assert r.status_code in (200, 201), f"register failed: {r.status_code} {r.text}"
    data = r.json()
    assert data.get("username") == username

    # Login (form)
    r = requests.post(
        f"{BASE}/api/v1/auth/token",
        data={"username": username, "password": payload["password"]},
        timeout=10,
    )
    assert r.status_code == 200, f"login failed: {r.status_code} {r.text}"
    token = r.json().get("access_token")
    assert token

    # Use token to call a protected endpoint (get own user)
    # We need to find user id from register response
    user_id = data.get("id") or data.get("ID") or data.get("Id")
    if not user_id:
        # fallback: call /api/v1/users/ and find by username
        r = requests.get(f"{BASE}/api/v1/users/", headers={"Authorization": f"Bearer {token}"}, timeout=10)
        assert r.status_code == 200
        users = r.json()
        matches = [u for u in users if u.get("username") == username]
        assert matches
        user_id = matches[0]["id"]

    r = requests.get(f"{BASE}/api/v1/users/{user_id}", headers={"Authorization": f"Bearer {token}"}, timeout=10)
    assert r.status_code == 200, f"get user failed: {r.status_code} {r.text}"
    u = r.json()
    assert u.get("username") == username
