import asyncio
import re
from typing import List
from playwright.async_api import async_playwright, ElementHandle
from app.core.logger import app_logger

from app.domain.models.product import Product

price_pattern = r"\d+\.\d+"


class JumboScraper:
    def __init__(self, url: str):
        """Constructor que inicializa la URL para el scraping."""
        self.url = url
        self.browser = None
        self.page = None

    async def start_browser(self):
        p = await async_playwright().start()
        self.browser = await p.chromium.launch(headless=True)
        self.page = await self.browser.new_page()

    async def wait_section_container(self):
        await self.page.wait_for_selector("#gallery-layout-container > div > section")

    async def scroll_down(self, times=2, sleep=1):
        for _ in range(times):
            await self.page.evaluate("window.scrollBy(0, window.innerHeight)")
            await asyncio.sleep(sleep)

    async def close(self):
        if self.browser:
            await self.browser.close()

    async def get_pages(self) -> List[ElementHandle]:
        pag_selector = "div.vtex-flex-layout-0-x-flexRow.vtex-flex-layout-0-x-flexRow--result-content > div > div:nth-child(3) > div > div > div.pr0.items-stretch.flex-grow-1.flex > div > div > div:nth-child(3) > div > div > div > div.w-60.justify-center.flex > div.overflow-hidden.h-100 > ul > li"
        pagination = await self.page.query_selector_all(pag_selector)
        app_logger.info(f"[JumboScraper] pages number {len(pagination)}")

        return pagination

    async def refresh_page(self):
        """
        Refreshes the page by scrolling and waiting for the page to load the necessary content.

        This method performs a scroll action on the page and waits for a response from the server
        (specifically a GraphQL request). It will wait for specific elements to appear, and if the
        page refreshes successfully, it logs a success message. Otherwise, it logs an error.

        The method scrolls down the page, waits for the page to refresh, and waits for a gallery
        section to be visible before scrolling again.

        If the response from the server is successful, it logs that the page was refreshed.
        Otherwise, an error is logged.

        Example:
            await scraper.refresh_page()
        """
        try:
            async with self.page.expect_response("**/graphql/v1") as response_info:
                await self.page.evaluate("window.scrollBy(0, window.innerHeight)")
            response = await response_info.value
            if response.ok:
                app_logger.info("[JumboScraper] page refreshed")

                await self.page.wait_for_selector(
                    "#gallery-layout-container > div > section", timeout=10000
                )
                await self.scroll_down(3)
            else:
                app_logger.error("[JumboScraper] page could not be refreshed")
        except Exception as e:
            app_logger.error(
                f"[JumboScraper] An unexpected error occurred: {str(e)}", exc_info=True
            )
            raise

    async def get_products_section(self) -> List[ElementHandle]:
        return await self.page.query_selector_all(
            "#gallery-layout-container > div > section"
        )

    async def get_price(self, price_element: ElementHandle) -> float:
        price = 0.0
        if price_element is not None:
            div_text = await price_element.inner_text()
            result = re.search(price_pattern, div_text)
            if result:
                price = float(result.group())
        return price

    async def get_product_data(self, product_element: ElementHandle) -> dict:
        """
        Extracts product data (name, price, and promotional price) from a product element.

        This method queries the product element for its price, promotional price, and name.
        It returns the extracted information in a dictionary format.

        Args:
            product_element (ElementHandle): The Playwright element handle representing a single product.

        Returns:
            dict: A dictionary containing the product's name, price, and promotional price.

        Example:
            product_data = await scraper.get_product_data(product_element)
        """
        price_element = await product_element.query_selector("#items-price > div > div")
        promo_element = await product_element.query_selector(
            "div.tiendasjumboqaio-jumbo-minicart-2-x-primePromotionsContent.tiendasjumboqaio-jumbo-minicart-2-x-primePromotionsContent--product-prime > div > div > div"
        )
        product_name_element = await product_element.query_selector(
            "div > div:nth-child(9) > div > h3 > span"
        )
        return {
            "price": f"$ {await self.get_price(price_element)}",
            "promo_price": f"$ {await self.get_price(promo_element)}",
            "name": await product_name_element.inner_text(),
        }

    async def go_to_url(self, url: str):
        app_logger.info(f"[JumboScraper] opening {url}")
        await self.page.goto(url)

    async def run(self, num_products):
        """
        Method to scrape products from the provided URL.

        This method initializes the browser, navigates to the product page, and extracts product information.
        It handles pagination and scrolling to ensure all desired products are retrieved.

        Args:
            num_products (int): The number of products to scrape.

        Returns:
            List[Product]: A list of `Product` objects containing the scraped product data.

        Logs:
            - Information about starting the scraper, clicking pages, and the total number of products scraped.

        Steps:
            1. Start the browser asynchronously.
            2. Navigate to the product page.
            3. Wait for the product section to load.
            4. Scroll down to load more products.
            5. Iterate through the pagination and extract product data.
            6. Break the loop once the specified number of products is reached.
            7. Close the browser when done.

        Example:
            products = await scraper.run(50)
        """
        try:
            app_logger.info("[JumboScraper] running scraper")
            total_products = 0
            products = []

            await self.start_browser()
            await self.go_to_url(self.url)

            await self.wait_section_container()
            await self.scroll_down(4)

            pagination = await self.get_pages()
            for page_number, pagination_page in enumerate(pagination, start=1):
                app_logger.info(
                    f"[JumboScraper] extracting data from page {page_number}..."
                )
                if page_number != 1 and page_number > 1:
                    app_logger.info(
                        f"[JumboScraper] clicking next page {page_number}..."
                    )
                    await self.page.click(
                        f"ul.vtex-slider-0-x-sliderFrame li:nth-child({page_number}) button"
                    )
                    await self.refresh_page()

                productos = await self.get_products_section()
                for _, producto in enumerate(productos, start=1):
                    product_data = await self.get_product_data(producto)
                    products.append(Product(**product_data))
                    total_products += 1
                    if total_products == num_products:
                        break

                if total_products == num_products:
                    break

            await self.close()
            app_logger.info(f"[JumboScraper] total products fetched {total_products}")

            return products
        except Exception as e:
            app_logger.error(
                f"[JumboScraper] An unexpected error occurred: {str(e)}", exc_info=True
            )
            raise
