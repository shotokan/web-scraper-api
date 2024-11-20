from fastapi import FastAPI
from app.api.v1.routes import router

app = FastAPI(title="Jumbo Scraper API", version="1.0.0")

# Incluir rutas
app.include_router(router, prefix="/api/v1", tags=["Scraping"])