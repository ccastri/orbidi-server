from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from db import Base  # Asegúrate de que la importación relativa es correcta
# from .db import Base  # Asegúrate de que la importación relativa es correcta

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    reviews = relationship("LocationCategoryReview", back_populates="location")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    reviews = relationship("LocationCategoryReview", back_populates="category")

class LocationCategoryReview(Base):
    __tablename__ = 'location_category_reviews'
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    last_reviewed = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    location = relationship("Location", back_populates="reviews")
    category = relationship("Category", back_populates="reviews")
