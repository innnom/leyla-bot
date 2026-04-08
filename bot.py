import requests
import time
import json

TOKEN = "8776355222:AAG4B1mxfINMu38buRwo5BHSBMIRsroBlhA"

print("🚀 БОТ ЗАПУЩЕН")
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

def send_photo(chat_id, image_path):
    """Отправка изображения"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': chat_id}
            response = requests.post(url, files=files, data=data)
            print(f"📷 Фото отправлено: {response.status_code}")
            return response.json()
    except Exception as e:
        print(f"❌ Ошибка отправки фото: {e}")
        return None

def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    response = requests.post(url, data=data)
    print(f"📤 Сообщение отправлено: {response.status_code}")
    return response.json()

# Текст сообщения
MESSAGE_TEXT = """Привет. Я Лейла🙌🏻

Сегодня ты получишь систему, благодаря которой сможешь зайти в графический дизайн с нуля и выйти на 100 000 ₽+, даже если сейчас у тебя нет опыта, портфолио и связей.

Да, это возможно.
Даже если ты никогда не открывал(а) программы.
Даже если думаешь, что «уже поздно» развиваться в онлайне.

Я тоже начинала без громкого имени и сильного старта.
Без стабильных заказов.
Без понимания, как вообще зарабатывать в этой нише.

Но когда я выстроила систему, всё изменилось.

Не "волшебная программа".
Не «талант».
А структура: какие навыки качать, как собрать портфолио, как прокачать навык продаж, как выйти на первых клиентов.

В этой статье я разберу:
— как войти в дизайн с нуля
— какие шаги дают реальный доход от 100к+
— и как не застрять в бесконечном обучении

Если ты хочешь не просто "изучить дизайн", а начать на нём зарабатывать, жми ниже⤵️"""

# Ссылка на PDF (ОБНОВЛЕНО)
PDF_URL = "https://leylastrategy.inomnekto.workers.dev/sstrategy.pdf"

while True:
    try:
        resp = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/getUpdates",
            params={"offset": last_id + 1, "timeout": 30}
        )
        
        data = resp.json()
        
        if data.get("result"):
            for update in data["result"]:
                print(f"📨 Новое сообщение!")
                last_id = update["update_id"]
                
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text", "")
                    print(f"💬 Текст: {text}")
                    
                    if text == "/start":
                        # 1. Отправляем изображение image.jpg
                        send_photo(chat_id, "image.jpg")
                        
                        # Небольшая пауза, чтобы сообщения не слились
                        time.sleep(0.5)
                        
                        # 2. Отправляем текст с кнопкой
                        keyboard = {
                            "inline_keyboard": [
                                [{"text": "📄 Открыть PDF", "url": PDF_URL}]
                            ]
                        }
                        send_message(chat_id, MESSAGE_TEXT, keyboard)
                        print(f"✅ Ответ отправлен пользователю {chat_id}")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        time.sleep(5)
