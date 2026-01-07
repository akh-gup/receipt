from fastapi import FastAPI
from app.routes import auth, receipts

app = FastAPI(title="Receipt Organizer POC")

# Auth routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Receipt routes
app.include_router(receipts.router, prefix="/receipts", tags=["receipts"])

@app.get("/")
def home():
    return {"message": "Receipt Organizer is running!"}