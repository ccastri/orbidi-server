from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class LocationBase(BaseModel):
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    class Config:
        from_attributes = True

class LocationUpdate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True
class CategoryUpdate(BaseModel):
    name: Optional[str] = None

    
class LocationCategoryReviewBase(BaseModel):
    location_id: int
    category_id: int

class LocationCategoryReviewCreate(LocationCategoryReviewBase):
    pass

class LocationCategoryReview(LocationCategoryReviewBase):
    id: int
    last_reviewed: datetime
    class Config:
        from_attributes = True
