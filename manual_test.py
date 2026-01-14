from app.services.fmp_client import (
    get_company_profile,
    get_company_metrics,
)

print("=== VALID SYMBOL (AAPL) ===")
profile = get_company_profile("AAPL")
metrics = get_company_metrics("AAPL")

print("Profile:")
print(profile)
print()

print("Metrics:")
print(metrics)
print()


print("=== INVALID SYMBOL (ZZZZZZ) ===")
profile_none = get_company_profile("ZZZZZZ")
metrics_none = get_company_metrics("ZZZZZZ")

print("Profile (should be None):")
print(profile_none)
print()

print("Metrics (should be None):")
print(metrics_none)
