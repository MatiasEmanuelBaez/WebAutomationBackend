from typing import List
import asyncio
from typing import Optional
from app.schemas import Product, Tasks
from uuid import uuid4
from datetime import datetime
from app.scrapers.saucedemo import Scraper as saucedemoScraper
from app.scrapers.practicesoftwaretesting import Scraper as practicesoftwaretestingScraper
from app.database import database, products, tasks

SCRAPERS = {
    "saucedemo": saucedemoScraper,
    "practicesoftwaretesting": practicesoftwaretestingScraper,
}



async def run_scraper(scraper_name: str, product_name: Optional[str] = None) -> str:
    auto_id = str(uuid4())
    
    scraper_cls = SCRAPERS.get(scraper_name)
    if not scraper_cls:
        raise ValueError(f"Scraper {scraper_name} no encontrado")

    if not database.is_connected:
        await database.connect()
    
    insert_task_query = tasks.insert().values(
        task_id=auto_id,
        status="in_progress",
        started_at = datetime.utcnow())
    
    await database.execute(insert_task_query)
    asyncio.create_task(_run_scraper_task(auto_id, scraper_cls, product_name))
    return auto_id



async def _run_scraper_task(auto_id, scraper_cls, product_name: Optional[str] = None):
    try:
        async with database.transaction():
            scraper = scraper_cls(auto_id)
            products_list = await scraper.scrape()
            
            if products_list:
                
                if product_name:
                    products_list = [p for p in products_list if product_name.lower() in p.name.lower()]
                
                if products_list:
                    query = products.insert()
                    values = [p.dict() for p in products_list]
                    await database.execute_many(query=query, values=values)

        update_task_query = tasks.update().where(tasks.c.task_id == auto_id).values(
            status="completed",
            finished_at=datetime.utcnow(),
            error=None)
        await database.execute(update_task_query)

    except Exception as e:
        update_task_query = tasks.update().where(tasks.c.task_id == auto_id).values(
            status="error",
            finished_at=datetime.utcnow(),
            error=str(e))
        await database.execute(update_task_query)



async def get_task_status(task_id: int):
    if not database.is_connected:
        await database.connect()

    query = tasks.select().where(tasks.c.task_id == task_id)
    row = await database.fetch_one(query)

    if row is None:
        return None 
    return dict(row)



async def get_products_by_task(task_id: str) -> List[Product]:
    if not database.is_connected:
        await database.connect()

    query = products.select().where(products.c.task_id == task_id)
    rows = await database.fetch_all(query)

    return [Product(**row) for row in rows]