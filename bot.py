import requests
import time
import json
import os

TOKEN = "8701460359:AAERNfHHiTbOsMn5enh3IvpLt3WtdN9rehY"

def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    
    response = requests.post(url, data=data)
    return response.json()

print("🤖 Бот запущен на Railway!")
print("📱 Напиши /start\n")

last_update_id = 0

while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        response = requests.get(url, params={"offset": last_update_id + 1, "timeout": 30})
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok") and data.get("result"):
                for update in data["result"]:
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"]["text"]
                        
                        if text == "/start":
                            pdf_url = "https://quiet-sky-6d3a.inomnekto.workers.dev/sstrategy.pdf"
                            
                            keyboard = {
                                "inline_keyboard": [
                                    [{"text": "📄 Открыть PDF", "url": pdf_url}]
                                ]
                            }
                            
                            send_message(chat_id, "Привет! 👋\nНажми на кнопку, чтобы открыть PDF:", keyboard)
                            print(f"✅ Ответ отправлен {chat_id}")
                        
                        last_update_id = update["update_id"]
        
        time.sleep(1)
        
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        time.sleep(5)