from google import genai

client = genai.Client(api_key="AQ.Ab8RN6KycydNrzXmDpANTNv6cZ1Tsg1BTKmAb7wT3hy0cLYl_g")

print("正在連線至 Gemini...")

response = client.models.generate_content(
    model="gemini-3.8-flash",  # 改這裡！
    contents="嗨！請用一句話向我打個招呼，證明我們連線成功！",
)

print("--- 測試成功！ ---")
print("AI 的回覆：", response.text)