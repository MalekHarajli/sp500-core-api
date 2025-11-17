from fastapi import APIRouter, HTTPException
from app.db import supabase

router = APIRouter(prefix="/candles", tags=["Candles"])

@router.get("/{symbol}/{timeframe}")
def get_candles(symbol: str, timeframe: str, limit: int = 500):
    valid = ["5m", "15m", "1h", "4h", "1d"]
    if timeframe not in valid:
        raise HTTPException(status_code=400, detail="Invalid timeframe")

    table_map = {
        "5m": "minute_ohlc_5m",
        "15m": "minute_ohlc_15m",
        "1h": "minute_ohlc_1h",
        "4h": "minute_ohlc_4h",
        "1d": "minute_ohlc_1d"
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

    return res.data[::-1] if res.data else []
