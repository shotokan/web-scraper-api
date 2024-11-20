from fastapi import APIRouter, HTTPException
from app.api.v1.dtos.product import ProductRequest, ProductsResponse
from app.core.logger import app_logger
from app.services.product import ProductService

router = APIRouter()


@router.post("/scrape", response_model=ProductsResponse)
async def scrape_products(request: ProductRequest):
    try:
        app_logger.info(f"scraping: {request}")
        products = await ProductService.fetch_products_from_url(request)
        return {
            "url": str(request.url),
            "products": [product.model_dump() for product in products],
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")