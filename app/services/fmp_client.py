import httpx
from app.core.config import FMP_API_KEY, FMP_BASE_URL
from typing import Optional, Dict

def get_company_profile(symbol) :
    """
    fetches company profile from FMP
    Extracts only the fields you care about
    Returns one company’s data in a clean structure
    output:
        a dictionary with selected fields
        OR None if the company does not exist
    build the /stable/profile request
    add API key automatically
    make HTTP request
    parse the JSON
    Handle edge cases

    edge cases:
    empty list --> return none
    non-200 response --> raise an error
    network timeout --> raise an error

    """

    url = FMP_BASE_URL + "/stable/profile"

    params = {
      "symbol" : symbol,
      "apikey" : FMP_API_KEY,
    }

    response = httpx.get(url, params = params, timeout = 3)

    if response.status_code != 200:
        raise RuntimeError("FMP request failed")
    
    data = response.json()

    if not data:
        return None
    
    profile = data[0]

    clean_profile = {
        "symbol" : profile.get("symbol"),
        "price" : profile.get("price"),
        "marketCap" : profile.get("marketCap"),
        "exchange" : profile.get("exchange"),
        "industry"  : profile.get("industry"),
        "sector" : profile.get("sector"),
        "country" : profile.get("country"),
        "ceo" : profile.get("ceo"),
        "fullTimeEmployees" : profile.get("fullTimeEmployees"),
        "companyName" : profile.get("companyName"),
    }

    return clean_profile



def get_company_metrics(symbol):
    """
    fetches latest metrics/ratios
    returns most recent record
    outputs a dictionary of key metrics or none
    calls /stable/key-metrics
    OR calls /stable/ratios
    use llimit-1
    extreact only meaningufl metrics(i.e. P/E, ROE, margins)
    edge cases:
    empty array --> return none
    API error --> raise an error

    """

    url = FMP_BASE_URL + "/stable/key-metrics"
    params = {
        "symbol" : symbol,
        "apikey" : FMP_API_KEY,
        "limit" :  1,
    }

    response = httpx.get(url, params = params, timeout = 3)

    if response.status_code in (404, 400):
        return None
    elif response.status_code != 200:
        print(response.status_code)
        raise RuntimeError("FMP request failed")
    
    data = response.json()

    if not data:
        return None
    
    metrics = data[0]

    clean_metrics = {
        "returnOnEquity" : metrics.get("returnOnEquity"),
        "currentRatio" : metrics.get("currentRatio"),
        "returnOnAssets" : metrics.get("returnOnAssets"),
        "earningsYield" : metrics.get("earningsYield"),
        "freeCashFlowYield" : metrics.get("freeCashFlowYield"),
    }

    return clean_metrics