# schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date


# --- PHẦN MỚI CHO VEHICLE (TOÀN BỘ) ---

class VehicleBase(BaseModel):
    license_plate: str
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None

class VehicleCreate(VehicleBase):
    pass # Khi tạo, chỉ cần thông tin base

class VehicleUpdate(BaseModel):
    # Khi cập nhật, mọi thứ đều là tùy chọn
    #license_plate: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None
    is_active: Optional[bool] = None

class Vehicle(VehicleBase):
    # Đây là model trả về (Read)
    id: UUID
    driver_id: UUID
    is_active: bool
    registered_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# --- SCHEMAS CHO DRIVER & VEHICLE (để minh họa) ---

class DriverProfileBase(BaseModel):
    license_number: str
    #license_expiry: Optional[date] = None

class DriverProfileCreate(DriverProfileBase):
    pass

class DriverProfile(DriverProfileBase):
    driver_id: UUID
    user_id: UUID
    approval_status: str
    rating_avg: float
    total_trips: int

    vehicles: List[Vehicle] = [] # <-- THÊM DÒNG NÀY
    
    model_config = ConfigDict(from_attributes=True)

class DriverProfileUpdate(BaseModel):
    license_number: Optional[str] = None
    #license_expiry: Optional[date] = None
    approval_status: Optional[str] = None # Thường admin mới được sửa cái này
    profile_photo_url: Optional[str] = None


# --- SCHEMAS CHO USER ---

class UserBase(BaseModel):
    # Đây là các trường an toàn để nhận làm input
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    firebase_uid: Optional[str] = None

class UserCreate(UserBase):
    # Khi tạo user, chúng ta chỉ cần thông tin base
    # KHÔNG CÓ MẬT KHẨU
    pass

class UserUpdate(BaseModel):
    # Khi cập nhật, tất cả các trường đều là tùy chọn
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    # Đây là model trả về cho client (response)
    # KHÔNG CÓ password_hash
    id: UUID
    role: str
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    driver_profile: Optional[DriverProfile] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    # Khi cập nhật, tất cả các trường đều là tùy chọn
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None

class DriverSignUp(UserCreate):
    """
    Schema dùng riêng cho endpoint đăng ký Driver.
    Kế thừa email, full_name, phone_number, firebase_uid từ UserCreate.
    """
    license_number: str
    license_expiry: Optional[date] = None