import re
from typing import Optional, List

TOTAL_KEYWORDS = [
    "total",
    "grand total",
    "amount payable",
    "net amount",
    "balance due"
]

AMOUNT_REGEX = re.compile(
    r"(?:₹|rs\.?|inr)?\s*([0-9]{1,3}(?:[,][0-9]{3})*(?:\.[0-9]{1,2})?)",
    re.IGNORECASE
)

def extract_amount_from_line(line: str) -> Optional[float]:
    matches = AMOUNT_REGEX.findall(line)
    if not matches:
        return None

    # Convert all matches to floats
    values = []
    for m in matches:
        try:
            values.append(float(m.replace(",", "")))
        except ValueError:
            continue

    return max(values) if values else None


def extract_total_amount(text: str) -> Optional[float]:
    lines = text.lower().splitlines()
    candidates: List[float] = []

    for line in lines:
        if any(keyword in line for keyword in TOTAL_KEYWORDS):
            amount = extract_amount_from_line(line)
            if amount:
                candidates.append(amount)

    if candidates:
        return max(candidates)

    # Fallback: largest number in entire receipt
    all_numbers = AMOUNT_REGEX.findall(text)
    all_values = [float(n.replace(",", "")) for n in all_numbers if n]

    return max(all_values) if all_values else None