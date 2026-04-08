import requests
import time
import json
import sys

TOKEN = "8776355222:AAG4B1mxfINMu38buRwo5BHSBMIRsroBlhA"

# Принудительно очищаем webhook и очередь
print("🧹 Очистка webhook и очереди...")
try:
    # Удаляем webhook
    r1 = requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
    print(f"  deleteWebhook: {r1.json()}")
    
    # Очищаем очередь обновлений
    r2 = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={"offset": -1})
    print(f"  getUpdates(-1): {r2.json()}")
except Exception as e:
    print(f"  Ошибка очистки: {e}")

print("✅ Очистка завершена")
print("🤖 Бот запущен на Railway!")
print(f"🆔 Bot ID: {TOKEN.split(':')[0]}")
print("📱 Напиши /start\n")
sys.stdout.flush()  # Принудительно выводим логи

def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    
    print(f"📤 Отправка сообщения в {chat_id}...")
    response = requests.post(url, data=data)
    print(f"📤 Статус: {response.status_code}")
    if response.status_code != 200:
        print(f"📤 Ошибка: {response.text}")
    return response.json()

last_update_id = 0
error_count = 0

while True:
    try:
        # Получаем обновления
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        params = {"offset": last_update_id + 1, "timeout": 30}
        
        print(f"🔄 Запрос getUpdates (offset={last_update_id + 1})...")
        response = requests.get(url, params=params, timeout=35)
        print(f"🔄 Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"🔄 Ответ: ok={data.get('ok')}, result_count={len(data.get('result', []))}")
            
            if data.get("ok") and data.get("result"):
                for update in data["result"]:
                    print(f"📨 Получен update: {update.get('update_id')}")
                    
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
                            
                            send_message(chat_id, "Привет! 👋\nНажми на кнопку, чтобы открыть PDF:", keyboard)
                            print(f"✅ Ответ отправлен в {chat_id}")
                        else:
                            send_message(chat_id, f"Я понимаю только команду /start. Ты написал: {text}")
                            print(f"✅ Ответ отправлен в {chat_id}")
                        
                        last_update_id = update["update_id"]
                        print(f"🆔 Обновлен last_update_id: {last_update_id}")
            else:
                print(f"⚠️ Нет новых обновлений или ошибка в данных")
        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
        
        error_count = 0
        time.sleep(2)
        
    except Exception as e:
        error_count += 1
        print(f"❌ Ошибка (попытка {error_count}): {e}")
        if error_count > 10:
            print("🔥 Слишком много ошибок, перезапуск...")
            sys.exit(1)
        time.sleep(5)
