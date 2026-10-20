import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 指定 SQLite 資料庫檔案路徑（會在專案根目錄自動產生）
SQLALCHEMY_DATABASE_URL = "sqlite:///./genfit.db"

# 2. 建立資料庫引擎 (check_same_thread 用於支援 FastAPI 的多執行緒環境)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 建立 Session 工作階段工廠與 ORM 基礎類別
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 4. 定義使用者資料表模型 (包含密碼雜湊與資安考量)
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # 儲存加密後的密碼
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 5. 定義運動動作紀錄資料表模型
class ExerciseLog(Base):
    __tablename__ = "exercise_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # 關聯至使用者 ID
    exercise_name = Column(String, nullable=False)                   # 運動名稱（如：深蹲）
    exercise_code = Column(String, nullable=False)                   # AI 動作代號
    joint_angles = Column(Text, nullable=False)                      # 儲存關節角度 JSON 字串
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 6. 提供給 FastAPI 的資料庫 Session 依賴函數
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 7. 初始化建立資料庫與實體表格
def init_db():
    Base.metadata.create_all(bind=engine)