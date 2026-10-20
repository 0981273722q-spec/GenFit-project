import json
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

# 伺服器啟動時自動建立資料庫與表格
@app.on_event("startup")
def startup_event():
    init_db()

# 定義前端傳進來的請求格式 (資料驗證)
class ExerciseRequest(BaseModel):
    exercise_name: str
    user_id: int = 1  # 預設使用者 ID

# 根目錄健康檢查
@app.get("/")
def read_root():
    return {"status": "success", "message": "GenFit AI 後端伺服器運行中！"}

# 核心 API 端點：接收前端動作 ➔ 呼叫 AI ➔ 寫入資料庫
@app.post("/api/get-skeleton")
def get_skeleton_data(request: ExerciseRequest, db: Session = Depends(get_db)):
    print(f"收到前端請求，正在處理動作：{request.exercise_name}")
    
    # 1. 呼叫我們寫好的 Gemini AI 服務
    skeleton_data = get_skeleton_test_data(request.exercise_name)
    
    # 2. 將 AI 算出的關節角度字典轉成 JSON 字串
    joint_angles_str = json.dumps(skeleton_data.get("joint_angles", {}))
    
    # 3. 建立 SQLite 資料庫紀錄物件
    log_entry = ExerciseLog(
        user_id=request.user_id,
        exercise_name=request.exercise_name,
        exercise_code=skeleton_data.get("exercise_code", "unknown"),
        joint_angles=joint_angles_str
    )
    
    # 4. 寫入並提交到 SQLite 資料庫
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    
    # 5. 回傳結果給前端
    return {
        "status": "success",
        "log_id": log_entry.id,
        "data": skeleton_data
    }