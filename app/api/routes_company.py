from app.services.fmp_client import (
    get_company_profile,
    get_company_metrics,
)
from fastapi import APIRouter, HTTPException


router = APIRouter()

@router.get("/company/{symbol}")
def get_company(symbol):
    symbol = symbol.strip().upper()

    profile = get_company_profile(symbol)

    if not profile:
        raise HTTPException(status_code = 404, detail = "Company not found")
    
    try:
        metrics = get_company_metrics(symbol)
    except Exception:
        metrics = None

    
    return {
        "profile" : profile,
        "metrics" : metrics
    }