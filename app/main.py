from fastapi import FastAPI, HTTPException
from typing import Optional
from typing import List
from uuid import uuid4
from fastapi import BackgroundTasks
from app.schemas import Product, Tasks
from app.services.scraper_service import run_scraper, get_task_status, get_products_by_task
from app.database import database, engine, metadata

app = FastAPI()

AVAILABLE_SCRAPERS = [
    "saucedemo", 
    "practicesoftwaretesting",
    
    ]



@app.on_event("startup")
async def startup():
    await database.connect()
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)



@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



@app.post("/tasks")
async def create_task(scraper_name: str, product_name: Optional[str] = None):
    try:
        task_id = await run_scraper(scraper_name, product_name)
        return {"task_id": task_id, "message": "Scraper iniciado"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar scraper: {str(e)}")



@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = await get_task_status(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    if task["status"] == "completed":
        products = await get_products_by_task(task_id)
        data = [{
            "name": p.name, 
            "price": p.price,
            "description": p.description,
            "image_url": p.image_url,
            } for p in products]
        
        return {
            "status": "completed",
            "data": data
        }
    
    return task