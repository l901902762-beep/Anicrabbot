from telebot import TeleBot
from keep_alive import keep_alive

keep_alive()

BOT_TOKEN = "8499334154:AAFBIypA5xDdvbwkW50mt7RZiPBcMutmBvw"
bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "👋 Bot ishlayapti!")

bot.infinity_polling()
