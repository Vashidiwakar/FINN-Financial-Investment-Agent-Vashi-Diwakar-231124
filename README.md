# FINN — Financial Investment Agent
### ENAM Holdings AI Engineer Build Challenge (2027 Screening)

> **Submission Status:** `READY FOR EVALUATION`  
> **Live Deployed Prototype:** [https://finn-financial-investment-agent.onrender.com](https://finn-financial-investment-agent.onrender.com)  
> **GitHub Repository:** [https://github.com/Vashidiwakar/FINN-Financial-Investment-Agent-Vashi-Diwakar-231124](https://github.com/Vashidiwakar/FINN-Financial-Investment-Agent-Vashi-Diwakar-231124)  
> **Test Suite:** 9/9 Integration Smoke Tests Passing (`test_agent.py`)  
> **Candidate:** Vashi Diwakar (4th Year Undergraduate, Electrical Engineering, IIT Kanpur)  
> **Target Reviewers:** ENAM Evaluation Team (`assessment@enam.com`)

---

## Executive Summary

**FINN** is a mobile-first investment intelligence agent engineered specifically for high-conviction public markets investors. Instead of creating more noise, FINN acts as an aggressive filter and research analyst companion: prioritizing high-signal developments, suppressing routine corporate filing paperwork, and cross-referencing management narrative against audited delivery.

---

## 1. Quick Start for Evaluators

### Step 1: Clone & Install Dependencies
Ensure you have **Python 3.10+** installed:
```bash
# Clone repository & enter directory
git clone https://github.com/Vashidiwakar/FINN-Financial-Investment-Agent-Vashi-Diwakar-231124.git
cd FINN-Financial-Investment-Agent-Vashi-Diwakar-231124

# Install minimal dependencies
pip install -r requirements.txt
```

### Step 2: Run Automated Smoke Tests
Validate that all backend endpoints, data feeds, and research engines are operational:
```bash
python test_agent.py
```
*(Expected output: All 9 test suites pass with `[PASS]` tags)*.

### Step 3: Launch the Prototype
```bash
python run.py
```
This boots the server on port `8000` and automatically opens `http://localhost:8000` in your default browser.

### Evaluator Quick-Start Credentials
When the prototype opens, use the **One-Click Evaluator Sign In** button or manually enter the pre-registered credentials:
* **Email:** `example@example.com`
* **Password:** `password123`
*(Or switch to "Create Account" to test new analyst registrations with real-time email verification).*

---

## 2. How to Test on Phone & Laptop

FINN is built **mobile-first** (`max-width: 480px`) to serve portfolio managers and analysts on the move.

### A. Testing on Laptop / Desktop (Mobile Simulator)
For the best evaluator experience on a desktop:
1. Open `http://localhost:8000` in **Chrome** or **Edge**.
2. Press **`F12`** (or right-click anywhere $\rightarrow$ **Inspect**).
3. Press **`Ctrl + Shift + M`** (Toggle Device Toolbar).
4. Select **iPhone 14 / iPhone 15 Pro** or **Pixel 7** from the top device dropdown to test touch scrolling, drawers, and tabs.

---

### B. Testing Directly on a Smartphone

#### Method 1: Local Network (Zero Setup)
`run.py` automatically binds to `0.0.0.0` and detects your machine's local IP address.

1. **Connect your phone and laptop to the same Wi-Fi network** (or connect your laptop to your phone's personal hotspot).
2. On your laptop, run:
   ```bash
   python run.py
   ```
3. The terminal prints your mobile URL:
   ```text
   =================================================================
     FINN: Financial Investment Agent (ENAM Holdings Challenge)
     Mobile-First AI Intelligence Layer for Public Markets
   =================================================================

     [Local PC]    : http://localhost:8000
     [On Your Phone]: http://<YOUR-LOCAL-IP>:8000 (e.g. http://192.168.1.5:8000)
   =================================================================
   ```
4. Open **Safari** (iOS) or **Chrome** (Android) on your phone and navigate to `http://<YOUR-LOCAL-IP>:8000`.  
*(If Windows Defender Firewall prompts you, select **"Allow access"**).*

#### Method 2: If on Corporate / Organization Wi-Fi (Client Isolation)
Enterprise office and organization Wi-Fi networks frequently block direct peer-to-peer device communication for network security. If Method 1 does not connect:

* **Option A (Personal Hotspot):** Turn on your phone's personal hotspot, connect your laptop to it, and re-run `python run.py`.
* **Option B (Instant Free Tunnel via LocalTunnel):** In a second terminal on your PC, run:
  ```bash
  npx localtunnel --port 8000
  ```
  This generates a public HTTPS link (e.g. `https://finn-eval.loca.lt`) that you can open from **any smartphone on cellular data (4G/5G)** without network restrictions.

---

## 3. Core Functionality of the Agent

FINN operates across two primary modes: **Push (Proactive Intelligence)** and **Pull (On-Demand Primary Research)**.

### A. Push Mode: The Wire & Triggered Alerts
* **16-Company Portfolio Watchlist:** Tracks a balanced mock portfolio spanning large-cap leaders (*Reliance, TCS, HDFC Bank, Tata Motors, Infosys*) and hyper-growth mid-caps (*Trent, Dixon Technologies, CDSL, Polycab*).
* **Windowed Digest (The Wire):** Ingests and aggregates corporate exchange filings across customizable time horizons (**24 Hours default**, **3 Days**, **7 Days**, or **All**).
* **Intelligent Noise Suppression:**
  * **Tier-1 Signal Elevation:** Major corporate actions (Quarterly Results, M&A, Leadership Changes, Major Capex) are displayed prominently with custom financial highlights.
  * **Collapsible Routine Drawer:** Routine secretarial paperwork (ESOP allotments, certificate compliances under Reg 74(5)) is filtered out of the main feed and tucked into a secondary expandable drawer.
* **Smart Enrichment (No Generic Text):**
  * **Financial Results:** Automatically extracts headline figures — **Revenue, EBITDA, PBT, and PAT** — displaying both **YoY%** and **QoQ%** percentage deltas.
  * **Executive Leadership Changes:** Profiles incoming C-suite executives (past roles, educational pedigree, professional credentials).
* **Triggered Anomaly Alerts:**
  * **Volume Anomaly:** Flags trading volume exceeding **$1.8\times$** (configurable to $2.0\times$ or $2.5\times$) against the **20-day rolling average baseline**.
  * **Price Movement:** Real-time triggers when a stock moves beyond **$\pm 3.0\%$** (configurable to $\pm 2.0\%$ or $\pm 5.0\%$).

---

### B. Pull Mode: Primary-Source Research Engine
* **Strict Primary Data Discipline:** Prohibits third-party broker opinions, tweets, or hallucinated AI summaries. Grounded strictly in **Audited Annual Reports** and **Earnings Call Transcripts** via Screener.in and official exchange filings.
* **4-Quarter "Narrative vs. Numbers" Reality Check:**
  * Cross-references management guidance and forward-looking commentary over the last 4 quarters against the audited numbers delivered.
  * Provides exact transcript page/quarter citations and quantitative verdicts: `BEAT`, `DELIVERED`, or `PARTIAL MISS`.
* **Management Credibility Score:** A quantitative reliability index (0–100) scoring management's guidance consistency.
* **Cash Quality Conversion Check:** Calculates the **$\text{CFO} / \text{PAT}$** ratio to verify if accounting profit translates into liquid cash flow or aggressive accruals.
* **Grounded Bull vs. Bear Case:** Structured balance sheet, moat, and risk analysis grounded in audited business metrics.
* **Dynamic Generalisation:** Engine dynamically audits both demo portfolio companies (*Tata Motors, Trent*) and arbitrary NSE tickers (*Zomato/Eternal, HAL, Titan, Dixon*).

---

### C. Novel Interaction Features
* **60-Second Audio Voice Dispatch:** Pre-market spoken briefing summarizing portfolio overnight anomalies, complete with variable speed playback (**0.8x, 1.0x, 1.2x, 1.5x, 2.0x**) for commutes.
* **Interactive FINN Copilot Drawer:** Bottom sheet drawer answering ad-hoc analyst queries (e.g. margin guidance, store additions) with verified primary citations.
* **1-Click Dalal Street Committee Memo:** Generates clean, formatted committee memos for WhatsApp/Telegram morning briefings without emojis.
* **Inline SVG Sparklines:** Real-time 20-day price trend lines embedded inside stock cards and alert rows.
* **10 Analyst Color Themes:** Instant theme switching (Midnight Dark, Nordic Light, Bloomberg Amber, Emerald Quant, Cyberpunk Neon, Hacker Matrix, Solarized Dark, FT Paper, Dracula Pro, Oceanic Navy).
* **Secure Client Authentication:** Email syntax validation, password length checks, and a custom password visibility toggle that prevents native browser icon collisions.

---

## 4. Technical Expectations & Design Decisions

| Criterion | Implementation |
| :--- | :--- |
| **Stock Data** | Live `yfinance` engine with 20-day rolling baseline calculations and in-memory fallback cache to ensure **zero evaluation downtime**. |
| **Primary Filings** | Integrated canonical Screener.in document resolver (`#documents`, `#concalls`) with dynamic scrip routing (e.g. `500570` for Tata Motors, `ETERNAL` for Zomato). |
| **Model Routing & Cost** | Deterministic regex heuristics for sub-second filing parsing; structured prompt routing for deep concall reasoning. |
| **Zero "AI Slop"** | Metric grids, structured promise-vs-delivery scorecards, and badge chips instead of generic chatbot paragraphs. |

---

## 5. Project Directory Structure

```
ENAM_Assignment/
│
├── README.md               # Evaluator documentation & testing guide
├── requirements.txt        # Minimal Python dependencies (fastapi, uvicorn, yfinance, httpx)
├── run.py                  # Dual-bind launcher (broadcasts to localhost & local phone IP)
├── app.py                  # FastAPI router orchestrating Push, Pull, Audio, & Copilot
├── test_agent.py           # 9-suite automated end-to-end integration test runner
├── .gitignore              # Ignores __pycache__, pyc, and virtualenv files
│
├── backend/
│   ├── config.py           # 16-company portfolio watchlist & alert threshold presets
│   ├── market_data.py      # EOD prices, volumes & 20-day rolling baseline calculation
│   ├── announcements.py    # NSE/BSE filing ingestion, categorization, & priority sorting
│   ├── intelligence.py     # Results extraction (YoY/QoQ) & executive background enrichment
│   └── pull_research.py    # Primary-source Narrative vs Numbers engine & Screener.in resolver
│
├── static/
│   ├── index.html          # Mobile-first executive UI layout & modals
│   ├── css/style.css       # 10 themes, CSS custom properties, & responsive design
│   └── js/app.js           # Client-side state, drawer logic, audio synthesis, & auth gate
│
└── submission/
    └── AI_BUILD_HISTORY.md # AI interaction log and architecture decision record
```

---

## 6. Submission Details

* **To:** `assessment@enam.com`
* **Subject:** `ENAM - IIT screening - 2027`
* **Candidate:** Vashi Diwakar (4th Year Undergraduate, Electrical Engineering, IIT Kanpur)
