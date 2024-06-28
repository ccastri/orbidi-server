from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
import schemas
import crud
from db import get_db

router = APIRouter()

@router.get("/locations/{location_id}", response_model=schemas.Location)
async def read_location(location_id: int, request: Request, db: Session = Depends(get_db)):
    location = await crud.get_location(db=db, location_id=location_id)
    if location:
        return {"location": location, "root_path": request.scope.get("root_path")}
    else:
        raise HTTPException(status_code=404, detail=f"Location with id {location_id} not found")

@router.post("/locations/", response_model=schemas.Location)
async def create_location(location: schemas.LocationCreate, request: Request, db: Session = Depends(get_db)):
    new_location = await crud.create_location(db=db, location=location)
    return {"location": new_location, "root_path": request.scope.get("root_path")}

@router.put("/locations/{location_id}", response_model=schemas.Location)
async def update_location(location_id: int, location: schemas.LocationUpdate, request: Request, db: Session = Depends(get_db)):
    updated_location = await crud.update_location(db=db, location_id=location_id, location=location)
    if updated_location:
        return {"location": updated_location, "root_path": request.scope.get("root_path")}
    else:
        raise HTTPException(status_code=404, detail=f"Location with id {location_id} not found")

@router.delete("/locations/{location_id}", response_model=schemas.Location)
async def delete_location(location_id: int, request: Request, db: Session = Depends(get_db)):
    deleted_location = await crud.delete_location(db=db, location_id=location_id)
    if deleted_location:
        return {"location": deleted_location, "root_path": request.scope.get("root_path")}
    else:
        raise HTTPException(status_code=404, detail=f"Location with id {location_id} not found")

# Exportar el router
location_router = router
