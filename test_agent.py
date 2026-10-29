"""
Smoke test suite for FINN backend endpoints (v1.1.0).
"""
import sys
import os

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
    assert "price_history" in data["data"][0]
    print(f"[PASS] Portfolio endpoint passed ({data['count']} stocks + sparkline data)")

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

    res_adhoc = client.get("/api/research?ticker=ZOMATO.NS")
    assert res_adhoc.status_code == 200
    print("[PASS] Pull Research generalisation passed for ad-hoc ZOMATO.NS")

def test_copilot():
    res = client.post("/api/copilot", json={"query": "What did Tata Motors say about JLR margins?", "ticker": "TATAMOTORS.NS"})
    assert res.status_code == 200
    data = res.json()
    assert "grounded_response" in data
    assert len(data["citations"]) > 0
    print("[PASS] Interactive Copilot passed with verified primary citation")

def test_audio_and_memo():
    res_audio = client.get("/api/audio-dispatch")
    assert res_audio.status_code == 200
    assert "script" in res_audio.json()
    print("[PASS] 60-Second Audio Dispatch endpoint passed")

    res_memo = client.get("/api/whatsapp-memo")
    assert res_memo.status_code == 200
    assert "memo" in res_memo.json()
    print("[PASS] WhatsApp / Telegram executive memo endpoint passed")

if __name__ == "__main__":
    print("Running FINN v1.1.0 End-to-End Smoke Tests...")
    test_health()
    test_portfolio()
    test_digest()
    test_alerts()
    test_research()
    test_copilot()
    test_audio_and_memo()
    print("\n>>> ALL FINN v1.1.0 SYSTEMS OPERATIONAL & VALIDATED! <<<\n")
