# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# BÌNH LUẬN LẠI DÒNG POSTGRESQL GÂY LỖI:
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/user_db"

# SỬ DỤNG DÒNG SQLITE NÀY THAY THẾ:
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Khang#890kk2@localhost:5432/user_db"  # Sẽ tạo file user.db

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,    
    #connect_args={"check_same_thread": False} # Bắt buộc cho SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()