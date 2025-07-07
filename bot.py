import telebot

TOKEN = "8128064097:AAEZpZ-XV660gElE_cHAl2QnIhvHM9O76Rs"
bot = telebot.TeleBot(TOKEN)

# Force remove webhook in case it was set
bot.remove_webhook()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "✅ Bot is running 24/7!")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, f"You said: {message.text}")

# Use non-stop polling (only one instance)
bot.polling(non_stop=True)
