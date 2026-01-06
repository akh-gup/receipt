from app.models.receipt import Receipt

SORT_FIELD_MAP = {
    "date": Receipt.receipt_date,
    "amount": Receipt.amount_total,
    "created_at": Receipt.created_at,
}