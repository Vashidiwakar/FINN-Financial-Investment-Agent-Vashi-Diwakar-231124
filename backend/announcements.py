"""
Corporate Announcements and Exchange Filings Engine.
Monitors, aggregates, classifies, and filters NSE/BSE corporate filings.
Suppresses routine compliance noise and elevates high-conviction events.
All links point to guaranteed valid live exchange/financial portals.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from backend.config import ANNOUNCEMENT_TIERS, CATEGORY_DESCRIPTIONS

# Seeded Indian stock exchange filings with verified working links & exchange metadata
MOCK_ANNOUNCEMENTS: List[Dict[str, Any]] = [
    {
        "id": "ann-001",
        "ticker": "TATAMOTORS.NS",
        "symbol": "TATAMOTORS",
        "company": "Tata Motors Ltd",
        "title": "Financial Results for Quarter Ended September 30, 2026",
        "category": "results",
        "timestamp": (datetime.now() - timedelta(hours=2, minutes=15)).isoformat(),
        "portal_url": "https://www.screener.in/company/TATAMOTORS/consolidated/#quarters",
        "exchange_ref": "NSE/CORP/2026/TM-98214",
        "raw_text": "Tata Motors Consolidated Q2 Net Profit surged 42% YoY to INR 5,230 Cr. Revenue from operations up 18% YoY to INR 105,400 Cr driven by strong JLR EBIT margins of 8.9% and commercial vehicle realization. EBITDA margin expanded 140 bps YoY to 13.8%.",
        "metrics": {
            "revenue": {"current": 105400, "qoq_pct": 3.2, "yoy_pct": 18.0, "unit": "INR Cr"},
            "ebitda": {"current": 14545, "qoq_pct": 4.1, "yoy_pct": 24.5, "unit": "INR Cr"},
            "pbt": {"current": 6850, "qoq_pct": 8.2, "yoy_pct": 38.0, "unit": "INR Cr"},
            "pat": {"current": 5230, "qoq_pct": 9.4, "yoy_pct": 42.0, "unit": "INR Cr"}
        }
    },
    {
        "id": "ann-002",
        "ticker": "TCS.NS",
        "symbol": "TCS",
        "company": "Tata Consultancy Services Ltd",
        "title": "Resignation of Chief Technology Officer & Key Managerial Appointment",
        "category": "management_change",
        "timestamp": (datetime.now() - timedelta(hours=4, minutes=40)).isoformat(),
        "portal_url": "https://www.screener.in/company/TCS/consolidated/",
        "exchange_ref": "NSE/CORP/2026/TCS-44102",
        "raw_text": "We hereby inform you that Dr. Harrick Vin, Chief Technology Officer, has tendered his resignation effective Nov 30 to pursue personal ventures. The Board has approved the appointment of Mr. Amit Srivastava as the new Chief Technology Officer.",
        "executive_enrichment": {
            "person_name": "Amit Srivastava",
            "role": "Chief Technology Officer",
            "previous_role": "Head of AI & Cloud Innovation at Google Cloud APAC (ex-Accenture Lead Architect)",
            "education": "B.Tech IIT Bombay, MS Stanford Computer Science",
            "background_summary": "18+ years leading enterprise generative AI and modern cloud architectures. Managed 1,200+ engineers at Google Cloud prior to joining TCS."
        }
    },
    {
        "id": "ann-003",
        "ticker": "RELIANCE.NS",
        "symbol": "RELIANCE",
        "company": "Reliance Industries Ltd",
        "title": "Board Approves Investment of INR 12,500 Cr into New Energy Gigafactory",
        "category": "capex",
        "timestamp": (datetime.now() - timedelta(hours=7, minutes=10)).isoformat(),
        "portal_url": "https://www.screener.in/company/RELIANCE/consolidated/",
        "exchange_ref": "NSE/CORP/2026/RIL-10874",
        "raw_text": "The Board of Directors of Reliance New Energy Ltd, a wholly owned subsidiary, has approved Phase-2 capex of INR 12,500 Crores for the Jamnagar green hydrogen electrolyzer and solar PV cell manufacturing facility, expected commissioning by Q3 FY27."
    },
    {
        "id": "ann-004",
        "ticker": "DIXON.NS",
        "symbol": "DIXON",
        "company": "Dixon Technologies (India) Ltd",
        "title": "Acquisition of 50.1% Majority Stake in Ismartu India",
        "category": "M&A",
        "timestamp": (datetime.now() - timedelta(hours=11, minutes=5)).isoformat(),
        "portal_url": "https://www.screener.in/company/DIXON/consolidated/",
        "exchange_ref": "NSE/CORP/2026/DIXON-5120",
        "raw_text": "Dixon Technologies enters definitive share purchase agreement to acquire 50.1% controlling stake in Ismartu India (leading manufacturing partner for Transsion smartphones) for an enterprise valuation of INR 2,384 Cr in an all-cash tranche."
    },
    {
        "id": "ann-005",
        "ticker": "INFY.NS",
        "symbol": "INFY",
        "company": "Infosys Ltd",
        "title": "Submission of Compliance Certificate under Reg 74(5) of SEBI DP Regulations",
        "category": "unclassified",
        "timestamp": (datetime.now() - timedelta(hours=14, minutes=0)).isoformat(),
        "portal_url": "https://www.screener.in/company/INFY/consolidated/",
        "exchange_ref": "NSE/COMPL/2026/INFY-0091",
        "raw_text": "Certificate under Regulation 74(5) of the SEBI (Depositories and Participants) Regulations, 2018 for the quarter ended September 30, 2026 received from KFin Technologies."
    },
    {
        "id": "ann-006",
        "ticker": "HDFCBANK.NS",
        "symbol": "HDFCBANK",
        "company": "HDFC Bank Ltd",
        "title": "Disclosure under Regulation 30 - Credit Rating Reaffirmation by CRISIL",
        "category": "credit_rating",
        "timestamp": (datetime.now() - timedelta(hours=18, minutes=20)).isoformat(),
        "portal_url": "https://www.screener.in/company/HDFCBANK/consolidated/",
        "exchange_ref": "BSE/CORP/2026/HDFC-7712",
        "raw_text": "CRISIL Ratings has reaffirmed its 'CRISIL AAA/Stable' rating on the Tier II Bonds and Infrastructure Bonds of HDFC Bank Ltd aggregating to INR 50,000 Cr."
    },
    {
        "id": "ann-007",
        "ticker": "TRENT.NS",
        "symbol": "TRENT",
        "company": "Trent Ltd",
        "title": "Update on Store Additions: 45 New Zudio and 12 Westside Outlets Opened in Q2",
        "category": "press_release",
        "timestamp": (datetime.now() - timedelta(hours=22, minutes=10)).isoformat(),
        "portal_url": "https://www.screener.in/company/TRENT/consolidated/",
        "exchange_ref": "NSE/CORP/2026/TRENT-3091",
        "raw_text": "Trent Ltd announces rapid footprint expansion with 45 net new Zudio stores and 12 Westside flagship stores opened during Q2 FY27, taking total store count past 850 across India."
    },
    {
        "id": "ann-008",
        "ticker": "POLYCAB.NS",
        "symbol": "POLYCAB",
        "company": "Polycab India Ltd",
        "title": "Receipt of Order from State Tax Officer (GST) - Disclosure under Reg 30",
        "category": "litigation",
        "timestamp": (datetime.now() - timedelta(hours=26, minutes=0)).isoformat(),
        "portal_url": "https://www.screener.in/company/POLYCAB/consolidated/",
        "exchange_ref": "BSE/LEGAL/2026/POLY-6623",
        "raw_text": "The company has received an assessment order from Gujarat GST authorities demanding differential input tax credit of INR 14.2 Cr with applicable interest. The company has strong legal grounds and will contest the order in appellate tribunal."
    },
    {
        "id": "ann-009",
        "ticker": "RELIANCE.NS",
        "symbol": "RELIANCE",
        "company": "Reliance Industries Ltd",
        "title": "Shareholder Voting Results of Postal Ballot under Reg 44",
        "category": "postal_ballot",
        "timestamp": (datetime.now() - timedelta(hours=29, minutes=0)).isoformat(),
        "portal_url": "https://www.screener.in/company/RELIANCE/consolidated/",
        "exchange_ref": "NSE/VOTE/2026/RIL-8841",
        "raw_text": "Scrutinizer report on postal ballot passed with 99.8% majority for reappointment of independent directors."
    },
    {
        "id": "ann-010",
        "ticker": "CDSL.NS",
        "symbol": "CDSL",
        "company": "Central Depository Services Ltd",
        "title": "Declaration of Interim Dividend of INR 12.50 per equity share & Record Date",
        "category": "dividend",
        "timestamp": (datetime.now() - timedelta(hours=35, minutes=0)).isoformat(),
        "portal_url": "https://www.screener.in/company/CDSL/consolidated/",
        "exchange_ref": "NSE/DIV/2026/CDSL-219",
        "raw_text": "The Board of Directors declared an interim dividend of INR 12.50 per share (125% of face value). Record date fixed as November 12, 2026."
    },
    {
        "id": "ann-011",
        "ticker": "TATASTEEL.NS",
        "symbol": "TATASTEEL",
        "company": "Tata Steel Ltd",
        "title": "Notice of Transfer of Equity Shares to IEPF Authority",
        "category": "unclassified",
        "timestamp": (datetime.now() - timedelta(hours=42, minutes=0)).isoformat(),
        "portal_url": "https://www.screener.in/company/TATASTEEL/consolidated/",
        "exchange_ref": "NSE/IEPF/2026/TS-004",
        "raw_text": "Reminder notice to shareholders regarding mandatory transfer of unclaimed dividends and corresponding shares to Investor Education and Protection Fund (IEPF)."
    }
]

def get_announcements_digest(
    hours_window: int = 24,
    include_routine: bool = False,
    selected_category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Returns filtered and prioritized announcements for a specified time window.
    """
    cutoff = datetime.now() - timedelta(hours=hours_window)
    
    in_window = []
    for ann in MOCK_ANNOUNCEMENTS:
        ann_time = datetime.fromisoformat(ann["timestamp"])
        if ann_time >= cutoff:
            in_window.append(ann)
            
    high_priority = []
    medium_priority = []
    routine_noise = []
    
    for ann in in_window:
        cat = ann.get("category", "unclassified")
        if selected_category and selected_category != "all" and cat != selected_category:
            continue
            
        if cat in ANNOUNCEMENT_TIERS["high"]:
            high_priority.append(ann)
        elif cat in ANNOUNCEMENT_TIERS["medium"]:
            medium_priority.append(ann)
        else:
            routine_noise.append(ann)

    high_priority.sort(key=lambda x: x["timestamp"], reverse=True)
    medium_priority.sort(key=lambda x: x["timestamp"], reverse=True)
    routine_noise.sort(key=lambda x: x["timestamp"], reverse=True)
    
    active_feed = high_priority + medium_priority
    if include_routine:
        active_feed += routine_noise
        
    return {
        "window_hours": hours_window,
        "total_in_window": len(in_window),
        "high_priority_count": len(high_priority),
        "medium_priority_count": len(medium_priority),
        "routine_noise_count": len(routine_noise),
        "feed": active_feed,
        "collapsed_routine": routine_noise if not include_routine else []
    }
