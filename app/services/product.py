from typing import List

from pydantic import HttpUrl
from app.domain.models.product import Product
from app.core.config import settings
from app.scrapper.tiendas_jumbo import JumboScraper
from app.core.logger import app_logger


class ProductService:
    @staticmethod
    async def fetch_products_from_url(product_request: HttpUrl) -> List[Product]:
        """
        Fetches a list of products from a given URL by scraping the page.

        This method initializes a scraper for the provided URL and fetches a specified number of products
        from the page. If the URL does not start with the required base URL, it raises a ValueError.
        It then returns a list of `Product` objects based on the scraped data.

        Args:
            product_request (HttpUrl): The URL from which to scrape the products, along with an optional
                                        number of products to fetch.

        Returns:
            List[Product]: A list of `Product` objects containing details of the scraped products.

        Raises:
            ValueError: If the provided URL does not start with the expected base URL.

        Example:
            products = await fetch_products_from_url(HttpUrl("https://example.com/products", num_products=10))
        """
        url_str = str(product_request.url)
        num_products = (
            product_request.num_products
            if product_request.num_products is not None
            else 15
        )
        if not url_str.startswith(settings.BASE_URL):
            raise ValueError(f"La URL debe comenzar con {settings.BASE_URL}")
        scraper = JumboScraper(url_str)
        try:
            products = await scraper.run(num_products)
        except Exception as e:
            app_logger.error(
                f"[ProductService] An unexpected error occurred: {str(e)}",
                exc_info=True,
            )

        return products
