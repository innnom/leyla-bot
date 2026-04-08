import requests
import time
import json

TOKEN = "8776355222:AAG4B1mxfINMu38buRwo5BHSBMIRsroBlhA"

print("🚀 БОТ ЗАПУЩЕН")

# Удаляем webhook
requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
print("Webhook удален")

# Очищаем очередь
requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={"offset": -1})
print("Очередь очищена")

print("✅ БОТ ГОТОВ. ЖДУ /start")

last_id = 0

def send_photo_with_caption(chat_id, image_path, caption, keyboard=None):
    """Отправка изображения с подписью и кнопкой"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': 'HTML'
        }
        if keyboard:
            data['reply_markup'] = json.dumps(keyboard)
        
        response = requests.post(url, files=files, data=data)
        print(f"📷 Фото с подписью отправлено: {response.status_code}")
        return response.json()

# Текст сообщения (будет под изображением)
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

# Ссылка на PDF
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
                        # Создаем кнопку
                        keyboard = {
                            "inline_keyboard": [
                                [{"text": "📄 Открыть PDF", "url": PDF_URL}]
                            ]
                        }
                        
                        # Отправляем ОДНО сообщение: изображение + текст под ним + кнопка
                        send_photo_with_caption(chat_id, "image.jpg", MESSAGE_TEXT, keyboard)
                        print(f"✅ Сообщение отправлено пользователю {chat_id}")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        time.sleep(5)
