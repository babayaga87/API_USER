from sqlalchemy.orm import Session
from uuid import UUID
from . import models, schemas # Đảm bảo import models và schemas

#
# ❗️ LƯU Ý QUAN TRỌNG:
# Tạm thời, chúng ta sẽ định nghĩa hàm này là HÀM ĐỒNG BỘ (dùng "def")
#
def create_trip(db: Session, trip_data: schemas.TripCreate):
   # 1. Chuyển đổi Pydantic schema -> SQLAlchemy model
    # (Dùng .model_dump() cho Pydantic v2)
    db_trip = models.Trip(**trip_data.model_dump())

    # 2. Thêm vào session (khu vực chờ)
    db.add(db_trip)

    # 3. LƯU (COMMIT) VÀO CSDL (BẠN CÓ THỂ ĐANG THIẾU DÒNG NÀY)
    db.commit()

    # 4. LÀM MỚI (REFRESH) ĐỐI TƯỢNG ĐỂ LẤY ID VÀ TIMESTAMP TỪ CSDL
    db.refresh(db_trip)

    return db_trip

def get_trip_by_id(db: Session, trip_id: UUID):
    """
    Hàm này lấy chi tiết một chuyến đi bằng ID của nó
    """
    # Dùng SQLAlchemy để query CSDL
    # Nó sẽ tìm trong bảng models.Trip
    # Lọc theo cột id và lấy bản ghi đầu tiên
    return db.query(models.Trip).filter(models.Trip.id == trip_id).first()

# Bạn có thể thêm các hàm service khác ở đây
# def get_trip(db: Session, trip_id: int):
#     ...