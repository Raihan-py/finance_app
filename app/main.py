from fastapi import FastAPI
from app.api.routes_company import router as company_router

app = FastAPI(title="Finance App")

app.include_router(company_router)
