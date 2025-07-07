import telebot

TOKEN = "8128064097:AAEZpZ-XV660gElE_cHAl2QnIhvHM9O76Rs"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🤖 I'm alive 24/7 with lightning speed!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"🗣 You said: {message.text}")

bot.polling(non_stop=True)
