import os
import httpx
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def fetch_company(symbol: str) -> tuple[dict | None, str | None]:
    symbol = (symbol or "").strip().upper()
    if not symbol:
        return None, "Please eneter a stock symbol (e.g. AAPL)."
    
    url = f"{API_BASE_URL}/company/{symbol}"

    try:
        with httpx.Client(timeout = 10.0) as client:
            r = client.get(url)
        if r.status_code == 404:
            return None, f"Company '{symbol}' not found."
        r.raise_for_status()
        return r.json(), None
    except httpx.ConnectError:
        return None, f"Could not connect to backend at {API_BASE_URL}. Is FastAPI running?"
    except httpx.HTTPStatusError as e:
        return None, f"Backend error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return None, f"Unexpected error: {e}"
    
def format_money(value: float | int | None) -> str:
    if value is None:
        return "-"
    try:
        return f"${value:,.0f}"
    except Exception:
        return str(value)
    
def format_number(value: float | int | None) -> str:
    if value is None:
        return "-"
    try:
        return f"{value:,.2f}"
    except Exception:
        return str(value)
    
st.set_page_config(page_title = "Finance App", page_icon = "📈", layout = "centered")
st.title("📈 Finance App")
st.caption("Streamlit UI -> calls your FastAPI backend -> which calls FMP")

with st.sidebar:
    st.header("Settings")
    st.write("Backend URL")
    st.code(API_BASE_URL)
    st.markdown(
        "Tip: run FastAPI on `http://localhost:8000`.\n\n"
        "If you want a different URL, set `API_BASE_URL` env var."
    )
symbol = st.text_input("Enter stock symbol", value = "AAPL", max_chars = 12)
col1, col2 = st.columns ([1, 2])
with col1:
    search = st.button("Search", use_container_width = True)
with col2:
    st.write("")

if search:
    with st.spinner("Fetching company data..."):
        data, err = fetch_company(symbol)

    if err:
        st.error(err)
        st.stop()


    if data is None:
        st.error("No data returned from backend")
        st.stop()

    profile = data.get("profile") or {}
    metrics = data.get("metrics")

    company_name = profile.get("companyName") or profile.get("name") or profile.get("symbol") or symbol.upper()
    st.subheader(f"{company_name} ({profile.get('symbol', symbol.upper())})")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Price", format_number(profile.get("price")))
    k2.metric("Market Cap", format_money(profile.get("marketCap")))
    k3.metric("Sector", profile.get("sector")[:12] + "…" if profile.get("sector") else "—")
    k4.metric("Industry", profile.get("industry")[:12] + "…" if profile.get("industry") else "—")

    st.caption(
        f"**Full sector:** {profile.get('sector') or '—'}  \n"
        f"**Full industry:** {profile.get('industry') or '—'}"
    )


    with st.expander("Company details"):
        st.write(f"**Exchange:** {profile.get('exchange') or '—'}")
        st.write(f"**Country:** {profile.get('country') or '—'}")
        st.write(f"**CEO:** {profile.get('ceo') or '—'}")
        st.write(f"**Full-time employees:** {profile.get('fullTimeEmployees') or '—'}")

    st.divider()

    st.subheader("Key Metrics")

    if not metrics:
        st.info("Metrics not available for this company")
    else:
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("ROE", format_number(metrics.get("returnOnEquity")))
        m2.metric("ROA", format_number(metrics.get("returnOnAssets")))
        m3.metric("Current Ratio", format_number(metrics.get("currentRatio")))
        m4.metric("Earnings Yield", format_number(metrics.get("earningsYield")))
        m5.metric("FCF Yield", format_number(metrics.get("freeCashFlowYield")))

        with st.expander("Raw metrics JSON"):
            st.json(metrics)


    with st.expander("Raw profile JSON"):
        st.json(profile)
