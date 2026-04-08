import requests
import time
import json
import os

TOKEN = "8776355222:AAG4B1mxfINMu38buRwo5BHSBMIRsroBlhA"

def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    
    print(f"📤 Отправляем: {data}")
    
    response = requests.post(url, data=data)
    print(f"📤 Статус: {response.status_code}")
    print(f"📤 Ответ: {response.text}")
    
    return response.json()

print("🤖 Бот запущен на Railway!")
print("📱 Напиши /start\n")

last_update_id = 0

while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        response = requests.get(url, params={"offset": last_update_id + 1, "timeout": 30})
        
        print(f"🔄 Проверяем обновления... статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📦 Данные от Telegram: {json.dumps(data, indent=2)}")
            
            if data.get("ok") and data.get("result"):
                for update in data["result"]:
                    print(f"📨 Получен апдейт: {update}")
                    
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"]["text"]
                        
                        print(f"💬 Сообщение от {chat_id}: {text}")
                        
                        if text == "/start":
                            pdf_url = "https://quiet-sky-6d3a.inomnekto.workers.dev/sstrategy.pdf"
                            
                            keyboard = {
                                "inline_keyboard": [
                                    [{"text": "📄 Открыть PDF", "url": pdf_url}]
                                ]
                            }
                            
                            result = send_message(chat_id, "Привет! 👋\nНажми на кнопку, чтобы открыть PDF:", keyboard)
                            
                            if result.get("ok"):
                                print(f"✅ Сообщение отправлено!")
                            else:
                                print(f"❌ Ошибка: {result}")
                        
                        last_update_id = update["update_id"]
        
        time.sleep(2)
        
    except Exception as e:
        print(f"⚠️ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(5)
