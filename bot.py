import requests
import time
import json
import os
from datetime import datetime

TOKEN = "8701460359:AAERNfHHiTbOsMn5enh3IvpLt3WtdN9rehY"

# Пользователи с доступом к /stat
ADMIN_USERNAMES = {"innnom", "llshkka"}

# Файл для хранения статистики
STATS_FILE = "stats.json"

print("🚀 БОТ ЗАПУЩЕН")

# Удаляем webhook
requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
print("Webhook удален")

# Очищаем очередь
requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={"offset": -1})
print("Очередь очищена")

print("✅ БОТ ГОТОВ. ЖДУ /start")

last_id = 0

# ──────────────────────────────────────────
# Работа со статистикой
# ──────────────────────────────────────────

def load_stats():
    """Загрузить статистику из файла"""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": {}, "total_starts": 0}

def save_stats(stats):
    """Сохранить статистику в файл"""
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def register_user(stats, user):
    """Записать пользователя при /start"""
    user_id = str(user.get("id"))
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    if user_id not in stats["users"]:
        # Новый пользователь
        stats["users"][user_id] = {
            "id": user_id,
            "first_name": user.get("first_name", ""),
            "last_name": user.get("last_name", ""),
            "username": user.get("username", ""),
            "first_visit": now,
            "last_visit": now,
            "visits": 1
        }
    else:
        # Повторный визит
        stats["users"][user_id]["last_visit"] = now
        stats["users"][user_id]["visits"] += 1
        # Обновляем имя/username (могли измениться)
        stats["users"][user_id]["first_name"] = user.get("first_name", "")
        stats["users"][user_id]["last_name"] = user.get("last_name", "")
        stats["users"][user_id]["username"] = user.get("username", "")

    stats["total_starts"] += 1
    save_stats(stats)

def build_stat_message(stats):
    """Сформировать текст статистики"""
    users = stats["users"]
    total_unique = len(users)
    total_starts = stats["total_starts"]
    repeat_users = sum(1 for u in users.values() if u["visits"] > 1)

    lines = [
        "📊 <b>Статистика бота</b>",
        "",
        f"👥 Уникальных пользователей: <b>{total_unique}</b>",
        f"▶️ Всего нажатий /start: <b>{total_starts}</b>",
        f"🔁 Вернулись повторно: <b>{repeat_users}</b>",
        "",
        "─────────────────────",
        "📋 <b>Список пользователей:</b>",
        "",
    ]

    # Сортируем по дате первого визита (новые сначала)
    sorted_users = sorted(
        users.values(),
        key=lambda u: u["first_visit"],
        reverse=True
    )

    for i, u in enumerate(sorted_users, 1):
        name = f"{u['first_name']} {u['last_name']}".strip() or "Без имени"
        username = f"@{u['username']}" if u['username'] else "нет username"
        visits_str = f"{u['visits']} раз" if u['visits'] != 1 else "1 раз"

        lines.append(
            f"{i}. <b>{name}</b> ({username})\n"
            f"   🆔 {u['id']} | 📅 {u['first_visit']} | 🔁 был(а) {visits_str}"
        )

    if not sorted_users:
        lines.append("Пока никого нет 😔")

    return "\n".join(lines)

# ──────────────────────────────────────────
# Отправка сообщений
# ──────────────────────────────────────────

def send_message(chat_id, text):
    """Отправить текстовое сообщение"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    # Telegram ограничивает сообщения ~4096 символами — режем если надо
    max_len = 4000
    chunks = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    for chunk in chunks:
        requests.post(url, data={
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "HTML"
        })

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

# ──────────────────────────────────────────
# Тексты
# ──────────────────────────────────────────

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

PDF_URL = "https://leylastrategy.inomnekto.workers.dev/sstrategy.pdf"

# ──────────────────────────────────────────
# Главный цикл
# ──────────────────────────────────────────

stats = load_stats()

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
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]
                    text = msg.get("text", "")
                    user = msg.get("from", {})
                    username = user.get("username", "")

                    print(f"💬 Текст: {text} | от @{username}")
                    
                    if text == "/start":
                        # Фиксируем пользователя
                        register_user(stats, user)

                        keyboard = {
                            "inline_keyboard": [
                                [{"text": "Подробнее", "url": PDF_URL}]
                            ]
                        }
                        send_photo_with_caption(chat_id, "image.jpg", MESSAGE_TEXT, keyboard)
                        print(f"✅ Сообщение отправлено пользователю {chat_id}")

                    elif text == "/stat":
                        # Проверяем права
                        if username in ADMIN_USERNAMES:
                            stat_text = build_stat_message(stats)
                            send_message(chat_id, stat_text)
                            print(f"📊 Статистика отправлена @{username}")
                        else:
                            # Тихо игнорируем — ответа нет
                            print(f"🚫 /stat от @{username} — нет доступа, игнорируем")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        time.sleep(5)
