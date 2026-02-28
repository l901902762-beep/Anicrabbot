from telebot import TeleBot
from keep_alive import keep_alive
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

keep_alive()

# ✅ Bot tokeningiz
BOT_TOKEN = "8499334154:AAFBIypA5xDdvbwkW50mt7RZiPBcMutmBvw"
bot = TeleBot(BOT_TOKEN)

# 🔹 Majburiy obuna uchun kanal va egasi
CHANNELS = ["@kanal1", "@kanal2"]  # bu yerga kanallarni yozing
OWNER_ID = 123456789  # o'z Telegram ID'ingiz
ADMINS = [OWNER_ID]

# 🔹 Obuna tekshirish funksiyasi
def check_sub(user_id):
    for channel in CHANNELS:
        status = bot.get_chat_member(channel, user_id).status
        if status not in ["member", "administrator", "creator"]:
            return False
    return True

# 🔹 /start komanda
@bot.message_handler(commands=['start'])
def start(message):
    if not check_sub(message.from_user.id):
        markup = InlineKeyboardMarkup()
        for channel in CHANNELS:
            markup.add(InlineKeyboardButton("Obuna bo‘lish", url=f"https://t.me/{channel[1:]}"))
        markup.add(InlineKeyboardButton("Tekshirish", callback_data="check"))
        bot.send_message(message.chat.id, "Botdan foydalanish uchun obuna bo‘ling!", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Salom botimizga xush kelibsiz! 🎬")

# 🔹 Callback tugma tekshirish
@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
    if check_sub(call.from_user.id):
        bot.send_message(call.message.chat.id, "Obuna tasdiqlandi ✅ Endi kod yuboring.")
    else:
        bot.answer_callback_query(call.id, "Hali obuna bo‘lmagansiz ❌", show_alert=True)

# 🔹 Anime kodi qidirish
ANIME_DB = {
    "101": "https://t.me/kanaling/5",
    "102": "https://t.me/kanaling/6"
}

@bot.message_handler(func=lambda message: True)
def search(message):
    code = message.text.strip()
    if code in ANIME_DB:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🎬 Tomosha qilish", url=ANIME_DB[code]))
        bot.send_message(message.chat.id, "Mana topildi:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Bunday kod topilmadi ❌")

# 🔹 Admin panel
@bot.message_handler(commands=['addadmin'])
def add_admin(message):
    if message.from_user.id == OWNER_ID:
        try:
            new_admin = int(message.text.split()[1])
            ADMINS.append(new_admin)
            bot.send_message(message.chat.id, "Admin qo‘shildi ✅")
        except:
            bot.send_message(message.chat.id, "ID noto‘g‘ri ❌")
    else:
        bot.send_message(message.chat.id, "Sizga ruxsat yo‘q ❌")

# 🔹 Bot ishga tushishi
bot.infinity_polling()
