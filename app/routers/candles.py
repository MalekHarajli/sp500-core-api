from fastapi import APIRouter, HTTPException
from app.db import supabase

router = APIRouter(prefix="/candles", tags=["Candles"])

@router.get("/{symbol}/{timeframe}")
def get_candles(symbol: str, timeframe: str, limit: int = 500):
    valid = ["5m", "15m", "1h", "4h", "1d"]
    if timeframe not in valid:
        raise HTTPException(status_code=400, detail="Invalid timeframe")

    # Query single unified table
    table = "historical_prices"

    res = (
        supabase.table(table)
        .select("*")
        .eq("symbol", symbol.upper())
        .eq("timeframe", timeframe)
        .order("ts", desc=True)
        .limit(limit)
        .execute()
    )

    if not res.data:
        raise HTTPException(status_code=404, detail="No data found")

    # Return oldest → newest
    return res.data[::-1]
