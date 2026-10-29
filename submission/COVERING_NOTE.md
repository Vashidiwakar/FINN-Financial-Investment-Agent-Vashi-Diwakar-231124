# Covering Note: FINN — Financial Investment Agent (v1.1.0)

**To:** assessment@enam.com  
**Subject:** ENAM - IIT screening - 2027  
**Candidate Name:** Sachin Kumar  
**Date:** October 2026  
**Repository:** [GitHub Repository Link - Insert Your Repo URL]  
**Live Working Prototype:** [Deployed URL / Local Instructions - e.g., Render/Railway/Local]

---

### 1. What Was Built
**FINN** is a mobile-first investment intelligence agent engineered specifically for high-conviction public markets investors. Instead of aggregating more noise, FINN serves as an aggressive filter and analyst companion:

* **Push Mode (The Wire & Triggered Alerts):**
  * **Windowed Digest (24h/Custom):** Automatically aggregates corporate filings across a 16-company mock portfolio spanning large-cap leaders (Reliance, TCS, HDFC Bank, Tata Motors) and hyper-growth mid-caps (Trent, Dixon, CDSL). High-signal events (Results, M&A, Leadership Changes) are elevated to the top; routine compliance paperwork (ESOP allotments, Reg 74 certificates) is suppressed into a collapsible drawer.
  * **Triggered Anomaly Alerts:** Evaluates daily price movements against a configurable threshold (e.g., $\pm 3.0\%$) and volume surges against a 20-day rolling baseline ($> 1.8\times$ or $2.0\times$ average volume).
  * **High-Conviction Enrichment:** 
    * *Results:* Instantly extracts Revenue, EBITDA, PBT, PAT with YoY and QoQ percentage deltas.
    * *Management Changes:* Profiles incoming executives (previous employer, educational pedigree, professional background) so analysts don't need to manually check LinkedIn.
* **Pull Mode (Primary-Source Deep Dive):**
  * On-demand analysis strictly grounded in primary documents (Earnings Call transcripts and Audited Annual Reports via Screener.in / Exchange Filings).
  * **Narrative vs. Numbers Reality Check:** Takes the last 4 quarters of management guidance/commentary and systematically verifies whether management delivered on its promises (with exact transcript page citations and verdicts: `BEAT`, `DELIVERED`, `PARTIAL MISS`).
  * Computes a **Management Credibility Score** and **Cash Quality conversion check** ($\text{CFO} / \text{PAT}$ ratio to detect aggressive accounting accruals).
  * **Engine Generalisation:** Validated both on portfolio stocks and ad-hoc companies outside the portfolio (e.g., `ZOMATO.NS`, `HAL.NS`, `TITAN.NS`).

* **Novel Interaction Model Additions (Beyond Generic Dashboards):**
  * **60-Second Audio Voice Dispatch:** Pre-market audio briefing synthesizing high-conviction overnight moves, allowing fund managers to listen to their portfolio dispatch while commuting.
  * **Interactive Primary Copilot Drawer:** Ad-hoc questions (e.g. segment margins, guidance delivery) answered exclusively with primary citations.
  * **1-Click WhatsApp / Telegram Executive Memo:** Automatically generates formatted committee memos with bold headers and metrics for instant morning distribution.
  * **Inline SVG Sparklines:** Real-time 20-day price trend lines embedded directly within portfolio and alert cards.

---

### 2. Key Decisions & Architectural Trade-offs
1. **Zero "AI Slop" Rule:** Financial analysts do not read generic AI paragraphs. The UI is designed for extreme density and rapid visual parsing: metric grids for financials, badge chips for verdicts, and structured side-by-side promise-vs-delivery scorecards.
2. **Primary Data Discipline:** For the Pull research module, external secondary commentary (brokerage notes, tweets, news opinions) was strictly banned. Differentiated edge exists only in primary filings.
3. **Smart Model Routing & Cost Efficiency:** 
   * Low-tier classification and routine filing filtering are handled via lightweight deterministic rule extraction / small models to keep latency sub-second and API costs near zero.
   * Deep reasoning (Narrative vs. Numbers reconciliation) is executed via structured prompt routing.
4. **Resilient Local & Live Fallbacks:** Public exchange APIs and yfinance frequently throttle or trigger rate-limits during peak trading hours. We engineered a resilient benchmark fallback layer so that the app **never crashes or throws errors during an evaluation**.

---

### 3. What Was Deliberately Left Out
* **Unconstrained Generative Chatbot:** Open-ended chatbots hallucinate financial numbers. We anchored all chat capabilities to a specialized Primary-Source Copilot that only answers when verified citations exist.
* **Non-Essential Research Modules:** Of the 8 potential pull modules in the brief, we laser-focused on **Narrative vs. Numbers** and **Cash Quality**. Delivering these two with 100% precision and verifiable citations beats shallow implementations of all eight.

---

### 4. Where I Would Take It Next
1. **Audio Concall Scraping & Tone Analysis:** Ingest the raw audio of earnings calls to detect vocal hesitation, stress markers, or evasive language during analyst Q&A sessions.
2. **Direct Exchange Webhooks:** Hook into BSE/NSE XML feeds via real-time WebSockets for sub-second filing parsing.
3. **Automated Forensic Red-Flag Checker:** Flag sudden spikes in related-party transactions (RPTs), auditor qualifications, or promoter pledge increases across quarterly filings.
