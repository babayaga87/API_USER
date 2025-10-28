from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app import schemas, models, services
from app.core.database import get_db

router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)

@router.post("/", response_model=schemas.TripResponse, status_code=status.HTTP_201_CREATED)
async def request_new_trip( # Chuyển sang async vì service có gọi API
    trip: schemas.TripCreate, 
    db: Session = Depends(get_db)
):
    """
    Hành khách yêu cầu một chuyến đi mới.
    """ 
    # Chỉ cần gọi service, mọi logic đã nằm trong đó
    return  services.create_trip(db=db, trip_data=trip)


@router.get("/{trip_id}", response_model=schemas.TripResponse)
def get_trip_details(
    trip_id: UUID, 
    db: Session = Depends(get_db)
):
    """
    Lấy thông tin chi tiết của một chuyến đi.
    """
    db_trip = services.get_trip_by_id(db, trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # TODO: Đây là nơi bạn có thể làm "API Composition"
    # Gọi userService để lấy tên passenger
    # Gọi driverService để lấy tên tài xế
    # Gộp 3 response lại rồi trả về
    
    return db_trip