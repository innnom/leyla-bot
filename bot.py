import requests
import time
import json

TOKEN = "8776355222:AAG4B1mxfINMu38buRwo5BHSBMIRsroBlhA"

print("🤖 Бот запущен")

# Удаляем webhook
requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
print("✅ Webhook удален")

# Очищаем все старые обновления
requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={"offset": -1})
print("✅ Очередь очищена")

print("📱 Напиши /start\n")

last_id = 0

def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    
    response = requests.post(url, data=data)
    print(f"📤 Статус: {response.status_code}")
    return response.json()

while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        params = {"offset": last_id + 1, "timeout": 30}
        
        response = requests.get(url, params=params, timeout=35)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("ok") and data.get("result"):
                for update in data["result"]:
                    print(f"📨 Получен update {update['update_id']}")
                    
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"]["text"]
                        
                        print(f"💬 Сообщение: {text}")
                        
                        if text == "/start":
                            pdf_url = "https://quiet-sky-6d3a.inomnekto.workers.dev/sstrategy.pdf"
                            
                            keyboard = {
                                "inline_keyboard": [
                                    [{"text": "📄 Открыть PDF", "url": pdf_url}]
                                ]
                            }
                            
                            result = send_message(chat_id, "Привет! 👋\nНажми на кнопку, чтобы открыть PDF:", keyboard)
                            
                            if result.get("ok"):
                                print(f"✅ Ответ отправлен!")
                            else:
                                print(f"❌ Ошибка: {result}")
                        
                        last_id = update["update_id"]
                        print(f"🆔 Новый last_id: {last_id}")
            else:
                print("⏳ Нет новых сообщений...")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        time.sleep(5)
