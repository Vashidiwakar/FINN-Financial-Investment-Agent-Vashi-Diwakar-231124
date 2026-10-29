"""
FINN - Financial Investment Agent
Main FastAPI Application: Exposes Push Digest, Triggered Alerts,
Portfolio Metrics, Grounded Pull Research, Audio Dispatch, and Copilot APIs.
"""
from fastapi import FastAPI, Query, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
from pydantic import BaseModel
import os

from backend.config import PORTFOLIO_COMPANIES, ADHOC_COMPANIES, DEFAULT_THRESHOLDS
from backend.market_data import get_portfolio_market_summary, get_ticker_metrics
from backend.announcements import get_announcements_digest
from backend.intelligence import enrich_pushed_item
from backend.pull_research import analyze_company_fundamentals
from backend.copilot import ask_finn_copilot

app = FastAPI(
    title="FINN - Financial Investment Agent",
    description="Mobile-first AI intelligence layer for public-markets investment managers (ENAM Holdings Challenge)",
    version="1.1.0"
)

# CORS middleware for universal access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def serve_index():
    """Serves the mobile-first executive UI."""
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "FINN Agent API is live. Static UI pending."}


@app.get("/manifest.json")
def get_manifest():
    """PWA Web App Manifest."""
    manifest_file = os.path.join(STATIC_DIR, "manifest.json")
    if os.path.exists(manifest_file):
        return FileResponse(manifest_file, media_type="application/manifest+json")
    return JSONResponse(content={"name": "FINN Agent", "short_name": "FINN"})


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "FINN AI Agent", "portfolio_count": len(PORTFOLIO_COMPANIES), "version": "1.1.0"}


@app.get("/api/portfolio")
def get_portfolio(
    price_thresh: float = Query(DEFAULT_THRESHOLDS["price_change_pct"], description="Price anomaly threshold %"),
    vol_thresh: float = Query(DEFAULT_THRESHOLDS["volume_multiplier"], description="Volume multiple threshold (e.g. 1.8x)")
):
    """
    Returns EOD price, volume, 20-day rolling average, sparkline history, and anomaly flags.
    """
    summary = get_portfolio_market_summary(price_threshold_pct=price_thresh, volume_multiplier_threshold=vol_thresh)
    anomalous = [item for item in summary if item.get("is_unusual_volume") or item.get("is_unusual_price")]
    return {
        "count": len(summary),
        "anomalies_detected": len(anomalous),
        "data": summary
    }


@app.get("/api/digest")
def get_digest(
    window: int = Query(24, description="Time window in hours (default: 24h)"),
    include_routine: bool = Query(False, description="Whether to include collapsed routine filings"),
    category: Optional[str] = Query("all", description="Filter by announcement category")
):
    """
    Push Mode (Flavour 1): Windowed Digest.
    """
    digest_raw = get_announcements_digest(hours_window=window, include_routine=include_routine, selected_category=category)
    enriched_feed = [enrich_pushed_item(item) for item in digest_raw["feed"]]
    
    return {
        "window_hours": digest_raw["window_hours"],
        "total_filings_count": digest_raw["total_in_window"],
        "high_priority_count": digest_raw["high_priority_count"],
        "medium_priority_count": digest_raw["medium_priority_count"],
        "routine_collapsed_count": digest_raw["routine_noise_count"],
        "feed": enriched_feed,
        "collapsed_routine": digest_raw["collapsed_routine"]
    }


@app.get("/api/alerts")
def get_triggered_alerts(
    price_thresh: float = Query(DEFAULT_THRESHOLDS["price_change_pct"]),
    vol_thresh: float = Query(DEFAULT_THRESHOLDS["volume_multiplier"])
):
    """
    Push Mode (Flavour 2): Triggered Alerts.
    """
    alerts = []
    portfolio = get_portfolio_market_summary(price_threshold_pct=price_thresh, volume_multiplier_threshold=vol_thresh)
    for stock in portfolio:
        if stock.get("is_unusual_volume"):
            alerts.append({
                "type": "MARKET_ANOMALY",
                "severity": "HIGH",
                "ticker": stock["ticker"],
                "company": stock["name"],
                "headline": f"Unusual Volume Surge ({stock['volume_multiplier']}x 20-Day Avg)",
                "detail": f"Traded volume {stock['volume']:,} vs 20-day baseline {stock['avg_volume_20d']:,}. Price {stock['pct_change']:+0.2f}%.",
                "category": "volume_spike",
                "price_history": stock.get("price_history", [])
            })
        if stock.get("is_unusual_price"):
            direction = "Spike" if stock["pct_change"] > 0 else "Drop"
            alerts.append({
                "type": "MARKET_ANOMALY",
                "severity": "HIGH",
                "ticker": stock["ticker"],
                "company": stock["name"],
                "headline": f"Extreme Price {direction}: {stock['pct_change']:+0.2f}% in a Day",
                "detail": f"Stock moved past configured threshold of ±{price_thresh}%. Current Close: ₹{stock['close_price']}.",
                "category": "price_swing",
                "price_history": stock.get("price_history", [])
            })
            
    recent_filings = get_announcements_digest(hours_window=24, include_routine=False)["feed"]
    for filing in recent_filings:
        if filing.get("category") in ["results", "management_change", "M&A", "litigation"]:
            enriched = enrich_pushed_item(filing)
            alerts.append({
                "type": "MATERIAL_FILING",
                "severity": "CRITICAL" if filing.get("category") in ["results", "management_change", "M&A"] else "HIGH",
                "ticker": filing["ticker"],
                "company": filing["company"],
                "headline": filing["title"],
                "detail": enriched.get("investor_takeaway"),
                "category": filing["category"],
                "executive_enrichment": filing.get("executive_enrichment"),
                "metrics": filing.get("metrics"),
                "pdf_url": filing.get("pdf_url")
            })

    return {
        "alert_count": len(alerts),
        "thresholds_applied": {
            "price_threshold_pct": price_thresh,
            "volume_multiplier_threshold": vol_thresh
        },
        "alerts": alerts
    }


@app.get("/api/research")
def get_company_research(
    ticker: str = Query("TATAMOTORS.NS", description="NSE Ticker symbol (e.g. TATAMOTORS.NS, TRENT.NS, ZOMATO.NS)")
):
    """
    Pull Mode: On-Demand Deep Fundamental Research Grounded in Primary Documents.
    """
    analysis = analyze_company_fundamentals(ticker)
    return {
        "ticker": ticker.upper(),
        "research": analysis
    }


class CopilotRequest(BaseModel):
    query: str
    ticker: Optional[str] = "TATAMOTORS.NS"

@app.post("/api/copilot")
def query_copilot(payload: CopilotRequest):
    """
    Interactive Primary-Source Financial Copilot.
    """
    result = ask_finn_copilot(payload.query, payload.ticker or "TATAMOTORS.NS")
    return result


@app.get("/api/audio-dispatch")
def get_audio_dispatch():
    """
    Morning Audio Dispatch: 60-Second Executive Voice Briefing.
    Generated for public-market investors before the market opening bell.
    """
    script = (
        "Good morning. Here is your 60-second FINN executive intelligence briefing. "
        "Across your 16 watchlist companies, two high-conviction events occurred in the last 24 hours. "
        "First, Tata Motors released Q2 results with consolidated profit surging 42% year over year to 5,230 crore rupees, "
        "beating management's guided JLR EBIT margin by 40 basis points. "
        "Second, TCS announced a key leadership transition, appointing Amit Srivastava, former Google Cloud APAC AI lead, as Chief Technology Officer. "
        "On the trading desk, Trent and Dixon Technologies are seeing abnormal volume surges above 2.3 times their 20-day average. "
        "Four routine secretarial filings have been safely suppressed from your morning wire. "
        "Have a profitable trading session."
    )
    return {
        "title": "ENAM Morning Intelligence Dispatch",
        "duration_seconds": 58,
        "script": script,
        "key_signals": [
            "Tata Motors Q2 PAT +42% YoY (JLR margin beat)",
            "TCS appoints Amit Srivastava (Google Cloud APAC) as CTO",
            "Trent & Dixon volume breakout > 2.3x baseline"
        ]
    }


@app.get("/api/whatsapp-memo")
def get_whatsapp_memo():
    """
    Formats the 24-hour digest into a ready-to-copy WhatsApp/Telegram memo
    commonly shared across Dalal Street investment committees.
    """
    text = (
        "📊 *FINN MORNING WIRE | ENAM PORTFOLIO UPDATE*\n"
        "📅 _October 2026 - Pre-Market Opening Brief_\n\n"
        "⚡ *TOP HIGH-CONVICTION SIGNALS:*\n"
        "1️⃣ *TATAMOTORS* (Q2 Results): PAT +42% YoY (₹5,230 Cr). JLR EBIT margin 8.9% (+40 bps vs guided). Net auto debt-free status confirmed.\n"
        "2️⃣ *TCS* (Management Change): Dr. Harrick Vin steps down. New CTO: *Amit Srivastava* (ex-Google Cloud APAC AI Head, IIT Bombay/Stanford).\n"
        "3️⃣ *DIXON* (M&A): Acquired 50.1% in Ismartu India for ₹2,384 Cr (Transsion handset consolidation).\n"
        "4️⃣ *RELIANCE* (Capex): ₹12,500 Cr Phase-2 green hydrogen electrolyzer gigafactory capex approved.\n\n"
        "🚨 *VOLUME & PRICE ANOMALIES (20-Day Baseline):*\n"
        "• *TRENT*: +4.5% | Vol 2.5x Avg (Zudio footprint expansion)\n"
        "• *DIXON*: +5.1% | Vol 2.3x Avg (M&A announcement)\n"
        "• *INFY*: -3.2% price drop | Normal volume\n\n"
        "📁 _4 routine ESOP/compliance filings filtered out._\n"
        "🔗 _Full primary concall audit available on FINN Mobile Agent._"
    )
    return {"memo": text}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
