# models.py
from sqlalchemy import (Column, String, Boolean, TIMESTAMP, ForeignKey,
                        Date, Numeric, Integer, SmallInteger)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firebase_uid = Column(String, unique=True, index=True, nullable=True) # (nullable=True nếu có thể có user không dùng Firebase)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), unique=True)
    #password_hash = Column(String(255)) # Vẫn định nghĩa ở đây, nhưng API sẽ bỏ qua
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default='passenger')
    is_verified = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Quan hệ 1-1 với DriverProfile
    driver_profile = relationship("DriverProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

class DriverProfile(Base):
    __tablename__ = "driver_profiles"
    
    driver_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    license_number = Column(String(100), unique=True, nullable=False)
    #license_expiry = Column(Date)
    approval_status = Column(String(20), default='pending')
    rating_avg = Column(Numeric(3, 2), default=0.0)
    total_trips = Column(Integer, default=0)
    profile_photo_url = Column(String(512))
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Quan hệ 1-1
    user = relationship("User", back_populates="driver_profile")
    # Quan hệ 1-Nhiều với Vehicle
    vehicles = relationship("Vehicle", back_populates="driver", cascade="all, delete-orphan")

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_id = Column(UUID(as_uuid=True), ForeignKey("driver_profiles.driver_id", ondelete="CASCADE"), nullable=False)
    license_plate = Column(String(20), unique=True, nullable=False)
    model = Column(String(100))
    color = Column(String(50))
    year = Column(SmallInteger)
    is_active = Column(Boolean, default=False)
    
    registered_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Quan hệ Nhiều-1
    driver = relationship("DriverProfile", back_populates="vehicles")