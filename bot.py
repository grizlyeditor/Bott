import telebot
import requests
import time
import threading

BOT_TOKEN = "8058667580:AAH3gUzPch6o0mylRliXzmgSACLmqivhlig"
ALLOWED_GROUP_ID = -1002765768239
like_request_tracker = {}

VIP_USERS = {7699347302,6204812537}

bot = telebot.TeleBot(BOT_TOKEN)

def call_api(region, uid):
    url = f"https://grizly2.vercel.app/like?uid={uid}&server_name={region}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200 or not response.text.strip():
            return "API_ERROR"
        return response.json()
    except (requests.exceptions.RequestException, requests.exceptions.JSONDecodeError):
        return "API_ERROR"

def process_like(message, region, uid):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if user_id not in VIP_USERS and like_request_tracker.get(user_id, False):
        bot.reply_to(message, "⚠️ You have exceeded your daily request limit! ⏳ Try again later.")
        return

    processing_msg = bot.reply_to(message, "⏳ Processing your request... 🔄")

    time.sleep(1)
    bot.edit_message_text("🔄 Fetching data from server... 10%", chat_id, processing_msg.message_id)
    time.sleep(1)
    bot.edit_message_text("🔄 Validating UID & Region... 30%", chat_id, processing_msg.message_id)
    time.sleep(1)
    bot.edit_message_text("🔄 Sending like request... 60%", chat_id, processing_msg.message_id)
    time.sleep(1)
    bot.edit_message_text("🔄 Almost Done... 90%", chat_id, processing_msg.message_id)

    response = call_api(region, uid)

    if response == "API_ERROR":
        bot.edit_message_text("🚨 API ERROR! ⚒️ We are fixing it, please wait for 8 hours. ⏳", chat_id, processing_msg.message_id)
        return

    if response.get("status") == 1:
        if user_id not in VIP_USERS:
            like_request_tracker[user_id] = True  # Mark usage

        try:
            photos = bot.get_user_profile_photos(user_id)
            if photos.total_count > 0:
                file_id = photos.photos[0][-1].file_id
                bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=processing_msg.message_id,
                    media=telebot.types.InputMediaPhoto(
                        file_id,
                        caption=f"✅ **Like Added Successfully!**\n"
                                f"🔹 **UID:** `{response.get('UID', 'N/A')}`\n"
                                f"🔸 **Player Nickname:** `{response.get('PlayerNickname', 'N/A')}`\n"
                                f"🔸 **Likes Before:** `{response.get('LikesbeforeCommand', 'N/A')}`\n"
                                f"🔸 **Likes After:** `{response.get('LikesafterCommand', 'N/A')}`\n"
                                f"🔸 **Likes By Bot:** `{response.get('LikesGivenByAPI', 'N/A')}`\n\n"
                                "🗿 **SHARE US FOR MORE:**\n https://youtube.com/@teamxcutehack",
                        parse_mode="Markdown"
                    )
                )
                return
        except:
            pass

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=processing_msg.message_id,
            text=f"✅ **Like Added Successfully!**\n"
                 f"🔹 **UID:** `{response.get('UID', 'N/A')}`\n"
                 f"🔸 **Player Nickname:** `{response.get('PlayerNickname', 'N/A')}`\n"
                 f"🔸 **Likes Before:** `{response.get('LikesbeforeCommand', 'N/A')}`\n"
                 f"🔸 **Likes After:** `{response.get('LikesafterCommand', 'N/A')}`\n"
                 f"🔸 **Likes By Bot:** `{response.get('LikesGivenByAPI', 'N/A')}`\n\n"
                 "🗿 **SHARE US FOR MORE:**\n https://youtube.com/@teamxcutehack",
            parse_mode="Markdown"
        )
    else:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=processing_msg.message_id,
            text=f"💔 UID `{uid}` has already received Max Likes for Today 💔.\n"
                 "🔄 Please Try a different UID.",
            parse_mode="Markdown"
        )

@bot.message_handler(commands=['like'])
def handle_like(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id != ALLOWED_GROUP_ID:
        bot.reply_to(message, "🚫 This group is not allowed to use this bot! ❌")
        return

    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "❌ Incorrect format! Use: `/like {region} {uid}`\n📌 Example: `/like ind 8385763215`", parse_mode="Markdown")
        return

    region, uid = args[1], args[2]

    if not region.isalpha() or not uid.isdigit():
        bot.reply_to(message, "⚠️ Invalid input! Region should be text and UID should be numbers.\n📌 Example: `/like ind 8385763215`")
        return

    threading.Thread(target=process_like, args=(message, region, uid)).start()

bot.polling(none_stop=True)