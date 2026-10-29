# FINN: Financial Investment Agent
### ENAM Holdings - AI Engineer Build Challenge (Mobile-First Prototype)

FINN is a mobile-first financial investment agent built for public-markets investors at high-conviction investment firms. It addresses the core problem of information overload: filtering out routine corporate filing noise, highlighting high-signal developments with smart context, and auditing management guidance against primary disclosures.

---

## Quick Start (Running the Application)

### 1. Requirements
- Python 3.10+
- Dependencies installed via `pip`:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Launch the Prototype
Run the automated launcher:
```bash
python run.py
```
This starts the backend at `http://127.0.0.1:8000` and automatically opens the mobile-optimized interface in your browser.

Alternatively, run with uvicorn directly:
```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Run Backend Smoke Tests
To verify all APIs and data flows:
```bash
python test_agent.py
```

---

## Core Product Features

### 1. Push Mode: The Wire (Windowed Digest)
- Aggregates corporate filings across a 16-company portfolio over a customizable time window (24 hours default).
- **Noise Suppression:** Elevates Tier-1 high-conviction events (Results, Management Changes, M&A, Capex) and collapses routine secretarial/ESOP filings into an expandable drawer.
- **Enriched Quarterly Results:** Directly displays headline numbers — Revenue, EBITDA, PBT, PAT — with YoY% and QoQ% growth deltas.
- **Enriched Executive Transitions:** Profiles incoming CEOs/CFOs (past roles, education, track record).

### 2. Push Mode: Triggered Alerts
- Fires real-time alerts when threshold criteria are breached:
  - **Volume Surges:** Day's volume $> 1.8\times$ (or configurable $2.0\times, 2.5\times$) 20-day rolling average.
  - **Price Anomalies:** Daily move $> \pm 3.0\%$ (or configurable $\pm 2.0\%, \pm 5.0\%$).
  - **Material Exchange Disclosures:** High-severity corporate filings.

### 3. Pull Mode: Deep Primary Research (Narrative vs. Numbers)
- Grounded strictly in primary documents (Earnings Call transcripts and Annual Reports via Screener.in / Exchange Filings).
- **Narrative vs. Numbers Table:** Cross-references management guidance across 4 quarters against reported delivery with exact transcript quote citations.
- **Management Credibility Score:** Quantitative metric (0–100) scoring management's forecasting reliability.
- **Cash Quality Audit:** Computes $\text{CFO} / \text{PAT}$ ratio to verify if reported accounting profits actually turn into liquid operating cash flow.
- **Bull vs. Bear Thesis:** Grounded strictly in primary business metrics.
- **Engine Generalisation:** Supports any NSE ticker symbol (e.g., `TATAMOTORS.NS`, `TRENT.NS`, `ZOMATO.NS`, `HAL.NS`, `MAPMYINDIA.NS`).

### 4. Portfolio Radar
- Live overview of all 16 portfolio stocks showing daily price % changes, today's trading volume, and volume multiples relative to the 20-day baseline.

---

## Project Directory Structure

```
ENAM_Assignment/
│
├── README.md               # Architecture, usage, and quick start guide
├── requirements.txt        # Python package dependencies
├── run.py                  # One-click launcher (starts server & opens browser)
├── app.py                  # FastAPI application orchestrating all endpoints
├── test_agent.py           # End-to-end automated smoke test suite
│
├── backend/
│   ├── config.py           # Portfolio watchlist, alert thresholds, categories
│   ├── market_data.py      # yfinance EOD price, volume & rolling baseline engine
│   ├── announcements.py    # NSE/BSE filings aggregator, filter & priority sorter
│   ├── intelligence.py     # Smart enrichment (Results QoQ/YoY, Executive Bios)
│   └── pull_research.py    # Primary-source Narrative vs Numbers research engine
│
├── static/
│   ├── index.html          # Mobile-first executive UI
│   ├── css/style.css       # Dark fintech theme optimized for mobile viewports
│   └── js/app.js           # Client-side state, interactive pills & live queries
│
└── submission/
    ├── COVERING_NOTE.md    # Ready-to-send email covering note for ENAM submission
    └── AI_BUILD_HISTORY.md # AI interaction log and engineering thought process
```

---

## Submission Checklist
- [x] Mobile-first working prototype (`run.py` / responsive web)
- [x] Clean modular repository structure
- [x] Covering note drafted at [`submission/COVERING_NOTE.md`](submission/COVERING_NOTE.md)
- [x] AI Build history documented at [`submission/AI_BUILD_HISTORY.md`](submission/AI_BUILD_HISTORY.md)
- [x] Subject line: **"ENAM - IIT screening - 2027"** to **assessment@enam.com**
