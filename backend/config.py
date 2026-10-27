"""
Configuration for FINN - Financial Investment Agent.
Defines mock portfolio, ad-hoc tickers, alert thresholds, and announcement categories.
"""
from typing import Dict, List, Any

# Primary Mock Portfolio (16 NSE-listed companies across diverse sectors and market caps)
PORTFOLIO_COMPANIES: List[Dict[str, str]] = [
    {"ticker": "RELIANCE.NS", "name": "Reliance Industries", "sector": "Energy / Retail / Telecom", "cap": "Large"},
    {"ticker": "TCS.NS", "name": "Tata Consultancy Services", "sector": "IT Services", "cap": "Large"},
    {"ticker": "HDFCBANK.NS", "name": "HDFC Bank", "sector": "Banking & Financial Services", "cap": "Large"},
    {"ticker": "TATAMOTORS.NS", "name": "Tata Motors", "sector": "Automobile", "cap": "Large"},
    {"ticker": "INFY.NS", "name": "Infosys", "sector": "IT Services", "cap": "Large"},
    {"ticker": "ICICIBANK.NS", "name": "ICICI Bank", "sector": "Banking", "cap": "Large"},
    {"ticker": "BHARTIARTL.NS", "name": "Bharti Airtel", "sector": "Telecom", "cap": "Large"},
    {"ticker": "ITC.NS", "name": "ITC Ltd", "sector": "FMCG / Cigarettes / Hotels", "cap": "Large"},
    {"ticker": "LT.NS", "name": "Larsen & Toubro", "sector": "Infrastructure / Capital Goods", "cap": "Large"},
    {"ticker": "TRENT.NS", "name": "Trent Ltd (Westside/Zudio)", "sector": "Retail & Fashion", "cap": "Large Growth"},
    {"ticker": "DIXON.NS", "name": "Dixon Technologies", "sector": "Electronics Manufacturing (EMS)", "cap": "Mid Growth"},
    {"ticker": "CDSL.NS", "name": "Central Depository Services", "sector": "Market Infrastructure", "cap": "Mid"},
    {"ticker": "POLYCAB.NS", "name": "Polycab India", "sector": "Wires & Cables / FMEG", "cap": "Mid"},
    {"ticker": "TATASTEEL.NS", "name": "Tata Steel", "sector": "Metals & Mining", "cap": "Cyclical Large"},
    {"ticker": "SUNPHARMA.NS", "name": "Sun Pharmaceutical", "sector": "Pharmaceuticals", "cap": "Defensive Large"},
    {"ticker": "KPITTECH.NS", "name": "KPIT Technologies", "sector": "Automotive Software / Tech", "cap": "Mid Growth"},
]

# Ad-hoc research tickers outside portfolio (proves engine generalisation)
ADHOC_COMPANIES: List[Dict[str, str]] = [
    {"ticker": "ZOMATO.NS", "name": "Zomato Ltd (Eternal)", "sector": "Consumer Internet / Quick Commerce", "cap": "Large Growth"},
    {"ticker": "HAL.NS", "name": "Hindustan Aeronautics", "sector": "Defense & Aerospace", "cap": "Large PSU"},
    {"ticker": "TITAN.NS", "name": "Titan Company", "sector": "Consumer Discretionary / Jewellery", "cap": "Large"},
    {"ticker": "MAPMYINDIA.NS", "name": "CE Info Systems (MapmyIndia)", "sector": "DeepTech / Geospatial", "cap": "Small/Mid"},
]

# Configurable Triggered Alert Thresholds
DEFAULT_THRESHOLDS = {
    "price_change_pct": 3.0,   # Absolute daily price move exceeding +/- 3.0%
    "volume_multiplier": 1.8,   # Day's volume >= 1.8x the 20-day rolling average volume
}

# Corporate Announcement Categories defined in ENAM Reference Glossary
# Grouped into Priority Tiers:
# Tier 1 (High Signal / Instant Alert): results, management_change, M&A, litigation, fund_raise, insider_trading
# Tier 2 (Material / Medium Priority): earnings_call, capex, dividend, credit_rating, bonus_split, press_release
# Tier 3 (Routine / Noise): postal_ballot, agm_egm, pledging, unclassified
ANNOUNCEMENT_TIERS = {
    "high": ["results", "management_change", "M&A", "litigation", "fund_raise", "insider_trading"],
    "medium": ["earnings_call", "capex", "dividend", "credit_rating", "bonus_split", "press_release"],
    "routine": ["postal_ballot", "agm_egm", "pledging", "unclassified"]
}

CATEGORY_DESCRIPTIONS = {
    "results": "Quarterly/annual financial results, board approvals, investor presentations",
    "M&A": "Acquisitions, mergers, demergers, joint ventures, stake purchases/sales",
    "fund_raise": "QIP, rights issues, preferential allotment, buybacks, commercial paper",
    "management_change": "Resignation, appointment, retirement of CEO, CFO, MD, or Board Directors",
    "litigation": "Lawsuits, regulatory orders, SEBI/RBI fines, forensic audits, warnings",
    "insider_trading": "Promoter or key managerial personnel buying/selling shares",
    "earnings_call": "Earnings conference call notices, audio recordings, and transcripts",
    "investor_meetings": "One-on-one or institutional investor meets",
    "credit_rating": "Crisil/ICRA rating upgrades, downgrades, or reaffirmations",
    "dividend": "Interim or final cash dividend declarations & record dates",
    "bonus_split": "Bonus issue of shares or stock splits",
    "capex": "Approval of new manufacturing plants, capacity expansions",
    "press_release": "Commercial order wins, partnerships, product launches",
    "postal_ballot": "Shareholder voting notices and scrutiny results",
    "agm_egm": "Annual or Extraordinary General Meetings notices/results",
    "pledging": "Promoter shares pledged or revoked as loan collateral",
    "unclassified": "Routine ESOP allotments, compliance certificates, secretarial filings"
}
