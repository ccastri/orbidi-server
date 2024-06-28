from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
import crud
from db import get_db
# from .. import schemas, crud
# from ..db import get_db

router = APIRouter(prefix="/api/v1")

@router.get('/healthcheck')
async def healthcheck():
    try:
        print("Healthcheck endpoint called")
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")

@router.get("/locations/{location_id}", response_model=schemas.Location)
async def read_location(location_id: int, db: Session = Depends(get_db)):
    location = await crud.get_location(db=db, location_id=location_id)
    if location:
        return location
    else:
        raise HTTPException(status_code=404, detail=f"Location with id {location_id} not found")

@router.post("/locations/", response_model=schemas.Location)
async def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    return await crud.create_location(db=db, location=location)
'''

Categories

'''
@router.post("/categories/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return await crud.create_category(db=db, category=category)


'''

Recommendations

'''
@router.get("/recommendations/", response_model=List[schemas.LocationCategoryReview])
async def get_recommendations(db: Session = Depends(get_db)):
    return crud.get_unreviewed_locations(db=db)

@router.get("/recommendations/", response_model=List[schemas.LocationCategoryReview])
async def get_unreviewed_locations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    recommendations = await crud.get_recommendations(db=db, skip=skip, limit=limit)
    return recommendations

@router.post("/recommendations/", response_model=schemas.LocationCategoryReview)
async def create_recommendation(recommendation: schemas.LocationCategoryReviewCreate, db: Session = Depends(get_db)):
    db_recommendation = await crud.create_recommendation(db=db, recommendation=recommendation)
    return db_recommendation

@router.put("/recommendations/{recommendation_id}", response_model=schemas.LocationCategoryReview)
async def update_recommendation(recommendation_id: int, reviewed: bool, db: Session = Depends(get_db)):
    db_recommendation = await crud.update_recommendation(db=db, recommendation_id=recommendation_id, reviewed=reviewed)
    if db_recommendation:
        return db_recommendation
    else:
        raise HTTPException(status_code=404, detail=f"Recommendation with id {recommendation_id} not found")

@router.delete("/recommendations/{recommendation_id}", response_model=schemas.LocationCategoryReview)
async def delete_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    db_recommendation = await crud.delete_recommendation(db=db, recommendation_id=recommendation_id)
    if db_recommendation:
        return db_recommendation
    else:
        raise HTTPException(status_code=404, detail=f"Recommendation with id {recommendation_id} not found")

# Export the router
recommendations_router = router
