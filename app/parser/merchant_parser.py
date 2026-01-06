import re
from typing import Optional, List

BLACKLIST_KEYWORDS = [
    "invoice", "bill", "tax", "gst", "vat",
    "total", "amount", "date", "cash",
    "credit", "debit", "receipt"
]


def clean_line(line: str) -> str:
    return re.sub(r"[^A-Za-z &]", "", line).strip()


def is_likely_merchant(line: str) -> bool:
    line_lower = line.lower()
    return not any(word in line_lower for word in BLACKLIST_KEYWORDS)


def merchant_score(line: str) -> int:
    score = 0

    if line.isupper():
        score += 3

    if re.fullmatch(r"[A-Za-z &]+", line):
        score += 2

    word_count = len(line.split())
    if 2 <= word_count <= 6:
        score += 2

    if len(line) <= 40:
        score += 1

    return score


def extract_merchant_name(text: str, max_lines: int = 8) -> Optional[str]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    candidates = []

    for line in lines[:max_lines]:
        cleaned = clean_line(line)
        if not cleaned:
            continue

        if not is_likely_merchant(cleaned):
            continue

        score = merchant_score(cleaned)
        if score >= 4:
            candidates.append((score, cleaned))

    if not candidates:
        return None

    candidates.sort(reverse=True)
    return candidates[0][1]
