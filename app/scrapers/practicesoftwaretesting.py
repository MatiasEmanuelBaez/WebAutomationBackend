from typing import List
from app.schemas import Product
from decimal import Decimal
from pathlib import Path
from urllib.parse import urljoin
from app.scrapers.base import BaseScraper
from playwright.async_api import async_playwright
from urllib.parse import urlparse
import aiohttp
import uuid
import logging
import os

logging.basicConfig(level=logging.INFO)

IMAGES_DIR = Path("/app/images")



async def download_image(session: aiohttp.ClientSession, url: str, save_path: Path) -> bool:
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                content = await resp.read()
                with open(save_path, "wb") as f:
                    f.write(content)
                return True
            else:
                logging.warning(f"Falló descarga de imagen {url}: status {resp.status}")
                return False
    except Exception as e:
        logging.error(f"Error descargando imagen {url}: {e}")
        return False



class Scraper(BaseScraper):
    def __init__(self, task_id: str):
        self.task_id = task_id
        
    async def scrape(self) -> List[Product]:
        async with async_playwright() as p, aiohttp.ClientSession() as session:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            products = []
            url= "https://practicesoftwaretesting.com/"
            
            await page.goto(url)
            await page.wait_for_timeout(2000)
            
            while True:
            
                items = await page.query_selector_all("a.card[data-test^='product-']")
                
                for item in items:
                    
                    item_link = await item.get_attribute("href")
                    full_url = urljoin(page.url, item_link)

                    item_page = await browser.new_page()
                    await item_page.goto(full_url)
                    await item_page.wait_for_timeout(10000)

                    name_element = await item_page.query_selector("[data-test='product-name']")
                    price_element = await item_page.query_selector("[data-test='unit-price']")
                    price_text = (await price_element.inner_text()).strip()
                    desc_element = await item_page.query_selector("[data-test='product-description']")
                    img_element = await item_page.query_selector("img")
                    
                    name = (await name_element.inner_text()).strip()
                    price = Decimal(price_text)
                    description = (await desc_element.inner_text()).strip()
                    original_image_url = urljoin(page.url,(await img_element.get_attribute("src")).strip())
                    
                    i_parsed_url = urlparse(original_image_url)
                    image_name = os.path.basename(i_parsed_url.path)
                    i_name, i_ext = os.path.splitext(image_name)
                    i_unique_name = f"{i_name}_{uuid.uuid4().hex}{i_ext}"
                    save_path = IMAGES_DIR / i_unique_name
                    
                    success = await download_image(session, original_image_url, save_path)

                    if success:
                        image_url = f"http://localhost:8000/images/{image_name}"
                    else:
                        image_url = original_image_url
                    

                    products.append(Product(
                        name=name,
                        price=price,
                        description=description,
                        image_url=image_url,
                        task_id=self.task_id
                    ))
                    
                    await item_page.close()
                
                await page.wait_for_timeout(1000)
                next_button = page.locator('li.page-item:not(.disabled) a[aria-label="Next"]')

                if await next_button.count() == 0:
                    break

                try:
                    await next_button.click()
                    await page.wait_for_timeout(5000)
                except Exception as e:
                    logging.error(f"Error al tratar de ir a la siguiente pagina: {str(e)}")
                    break

            logging.info(f"Scraping completo, {len(products)} productos encontrados")
            await browser.close()
            return products