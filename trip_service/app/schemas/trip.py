from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional
from ..models.trip import TripStatus # Import Enum từ model

# Dữ liệu cơ bản
class TripBase(BaseModel):
    start_location_address: str
    start_lat: Decimal
    start_lng: Decimal
    end_location_address: str
    end_lat: Decimal
    end_lng: Decimal

# Dữ liệu nhận vào khi tạo chuyến
class TripCreate(TripBase):
    passenger_id: UUID
    # estimated_fare sẽ được tính bởi service

# Dữ liệu trả về cho client
class TripResponse(TripBase):
    id: UUID
    passenger_id: UUID
    driver_id: Optional[UUID] = None
    vehicle_id: Optional[UUID] = None
    status: TripStatus
    estimated_fare: Optional[Decimal] = None
    final_fare: Optional[Decimal] = None
    requested_at: datetime
    
    class Config:
        orm_mode = True # Cho phép Pydantic đọc từ model SQLAlchemy

# Dùng để cập nhật trạng thái
class TripStatusUpdate(BaseModel):
    status: TripStatus
