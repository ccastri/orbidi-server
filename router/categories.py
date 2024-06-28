from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import schemas
import crud
from db import get_db

router = APIRouter()

@router.post("/categories/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, request: Request, db: Session = Depends(get_db)):
    new_category = await crud.create_category(db=db, category=category)
    return {"category": new_category, "root_path": request.scope.get("root_path")}

@router.get("/categories/", response_model=list[schemas.Category])
async def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = crud.get_categories(db=db, skip=skip, limit=limit)
    return categories

@router.get("/categories/{category_id}", response_model=schemas.Category)
async def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db=db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/categories/{category_id}", response_model=schemas.Category)
async def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    updated_category = crud.update_category(db=db, category_id=category_id, category=category)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/categories/{category_id}", response_model=schemas.Category)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted_category = crud.delete_category(db=db, category_id=category_id)
    if deleted_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return deleted_category

# Exportar el router
category_router = router
