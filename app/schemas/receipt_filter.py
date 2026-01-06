from pydantic import BaseModel
from datetime import date
from typing import Optional, Literal

class ReceiptFilter(BaseModel):
    # Filter
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category: Optional[str] = None
    merchant: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    q: Optional[str] = None

    # Pagination
    limit: int = 20
    offset: int = 0

    # Sorting
    sort_by: Literal["date", "amount", "created_at"] = "date"
    order: Literal["asc", "desc"] = "desc"