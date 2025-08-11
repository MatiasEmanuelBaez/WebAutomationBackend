from abc import ABC, abstractmethod
from typing import List
from app.schemas import Product

class BaseScraper(ABC):
    @abstractmethod
    async def scrape(self, url: str) -> List[Product]:
        pass