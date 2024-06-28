from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import models
import schemas
# from . import models, schemas


def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.id == location_id).first()

def get_locations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Location).offset(skip).limit(limit).all()

def update_location(db: Session, location_id: int, location: schemas.LocationUpdate):
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if db_location:
        db_location.latitude = location.latitude if location.latitude is not None else db_location.latitude
        db_location.longitude = location.longitude if location.longitude is not None else db_location.longitude
        db.commit()
        db.refresh(db_location)
        return db_location
    return None

def delete_location(db: Session, location_id: int):
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if db_location:
        db.delete(db_location)
        db.commit()
        return db_location
    return None

def create_location(db: Session, location: schemas.LocationCreate):
    db_location = models.Location(latitude=location.latitude, longitude=location.longitude)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db_category.name = category.name if category.name is not None else db_category.name
        db.commit()
        db.refresh(db_category)
        return db_category
    return None

def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return db_category
    return None

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_unreviewed_locations(db: Session, days: int = 30, limit: int = 10):
    threshold_date = datetime.utcnow() - timedelta(days=days)
    return db.query(models.LocationCategoryReview).filter(models.LocationCategoryReview.last_reviewed < threshold_date).order_by(models.LocationCategoryReview.last_reviewed).limit(limit).all()

async def create_recommendation(db: Session, recommendation: schemas.LocationCategoryReviewCreate):
    db_recommendation = models.LocationCategoryReview(
        location_id=recommendation.location_id,
        category_id=recommendation.category_id,
        last_reviewed=datetime.now(timezone.utc)  # Actualiza la fecha y hora en UTC
    )
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation

def update_recommendation(db: Session, recommendation_id: int, reviewed: bool):
    db_recommendation = db.query(models.LocationCategoryReview).filter(models.LocationCategoryReview.id == recommendation_id).first()
    if db_recommendation:
        db_recommendation.reviewed = reviewed  # Actualiza el campo revisado
        db.commit()
        db.refresh(db_recommendation)
        return db_recommendation
    return None

def delete_recommendation(db: Session, recommendation_id: int):
    db_recommendation = db.query(models.LocationCategoryReview).filter(models.LocationCategoryReview.id == recommendation_id).first()
    if db_recommendation:
        db.delete(db_recommendation)
        db.commit()
        return db_recommendation
    return None


