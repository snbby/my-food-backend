from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional, List
import os
import asyncpg
import hmac

app = FastAPI()
security = HTTPBasic()

DB_CONFIG = dict(
    host=os.getenv("MYFOOD_DATABASE_HOST", "localhost"),
    port=int(os.getenv("MYFOOD_DATABASE_PORT", "5432")),
    user=os.getenv("MYFOOD_DATABASE_USER", ""),
    password=os.getenv("MYFOOD_DATABASE_PASS", ""),
    database=os.getenv("MYFOOD_DATABASE_NAME", ""),
)

API_USER = os.getenv("FASTAPI_USER", "user")
API_PASS = os.getenv("FASTAPI_PASS", "pass")

class FoodProduct(BaseModel):
    id: int
    product_name: Optional[str] = None
    brands: Optional[str] = None
    countries: Optional[str] = None
    fat_100g: Optional[float] = None
    carbohydrates_100g: Optional[float] = None
    proteins_100g: Optional[float] = None

class FoodProductDetail(FoodProduct):
    fiber_100g: Optional[float] = None
    sugars_100g: Optional[float] = None

def get_db():
    async def _get_db():
        conn = await asyncpg.connect(**DB_CONFIG)
        try:
            yield conn
        finally:
            await conn.close()
    return _get_db

async def verify_credentials(creds: HTTPBasicCredentials = Depends(security)):
    correct_username = hmac.compare_digest(creds.username, API_USER)
    correct_password = hmac.compare_digest(creds.password, API_PASS)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.get("/foodproducts/search/", response_model=List[FoodProduct])
async def search_food_products(q: Optional[str] = None, limit: int = 100, offset: int = 0, db=Depends(get_db())):
    query = """
        SELECT id, product_name, brands, countries, fat_100g,
               carbohydrates_100g, proteins_100g
        FROM myfood_foodproduct
    """
    params = []
    if q:
        query += " WHERE product_name ILIKE $1"
        params.append(f"%{q}%")
    query += f" ORDER BY id LIMIT {limit} OFFSET {offset}"
    rows = await db.fetch(query, *params)
    return [FoodProduct(**dict(r)) for r in rows]

@app.get("/foodproducts/search_detailed/", response_model=List[FoodProductDetail])
async def search_detailed_food_products(q: Optional[str] = None, limit: int = 100, offset: int = 0, auth: bool = Depends(verify_credentials), db=Depends(get_db())):
    query = """
        SELECT id, product_name, brands, countries, fat_100g,
               carbohydrates_100g, proteins_100g, fiber_100g, sugars_100g
        FROM myfood_foodproduct
    """
    params = []
    if q:
        query += " WHERE product_name ILIKE $1"
        params.append(f"%{q}%")
    query += f" ORDER BY id LIMIT {limit} OFFSET {offset}"
    rows = await db.fetch(query, *params)
    return [FoodProductDetail(**dict(r)) for r in rows]
