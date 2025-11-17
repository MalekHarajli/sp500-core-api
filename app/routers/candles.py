from fastapi import APIRouter, HTTPException
from app.db import supabase

router = APIRouter(prefix="/candles", tags=["Candles"])

@router.get("/{symbol}/{timeframe}")
def get_candles(symbol: str, timeframe: str, limit: int = 500):
    valid = ["1m", "5m", "15m", "1h", "4h", "1d"]
    if timeframe not in valid:
        raise HTTPException(status_code=400, detail="Invalid timeframe")

    table_map = {
        "1m": "minute_ohlc",
        "5m": "ohlc_5m",
        "15m": "ohlc_15m",
        "1h": "ohlc_1h",
        "4h": "ohlc_4h",
        "1d": "ohlc_1d"
    }

    table = table_map[timeframe]

    res = (
        supabase.table(table)
        .select("*")
        .eq("symbol", symbol.upper())
        .order("ts_bucket", desc=True)
        .limit(limit)
        .execute()
    )
    
    return res.data[::-1]  # Optional → earliest first
