from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class FoodProduct(SQLModel, table=True):
    __tablename__ = 'myfood_foodproduct'

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    product_name: Optional[str] = Field(default=None)
    brands: Optional[str] = Field(default=None)
    countries: Optional[str] = Field(default=None)

    carbohydrates_100g: Optional[float] = Field(default=None)
    proteins_100g: Optional[float] = Field(default=None)
    fat_100g: Optional[float] = Field(default=None)