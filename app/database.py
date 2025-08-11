from sqlalchemy import Table, Column, String, Integer, Numeric, DateTime, MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from databases import Database

import os

metadata = MetaData()

products = Table(
    "products",
    metadata,
    Column("product_id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("price", Numeric(10, 2)),
    Column("description", String),
    Column("image_url", String),
    Column("task_id", String),
)

tasks = Table(
    "tasks",
    metadata,
    Column("task_id", String, unique=True),
    Column("status", String),
    Column("started_at", DateTime),
    Column("finished_at", DateTime, nullable=True),
    Column("error", String, nullable=True),
)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@db:5432/scraperdb")

database = Database(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)
