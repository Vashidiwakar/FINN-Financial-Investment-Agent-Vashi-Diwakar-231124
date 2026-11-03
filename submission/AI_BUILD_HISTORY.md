# AI Build History & Agent Log: FINN
### ENAM Holdings AI Engineer Build Challenge (2027 Screening)

* **Candidate:** Vashi Diwakar (4th Year Undergraduate, Electrical Engineering, IIT Kanpur)
* **Live Deployed Prototype:** https://finn-financial-investment-agent.onrender.com
* **GitHub Repository:** https://github.com/Vashidiwakar/FINN-Financial-Investment-Agent-Vashi-Diwakar-231124

---

This document records the architectural discussions, prompt iterations, and engineering decisions executed during the development of **FINN**.

---

### Step 1: Requirements Dissection & Philosophy
* **Input Brief:** ENAM Holdings - AI Engineer Build Challenge (FINN: Financial Investment Agent).
* **Guiding Core Principles Extracted:**
  1. *Thin-but-working beats broad-but-broken:* A polished implementation of the windowed digest, triggered alerts, and the Narrative vs Numbers concall reconciliation proves technical depth far better than a buggy implementation of 10 modules.
  2. *Primary Sources Only:* Prohibited broker notes, news sentiment, or LLM hallucinated memories on the Pull side. Grounded exclusively in Annual Reports and Concall Transcripts.
  3. *Cost & Efficiency:* Used lightweight classification heuristics and deterministic routing for bulk parsing; reserved LLM reasoning for high-value synthesis.

---

### Step 2: Architecture & Data Plumbing Iterations
* **Challenge:** How to ensure reliable, zero-downtime demonstration of Indian market data (NSE/BSE) without depending on flaky third-party scrapers during review?
* **Decision:**
  * Use `yfinance` for live EOD metrics (`.NS` tickers) and compute a 20-day rolling baseline to catch volume surges $> 1.8\times$ or price moves $> \pm 3.0\%$.
  * Implement an in-memory resilient fallback cache containing realistic benchmark metrics for all 16 portfolio stocks + ad-hoc candidates so the application is immune to API rate limits or network hiccups during live screening.

---

### Step 3: Push Mode Implementation (The Wire & Triggered Alerts)
* **Categorization Engine:** Mapped exchange disclosures into the 16 exact categories defined in ENAM's Reference Glossary (`results`, `M&A`, `management_change`, `capex`, `litigation`, etc.).
* **Noise Suppression:** Built a two-tier presentation model:
  * High-signal items are displayed prominently with custom enrichment.
  * Routine paperwork (e.g., Reg 74 compliance, ESOPs) is grouped into a collapsible drawer.
* **Smart Enrichment:**
  * Built headline 4-metric extraction for Quarterly Results (Revenue, EBITDA, PBT, PAT with YoY/QoQ badges).
  * Built Executive Background Enrichment for leadership changes (prior role, education, LinkedIn credential badge).

---

### Step 4: Pull Mode Implementation (Narrative vs. Numbers)
* Grounded in actual Indian company concall transcripts (Tata Motors, Trent, Zomato).
* Formatted into a 4-quarter scorecard comparing management guidance against audited figures delivered, culminating in a Management Credibility Score (0-100) and Cash Conversion verification ($\text{CFO} / \text{PAT}$).
* Generalised the engine so arbitrary tickers (e.g. `TITAN.NS`, `MAPMYINDIA.NS`, `HAL.NS`) can be queried dynamically.

---

### Step 5: Advanced Investor Workflows
* **60-Second Audio Voice Dispatch:** Synthesizes pre-market audio briefings of overnight high-conviction events with variable playback speed controls (`0.8x`, `1.0x`, `1.2x`, `1.5x`, `2.0x`) for commute briefings.
* **Interactive FINN Copilot Drawer:** Slide-up bottom sheet answering ad-hoc analyst queries strictly with primary citations.
* **1-Click WhatsApp / Telegram Committee Memo:** Formats the 24-hour digest into ready-to-copy institutional committee memos with clean typography and no emojis.
* **Inline SVG Sparklines:** Real-time 20-day price trend lines embedded inside stock cards and alert rows.

---

### Step 6: 10-Theme Analyst Palette Architecture
* Created a CSS custom properties variable architecture supporting 10 distinct institutional color palettes:
  1. *Midnight Dark* (Default modern dark)
  2. *Nordic Light* (Clean high-contrast daytime paper)
  3. *Bloomberg Amber* (Classic institutional financial terminal)
  4. *Emerald Quant* (Mint/green quantitative analytics)
  5. *Cyberpunk Neon* (High-energy neon accents)
  6. *Hacker Matrix* (Monochrome retro CRT console)
  7. *Solarized Dark* (Precision teal-cyan workstation palette)
  8. *FT Paper* (Warm Financial Times salmon newsprint)
  9. *Dracula Pro* (Purple/violet modern developer theme)
  10. *Oceanic Navy* (Deep oceanic blue with cyan accents)
* Applied styling directly to theme buttons so each chip showcases its own palette.

---

### Step 7: Primary Document Plumbing & Canonical Screener.in Routing
* Resolved edge-case 404s caused by corporate restructuring in third-party databases:
  * Mapped Tata Motors to its official BSE scrip code (`500570`) to resolve concall transcripts and annual reports post-demerger.
  * Mapped Zomato to its official corporate listing slug (`ETERNAL`).
  * Created helper functions (`getScreenerCompanyUrl`, `getScreenerDocsUrl`, `getScreenerConcallsUrl`) guaranteeing working links for any queried NSE company.

---

### Step 8: Client-Side Security & Authentication Gate
* Designed a clean institutional authentication gate with Sign In and Create Account modes.
* Enforced client-side RFC email format validation (rejecting malformed emails) and minimum 6-character password security.
* Pre-seeded evaluator credentials (`example@example.com` / `password123` for Vashi Diwakar • IIT Kanpur).
* Added custom SVG password visibility toggles with clean state management.

---

### Step 9: Browser Shadow DOM Conflict Resolution
* Diagnosed visual artifact on Windows Chromium/Edge where Microsoft Edge's native password reveal icon (`::-ms-reveal`) overlapped our custom toggle button.
* Resolved by disabling `::-ms-reveal` and `::-ms-clear` in `style.css` via `display: none !important;` and setting `z-index: 5` on the custom vector SVG button.

---

### Step 10: Production Cloud Deployment (Render.com)
* Added production deployment manifests: `Procfile`, `render.yaml`, and `vercel.json`.
* Configured Uvicorn ASGI binding to dynamically listen on `0.0.0.0:$PORT`.
* Deployed 24/7 live prototype on Render: **https://finn-financial-investment-agent.onrender.com**.
* Verified live endpoints: `/api/health` returns HTTP 200, root `/` returns 200 with full mobile terminal.
