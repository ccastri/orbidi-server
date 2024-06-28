from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
import schemas
import crud
from db import get_db

# from .. import schemas, crud
# from ..db import get_db

router = APIRouter()

@router.get('/healthcheck')
async def healthcheck(request: Request):
    try:
        print("Healthcheck endpoint called")
        return {"status": "healthy", "root_path": request.scope.get("root_path")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")


@router.get("/recommendations/", response_model=List[schemas.LocationCategoryReview])
async def get_recommendations(request: Request, db: Session = Depends(get_db)):
    recommendations = crud.get_unreviewed_locations(db=db)
    return {"recommendations": recommendations, "root_path": request.scope.get("root_path")}


@router.post("/recommendations/", response_model=schemas.LocationCategoryReview)
async def create_recommendation(recommendation: schemas.LocationCategoryReviewCreate, request: Request, db: Session = Depends(get_db)):
    db_recommendation = await crud.create_recommendation(db=db, recommendation=recommendation)
    return {"recommendation": db_recommendation, "root_path": request.scope.get("root_path")}

@router.put("/recommendations/{recommendation_id}", response_model=schemas.LocationCategoryReview)
async def update_recommendation(recommendation_id: int, reviewed: bool, request: Request, db: Session = Depends(get_db)):
    db_recommendation = await crud.update_recommendation(db=db, recommendation_id=recommendation_id, reviewed=reviewed)
    if db_recommendation:
        return {"recommendation": db_recommendation, "root_path": request.scope.get("root_path")}
    else:
        raise HTTPException(status_code=404, detail=f"Recommendation with id {recommendation_id} not found")

@router.delete("/recommendations/{recommendation_id}", response_model=schemas.LocationCategoryReview)
async def delete_recommendation(recommendation_id: int, request: Request, db: Session = Depends(get_db)):
    db_recommendation = await crud.delete_recommendation(db=db, recommendation_id=recommendation_id)
    if db_recommendation:
        return {"recommendation": db_recommendation, "root_path": request.scope.get("root_path")}
    else:
        raise HTTPException(status_code=404, detail=f"Recommendation with id {recommendation_id} not found")

# Export the router
recommendations_router = router
