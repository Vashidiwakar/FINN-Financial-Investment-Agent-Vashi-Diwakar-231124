"""
Smoke test suite for FINN backend endpoints.
"""
import sys
import os

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    print("[PASS] Health check passed")

def test_portfolio():
    res = client.get("/api/portfolio")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] >= 15
    print(f"[PASS] Portfolio endpoint passed ({data['count']} stocks monitored)")

def test_digest():
    res = client.get("/api/digest?window=24&category=all")
    assert res.status_code == 200
    data = res.json()
    assert len(data["feed"]) > 0
    print(f"[PASS] Push Digest endpoint passed ({len(data['feed'])} active prioritized signals)")

def test_alerts():
    res = client.get("/api/alerts?price_thresh=3.0&vol_thresh=1.8")
    assert res.status_code == 200
    data = res.json()
    assert "alerts" in data
    print(f"[PASS] Triggered Alerts endpoint passed ({data['alert_count']} triggered alerts)")

def test_research():
    res = client.get("/api/research?ticker=TATAMOTORS.NS")
    assert res.status_code == 200
    data = res.json()
    assert "research" in data
    assert "narrative_vs_numbers" in data["research"]
    print("[PASS] Pull Research (Narrative vs Numbers) passed for TATAMOTORS.NS")

    # Test ad-hoc outside ticker generalisation
    res_adhoc = client.get("/api/research?ticker=ZOMATO.NS")
    assert res_adhoc.status_code == 200
    print("[PASS] Pull Research generalisation passed for ad-hoc ZOMATO.NS")

if __name__ == "__main__":
    print("Running FINN End-to-End Smoke Tests...")
    test_health()
    test_portfolio()
    test_digest()
    test_alerts()
    test_research()
    print("\n>>> ALL FINN SYSTEMS OPERATIONAL & VALIDATED! <<<\n")
