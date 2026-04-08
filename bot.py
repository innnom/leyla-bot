import requests
import time
import json

TOKEN = "8776355222:AAG4B1mxfINMu38buRwo5BHSBMIRsroBlhA"

# Очищаем очередь при запуске
print("🧹 Очищаем очередь обновлений...")
requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={"offset": -1})
requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
print("✅ Готово!")

def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    
    response = requests.post(url, data=data)
    print(f"📤 Статус: {response.status_code}")
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
                    print(f"📨 Получено сообщение")
                    
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"]["text"]
                        
                        print(f"💬 Текст: {text}")
                        
                        if text == "/start":
                            pdf_url = "https://quiet-sky-6d3a.inomnekto.workers.dev/sstrategy.pdf"
                            
                            keyboard = {
                                "inline_keyboard": [
                                    [{"text": "📄 Открыть PDF", "url": pdf_url}]
                                ]
                            }
                            
                            send_message(chat_id, "Привет! 👋\nНажми на кнопку, чтобы открыть PDF:", keyboard)
                            print(f"✅ Ответ отправлен")
                        
                        last_update_id = update["update_id"]
        
        time.sleep(1)
        
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        time.sleep(5)
