import json
import os
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from services.gemini_service import get_skeleton_test_data
from database import init_db, get_db, ExerciseLog

app = FastAPI(
    title="GenFit AI Backend",
    description="提供 3D 骨架與動作控制參數的 AI 核心後端",
    version="1.0.0"
)

# 伺服器啟動時自動建立 SQLite 檔案與資料表
@app.on_event("startup")
def startup_event():
    init_db()

# 定義前端傳進來的請求格式
class ExerciseRequest(BaseModel):
    exercise_name: str
    user_id: int = 1  # 預設使用者 ID，後續接上會員系統可傳真實 ID

@app.get("/")
def read_root():
    return {"status": "success", "message": "GenFit AI 後端伺服器 (SQLite 已連線) 運行中！"}

@app.post("/api/get-skeleton")
def get_skeleton_data(request: ExerciseRequest, db: Session = Depends(get_db)):
    """
    1. 接收動作名稱，呼叫 Gemini AI
    2. 將產生的動作骨架自動記錄到 SQLite 資料庫
    3. 回傳 JSON 給前端
    """
    print(f"收到前端請求，正在處理動作：{request.exercise_name}")
    
    # 呼叫 Gemini AI 服務
    skeleton_data = get_skeleton_test_data(request.exercise_name)
    
    # 將關節角度字典轉成 JSON 字串儲存
    joint_angles_str = json.dumps(skeleton_data.get("joint_angles", {}))
    
    # 建立 SQLite 動作紀錄物件
    log_entry = ExerciseLog(
        user_id=request.user_id,
        exercise_name=request.exercise_name,
        exercise_code=skeleton_data.get("exercise_code", "unknown"),
        joint_angles=joint_angles_str
    )
    
    # 寫入 SQLite 資料庫
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    
    return {
        "status": "success",
        "log_id": log_entry.id,  # 回傳這筆記錄在 SQLite 中的流水號 ID
        "data": skeleton_data
    }