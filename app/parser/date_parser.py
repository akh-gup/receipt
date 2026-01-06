import re
from datetime import datetime
from sqlite3 import Date
from typing import Optional, List

DATE_PATTERNS = [
    # 12/09/2024 or 12-09-24
    r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b",

    # 2024-09-12
    r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b",

    # 12 Sep 2024
    r"\b(\d{1,2})\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\s*(\d{2,4})\b",

    # Sep 12, 2024
    r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\s*(\d{1,2}),?\s*(\d{2,4})\b"
]

MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "may": 5, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "sept": 9, "oct": 10,
    "nov": 11, "dec": 12
}

DATE_KEYWORDS = ["date", "bill date", "invoice date"]


def normalize_year(year: int) -> int:
    if year < 100:
        return 2000 + year
    return year


def parse_date(match, pattern_index: int) -> Optional[datetime]:
    try:
        if pattern_index == 0:
            d, m, y = match
            return datetime(normalize_year(int(y)), int(m), int(d))

        if pattern_index == 1:
            y, m, d = match
            return datetime(int(y), int(m), int(d))

        if pattern_index == 2:
            d, mon, y = match
            return datetime(normalize_year(int(y)), MONTH_MAP[mon], int(d))

        if pattern_index == 3:
            mon, d, y = match
            return datetime(normalize_year(int(y)), MONTH_MAP[mon], int(d))

    except Exception:
        return None


def extract_dates_from_text(text: str) -> List[datetime]:
    dates = []

    for idx, pattern in enumerate(DATE_PATTERNS):
        for match in re.findall(pattern, text, re.IGNORECASE):
            parsed = parse_date(match, idx)
            if parsed:
                dates.append(parsed)

    return dates


def extract_transaction_date(text: str) -> Optional[Date]:
    today = datetime.today()
    lines = text.lower().splitlines()
    prioritized: List[datetime] = []
    fallback: List[datetime] = []

    for line in lines:
        dates = extract_dates_from_text(line)
        if not dates:
            continue

        if any(k in line for k in DATE_KEYWORDS):
            prioritized.extend(dates)
        else:
            fallback.extend(dates)

    candidates = prioritized or fallback

    # Remove future dates
    candidates = [d for d in candidates if d <= today]

    if not candidates:
        return None

    # Earliest date is usually transaction date
    best = min(candidates)
    return datetime.strptime(best.strftime("%Y-%m-%d"), "%Y-%m-%d").date()
