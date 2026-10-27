"""
FINN - Financial Investment Agent
Main FastAPI Application: Exposes Push Digest, Triggered Alerts,
Portfolio Metrics, and Grounded Pull Research APIs. Serves Mobile-First UI.
"""
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os

from backend.config import PORTFOLIO_COMPANIES, ADHOC_COMPANIES, DEFAULT_THRESHOLDS
from backend.market_data import get_portfolio_market_summary, get_ticker_metrics
from backend.announcements import get_announcements_digest
from backend.intelligence import enrich_pushed_item
from backend.pull_research import analyze_company_fundamentals

app = FastAPI(
    title="FINN - Financial Investment Agent",
    description="Mobile-first AI intelligence layer for public-markets investment managers (ENAM Holdings Challenge)",
    version="1.0.0"
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


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "FINN AI Agent", "portfolio_count": len(PORTFOLIO_COMPANIES)}


@app.get("/api/portfolio")
def get_portfolio(
    price_thresh: float = Query(DEFAULT_THRESHOLDS["price_change_pct"], description="Price anomaly threshold %"),
    vol_thresh: float = Query(DEFAULT_THRESHOLDS["volume_multiplier"], description="Volume multiple threshold (e.g. 1.8x)")
):
    """
    Returns EOD price, volume, 20-day rolling average, and anomaly flags for portfolio.
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
    Filters and prioritizes announcements across the portfolio.
    Routine filings are collapsed, while high-impact items are enriched with smart investor takeaways.
    """
    digest_raw = get_announcements_digest(hours_window=window, include_routine=include_routine, selected_category=category)
    
    # Enrich active feed items
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
    Fires the moment something crosses a threshold:
    - Volume surge > 2x recent 20-day average
    - Price move beyond +/- X%
    - Tier-1 Material Corporate Announcements (Results, M&A, Management changes)
    """
    alerts = []
    
    # 1. Market Anomalies
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
                "category": "volume_spike"
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
                "category": "price_swing"
            })
            
    # 2. Material Corporate Filing Alerts
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
    Pull Mode: On-Demand Deep Fundamental Research.
    Grounded strictly in primary sources (Annual Reports + Concall Transcripts).
    Features Narrative vs. Numbers (Guidance vs Delivery) analysis,
    Cash Quality & Conversion, Credibility score, and Bull/Bear thesis.
    """
    analysis = analyze_company_fundamentals(ticker)
    return {
        "ticker": ticker.upper(),
        "generated_at": analyze_company_fundamentals.__name__,
        "research": analysis
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
