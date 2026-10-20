import os
import json
from dotenv import load_dotenv
from google import genai

# 1. 載入環境變數並初始化 Gemini 客戶端
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_skeleton_test_data(exercise_name: str) -> dict:
    """請求 Gemini 針對指定動作回傳骨架代號與關節角度（JSON 格式）"""
    try:
        # 2. 設計給 AI 的提示詞（Prompt），強烈約束輸出格式
        prompt = f"""
        你是一個 3D 骨架動畫 AI 核心。使用者指定的動作是：{exercise_name}。
        請以純 JSON 格式回傳（絕對不要包含 ```json 標記），必須包含以下欄位：
        1. "exercise_code": 英文代號（例如 "squat", "plank"）。
        2. "joint_angles": 關節角度物件（例如 {{"left_knee": 90, "spine": 15}}）。
        3. "message": 提示文字。
        """
        
        # 3. 呼叫 Google GenAI SDK 產生內容
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        
        # 4. 清理 AI 回傳的 Markdown 標記並轉成 Python 字典
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
        
    except Exception as e:
        # 5. 例外處理：若發生錯誤回傳安全預設值，避免程式崩潰
        print(f"❌ 【Gemini API 錯誤】: {e}")
        return {
            "exercise_code": "error",
            "joint_angles": {"left_knee": 0, "right_knee": 0, "spine": 0},
            "message": f"系統發生例外錯誤: {e}"
        }