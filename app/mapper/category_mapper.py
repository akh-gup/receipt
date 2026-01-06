# TODO: Move it to the db table
MERCHANT_CATEGORY_MAP = {
    "starbucks": "FOOD",
    "mcdonald": "FOOD",
    "domino": "FOOD",

    "big bazaar": "GROCERY",
    "dmart": "GROCERY",
    "reliance fresh": "GROCERY",

    "amazon": "SHOPPING",
    "flipkart": "SHOPPING",
    "myntra": "SHOPPING",

    "uber": "TRANSPORT",
    "ola": "TRANSPORT",

    "apollo pharmacy": "HEALTH",
    "pharmacy": "HEALTH"
}

KEYWORD_CATEGORY_MAP = {
    "fuel": "TRANSPORT",
    "petrol": "TRANSPORT",
    "diesel": "TRANSPORT",

    "medicine": "HEALTH",
    "tablet": "HEALTH",

    "electricity": "UTILITIES",
    "water bill": "UTILITIES"
}

def categorize_receipt(merchant: str | None, text: str) -> tuple[str, int]:
    if merchant:
        merchant_lower = merchant.lower()
        for key, category in MERCHANT_CATEGORY_MAP.items():
            if key in merchant_lower:
                return category, 90

    text_lower = text.lower()
    for key, category in KEYWORD_CATEGORY_MAP.items():
        if key in text_lower:
            return category, 60

    return "OTHER", 30