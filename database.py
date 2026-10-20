import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 使用 SQLite 資料庫，會在專案根目錄自動產生 genfit.db 檔案
SQLALCHEMY_DATABASE_URL = "sqlite:///./genfit.db"

# connect_args={"check_same_thread": False} 是 SQLite 在 FastAPI 多執行緒下必備的設定
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 1. 使用者資料表（包含密碼雜湊資安設計）
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # 儲存加密後的密碼
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 2. 運動動作紀錄資料表
class ExerciseLog(Base):
    __tablename__ = "exercise_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # 允許訪客或填寫特定使用者 ID
    exercise_name = Column(String, nullable=False)                  # 輸入的運動名稱（如：深蹲）
    exercise_code = Column(String, nullable=False)                  # AI 產生的代號（如：squat）
    joint_angles = Column(Text, nullable=False)                     # 儲存 Gemini 回傳的角度 JSON 字串
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 提供給 FastAPI 取得資料庫連線 Session 的 Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 初始化建立 SQLite 資料庫檔案與表格
def init_db():
    Base.metadata.create_all(bind=engine)