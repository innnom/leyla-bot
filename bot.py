import requests
import time

TOKEN = "8776355222:AAG4B1mxfINMu38buRwo5BHSBMIRsroBlhA"

print("🚀 СТАРТ БОТА")
print(f"Токен: {TOKEN[:10]}...")

# Проверка
r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe")
print(f"Бот: {r.json()}")

# Удаляем webhook
requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
print("Webhook удален")

# Очищаем очередь
requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={"offset": -1})
print("Очередь очищена")

print("✅ БОТ ГОТОВ. ЖДУ /start")

last_id = 0

while True:
    try:
        resp = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/getUpdates",
            params={"offset": last_id + 1, "timeout": 10}
        )
        
        data = resp.json()
        
        if data.get("result"):
            for update in data["result"]:
                print(f"📨 Новое сообщение!")
                last_id = update["update_id"]
                
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text", "")
                    print(f"Текст: {text}")
                    
                    # Отправляем ответ
                    send_data = {
                        "chat_id": chat_id,
                        "text": f"✅ Бот работает! Ты написал: {text}"
                    }
                    requests.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        json=send_data
                    )
                    print("✅ Ответ отправлен")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
