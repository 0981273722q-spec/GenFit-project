import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# 強制讀取根目錄的 .env 檔案
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
print(f"🔒 【系統檢查】讀取到的 API Key 是否存在：{bool(api_key)}")

client = genai.Client(api_key=api_key)

def get_skeleton_test_data(exercise_name: str) -> dict:
    """
    要求 Gemini 針對指定動作，回傳對應的骨架動畫代號與關節角度（JSON 格式）
    """
    try:
        prompt = f"""
        你是一個 3D 骨架動畫控制系統的 AI 核心。使用者指定的動作是：{exercise_name}。
        
        請以嚴格的 JSON 格式回傳（絕對不要包含 ```json 或任何反斜線標記），必須包含以下欄位：
        1. "exercise_code": 英文代號（例如 "squat", "plank", "idle"）。
        2. "joint_angles": 一個物件，包含主要關節的模擬旋轉角度（度數），例如膝蓋、脊椎、手臂。
           格式範例: {{"left_knee": 90, "right_knee": 90, "spine": 15}}
        3. "message": 給測試人員的提示文字。
        """
        
        # ✅ 更新為正確的模型名稱
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
        
    except Exception as e:
        print(f"❌ 【Gemini API 錯誤】: {str(e)}")
        return {
            "exercise_code": "error",
            "joint_angles": {"left_knee": 0, "right_knee": 0, "spine": 0},
            "message": f"後端呼叫 AI 發生例外錯誤: {str(e)}"
        }