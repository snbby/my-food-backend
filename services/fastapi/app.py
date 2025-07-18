from typing import List, Optional

from db import get_session
from fastapi import Depends, FastAPI, Query
from models import FoodProduct
from pagination import PaginationParams
from sqlmodel import select

app = FastAPI()

@app.get('/api/foodproducts/search/', response_model=List[FoodProduct])
def get_products(
    q: Optional[str] = Query(None),
    pagination: PaginationParams = Depends(),
    session=Depends(get_session)
):
    statement = select(FoodProduct)

    if q:
        statement = statement.where(FoodProduct.product_name.ilike(f'%{q}%'))

    statement = statement.offset(pagination.offset).limit(pagination.limit)
    results = session.exec(statement).all()
    return results