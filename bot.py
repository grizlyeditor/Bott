import telebot

TOKEN = "8128064097:AAEZpZ-XV660gElE_cHAl2QnIhvHM9O76Rs"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "🤖 I'm online 24/7!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"You said: {message.text}")

bot.polling(non_stop=True)
