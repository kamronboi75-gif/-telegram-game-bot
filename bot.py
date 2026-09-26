import socket
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response for response in responses if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

import telebot
from telebot import types
from telebot.types import BotCommand
import random
import urllib.parse

TOKEN = "8883804985:AAHCnhjy6PndFebJkEsfxK6kzWqJL0nWc-M"
bot = telebot.TeleBot(TOKEN)
OWNER_ID = 6944908309

# --- MAJBURIY OBUNA KANALLARI ---
REQUIRED_CHANNELS = [-1003789167416, -1003722269634]
CHANNEL_LINKS = {
    -1003789167416: "https://t.me/+4jc2wCvxEE8yZTBi",
    -1003722269634: "https://t.me/boqijonvv"
}

def check_channels(user_id):
    if user_id == OWNER_ID:
        return True
    for chat_id in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(chat_id, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            return False
    return True

def send_sub_required(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📢 1-Kanalga obuna bo'lish", url=CHANNEL_LINKS[-1003789167416]),
        types.InlineKeyboardButton("📢 2-Kanalga obuna bo'lish", url=CHANNEL_LINKS[-1003722269634]),
        types.InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_sub")
    )
    bot.send_message(
        chat_id, 
        "⚠️ **Botdan foydalanish uchun quyidagi kanallarga obuna bo'lishingiz shart!**\n\n"
        "Kanallarga a'zo bo'lgach, **\"✅ Obunani tekshirish\"** tugmasini bosing.", 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_subscription(call):
    user_id = call.from_user.id
    if check_channels(user_id):
        bot.answer_callback_query(call.id, "✅ Obuna tasdiqlandi!")
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        start_command_executed(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ Siz hali barcha kanallarga obuna bo'lmadingiz!", show_alert=True)

# --------------------------------

bot.set_my_commands([
    BotCommand("start", "Botni ishga tushirish / Bosh sahifa")
])

users_data = {}
user_orders = {}
user_game_choice = {} 
user_bot_plan = {}    
apple_active_games = {} 

# Mortal Kombat uchun o'yinlar bazasi
mk_battles = {} 
mk_active_matches = {} 

MK_FIGHTERS = [
    "Scorpion 🔥", "Sub-Zero ❄️", "Liu Kang 🐉", "Raiden ⚡",
    "Kitana 👑", "Kung Lao 👒", "Baraka ⚔️", "Mileena 💜",
    "Shao Kahn 🔨", "Johnny Cage 🎬"
]

def check_user(user_id, name="Foydalanuvchi", username=None):
    if user_id not in users_data:
        initial_coin = 10000 if user_id == OWNER_ID else 500 
        initial_som = 1000000 if user_id == OWNER_ID else 0
        users_data[user_id] = {
            'name': name, 
            'username': username, 
            'coin_balance': initial_coin, 
            'som_balance': initial_som,
            'bonus_claimed': False, 
            'referred_by': None, 
            'pending_topup_type': 'So\'m'
        }
    else:
        if username:
            users_data[user_id]['username'] = username
        if 'som_balance' not in users_data[user_id]:
            users_data[user_id]['som_balance'] = 0
        if 'coin_balance' not in users_data[user_id]:
            users_data[user_id]['coin_balance'] = 500
    if user_id not in user_orders:
        user_orders[user_id] = []
    return True

def find_user_by_identifier(identifier):
    identifier = str(identifier).strip()
    if identifier.isdigit():
        u_id = int(identifier)
        if u_id in users_data:
            return u_id
    
    clean_username = identifier.lstrip('@').lower()
    for u_id, data in users_data.items():
        u_name = data.get('username')
        if u_name and u_name.lower() == clean_username:
            return u_id
    return None

def get_main_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("🎁 Bonus olish"),
        types.KeyboardButton("👥 Do'stlarni taklif qilish")
    )
    markup.add(
        types.KeyboardButton("🤖 O'z botingizni yarating"),
        types.KeyboardButton("👑 Premium olish")
    )
    markup.add(
        types.KeyboardButton("⭐ Stars olish")
    )
    markup.add(
        types.KeyboardButton("💵 Valyuta"),
        types.KeyboardButton("🌐 Telegram akkaunt")
    )
    markup.add(
        types.KeyboardButton("🛍 SMM xizmatlar"),
        types.KeyboardButton("🎮 Donat qilish")
    )
    markup.add(
        types.KeyboardButton("💰 Balans"),
        types.KeyboardButton("💰 Balans to'ldirish")
    )
    markup.add(
        types.KeyboardButton("🛍 Buyurtmalarim"),
        types.KeyboardButton("👤 Profil")
    )
    markup.add(
        types.KeyboardButton("🏆 Reyting"),
        types.KeyboardButton("🎲 1 Kishilik O'yinlar")
    )
    markup.add(
        types.KeyboardButton("👥 2 Kishilik O'yinlar"),
        types.KeyboardButton("⚔️ 2 Kishilik Mortal Kombat")
    )
    markup.add(
        types.KeyboardButton("⚠️ Yordam")
    )
    if user_id == OWNER_ID:
        markup.add(types.KeyboardButton("👑 Admin Statistika"))
    return markup

def is_menu_button(text):
    menu_texts = [
        "🎁 Bonus olish", "👥 Do'stlarni taklif qilish", "🤖 O'z botingizni yarating", 
        "👑 Premium olish", "⭐ Stars olish", "💵 Valyuta", 
        "🌐 Telegram akkaunt", "🛍 SMM xizmatlar", "🎮 Donat qilish", 
        "💰 Balans", "💰 Balans to'ldirish", "🛍 Buyurtmalarim", "👤 Profil", "🏆 Reyting", 
        "🎲 1 Kishilik O'yinlar", "👥 2 Kishilik O'yinlar", 
        "⚔️ 2 Kishilik Mortal Kombat", "⚠️ Yordam"
    ]
    return text in menu_texts or text.startswith('/')

def cancel_states(user_id):
    user_game_choice.pop(user_id, None)
    user_bot_plan.pop(user_id, None)
    apple_active_games.pop(user_id, None)

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    
    text = message.text
    if " " in text:
        param = text.split(" ")[1]
        if param.startswith("mk_"):
            creator_id = int(param.split("_")[1])
            if creator_id == user_id:
                bot.send_message(message.chat.id, "❌ O'zingiz ochgan o'yinga o'zingiz qo'shila olmaysiz!")
                start_command_executed(message)
                return
            if creator_id not in mk_battles:
                bot.send_message(message.chat.id, "❌ Bu jang allaqachon yakunlangan yoki bekor qilingan!")
                start_command_executed(message)
                return
            
            check_user(user_id)
            battle = mk_battles[creator_id]
            if users_data[user_id][battle['balance_key']] < battle['bet']:
                bot.send_message(message.chat.id, f"❌ Bu jangga kirish uchun balansingiz yetarli emas! (Kerak: {battle['bet']} {battle['curr_label']})")
                start_command_executed(message)
                return
            
            mk_active_matches[user_id] = creator_id
            markup = types.InlineKeyboardMarkup(row_width=2)
            for idx, f in enumerate(MK_FIGHTERS[:6]):
                markup.add(types.InlineKeyboardButton(f, callback_data=f"mk_join_fight_{idx}"))
            bot.send_message(message.chat.id, f"⚔️ **Mortal Kombat janga qo'shildingiz!**\n\nStavka: {battle['bet']} {battle['curr_label']}\nJangchingizni tanlang:", reply_markup=markup, parse_mode="Markdown")
            return

    start_command_executed(message)

def start_command_executed(message):
    user_id = message.from_user.id
    cancel_states(user_id)
    check_user(user_id, message.from_user.first_name, message.from_user.username)
    text = (
        f"🎮 **Gamer Botga xush kelibsiz!** 🎮\n\n"
        f"🪙 O'yin Coini: **{users_data[user_id]['coin_balance']}** coin\n"
        f"💵 So'm balans: **{users_data[user_id]['som_balance']}** so'm\n\n"
        f"🎁 Bonus olish uchun pastdagi **\"🎁 Bonus olish\"** tugmasini bosing!"
    )
    bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard(user_id), parse_mode="Markdown")

@bot.message_handler(commands=['add'])
def admin_add_coin(message):
    if message.from_user.id != OWNER_ID:
        return
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Xato format! Masalan: `/add @username 1000`", parse_mode="Markdown")
        return
    try:
        target_identifier = args[1]
        amount = int(args[2])
        target_id = find_user_by_identifier(target_identifier)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Foydalanuvchi topilmadi!")
            return
        users_data[target_id]['coin_balance'] += amount
        bot.send_message(message.chat.id, f"✅ O'yin coiniga {amount} qo'shildi!")
        bot.send_message(target_id, f"🎉 Admin o'yin coin balansingizni **{amount}** coin bilan to'ldirdi! 🪙", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik: {e}")

@bot.message_handler(commands=['addsom'])
def admin_add_som(message):
    if message.from_user.id != OWNER_ID:
        return
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Xato format! Masalan: `/addsom @username 40000`", parse_mode="Markdown")
        return
    try:
        target_identifier = args[1]
        amount = int(args[2])
        target_id = find_user_by_identifier(target_identifier)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Foydalanuvchi topilmadi!")
            return
        users_data[target_id]['som_balance'] += amount
        bot.send_message(message.chat.id, f"✅ So'm balansiga {amount} so'm qo'shildi!")
        bot.send_message(target_id, f"🎉 Admin so'm balansingizni **{amount} so'm** bilan to'ldirdi! 💵", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik: {e}")

@bot.message_handler(func=lambda m: m.text == "💰 Balans")
def check_my_balance(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    check_user(user_id, message.from_user.first_name, message.from_user.username)
    bot.send_message(
        message.chat.id, 
        f"💰 **Sizning balansingiz:**\n\n"
        f"🪙 O'yin coini: **{users_data[user_id]['coin_balance']}** coin\n"
        f"💵 So'm balans: **{users_data[user_id]['som_balance']}** so'm", 
        parse_mode="Markdown", 
        reply_markup=get_main_keyboard(user_id)
    )

@bot.message_handler(func=lambda m: m.text == "🏆 Reyting")
def show_leaderboard(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    check_user(user_id, message.from_user.first_name, message.from_user.username)
    sorted_users = sorted(users_data.items(), key=lambda x: x[1]['coin_balance'], reverse=True)
    text = "🏆 **Top 10 O'yinchilar (Coin bo'yicha):**\n\n"
    for i, (u_id, u_data) in enumerate(sorted_users[:10], 1):
        text += f"{i}. {u_data.get('name', 'User')} — 🪙 {u_data.get('coin_balance', 0)} coin\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_keyboard(user_id))

@bot.message_handler(func=lambda m: m.text == "🎁 Bonus olish")
def get_bonus(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    check_user(user_id, message.from_user.first_name, message.from_user.username)
    if users_data[user_id]['bonus_claimed']:
        bot.send_message(message.chat.id, "❌ Siz bonusni allaqachon olgansiz!", reply_markup=get_main_keyboard(user_id))
    else:
        users_data[user_id]['bonus_claimed'] = True
        users_data[user_id]['coin_balance'] += 50
        bot.send_message(message.chat.id, f"🎉 50 o'yin coini bonus berildi! Balans: {users_data[user_id]['coin_balance']} coin", reply_markup=get_main_keyboard(user_id))

@bot.message_handler(func=lambda m: m.text == "👥 Do'stlarni taklif qilish")
def invite(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    _bot = bot.get_me()
    ref_link = f"https://t.me/{_bot.username}?start=ref_{user_id}"
    bot.send_message(message.chat.id, f"👥 Do'stlarni taklif qiling va 20 o'yin coini oling!\n\n🔗 Havolangiz:\n`{ref_link}`", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "👤 Profil")
def profile(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    check_user(user_id, message.from_user.first_name, message.from_user.username)
    bot.send_message(
        message.chat.id, 
        f"👤 **Profil**\n🆔 ID: `{user_id}`\n🪙 O'yin coini: **{users_data[user_id]['coin_balance']}** coin\n💵 So'm balans: **{users_data[user_id]['som_balance']}** so'm", 
        parse_mode="Markdown", 
        reply_markup=get_main_keyboard(user_id)
    )

@bot.message_handler(func=lambda m: m.text == "🛍 Buyurtmalarim")
def orders(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    ord_list = user_orders.get(user_id, [])
    if not ord_list:
        bot.send_message(message.chat.id, "📦 Buyurtmalar mavjud emas.", reply_markup=get_main_keyboard(user_id))
        return
    text = "🛍 **Sizning buyurtmalaringiz:**\n"
    for o in ord_list:
        text += f"- {o['item']} ({o['cost']})\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_keyboard(user_id))

@bot.message_handler(func=lambda m: m.text == "👑 Admin Statistika")
def stats(message):
    if message.from_user.id != OWNER_ID:
        return
    cancel_states(message.from_user.id)
    bot.send_message(message.chat.id, f"👥 Foydalanuvchilar: {len(users_data)} ta\n🪙 Jami coin: {sum(u['coin_balance'] for u in users_data.values())}\n💵 Jami so'm: {sum(u['som_balance'] for u in users_data.values())}")

@bot.message_handler(func=lambda m: m.text == "💰 Balans to'ldirish")
def balance_topup_menu(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    check_user(user_id, message.from_user.first_name, message.from_user.username)
    
    _bot = bot.get_me()
    bot_username = _bot.username
    msg_text = f"Salom men @{bot_username} balansini so'm orqali to'ldirmoqchiman. Iltimos karta tashlang.\n\nID: {user_id}"
    admin_url = f"https://t.me/Hellobroooooo0?text={urllib.parse.quote(msg_text)}"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 Adminga karta so'rovini yuborish", url=admin_url))
    
    card_text = (
        "💳 **Balansni to'ldirish (So'm):**\n\n"
        "Karta raqamini olish uchun pastdagi tugmani bosing.\n\n"
        "⚠️ Pulni o'tkazgach, **to'lov cheki (skrinshot)ni shu botga rasm ko'rinishida yuboring!**"
    )
    bot.send_message(message.chat.id, card_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🛍 SMM xizmatlar")
def smm_menu(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    _bot = bot.get_me()
    admin_url = f"https://t.me/Hellobroooooo0?text={urllib.parse.quote(f'Salom men @{_bot.username} orqali 1000 ta ko\'rish (SMM) xarid qilmoqchiman. ID: {message.from_user.id}')}"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👁 1000 Ko'rish — 5,000 so'm (Karta orqali)", url=admin_url))
    bot.send_message(message.chat.id, "🛍 **SMM xizmatlar bo'limi:**", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "👑 Premium olish")
def premium_menu(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    _bot = bot.get_me()
    
    url_1 = f"https://t.me/Hellobroooooo0?text={urllib.parse.quote(f'Salom men @{_bot.username} orqali 1 oylik premium (50,000 so\'m) xarid qilmoqchiman. Akauntga kirib olinadi. ID: {user_id}')}"
    url_3 = f"https://t.me/Hellobroooooo0?text={urllib.parse.quote(f'Salom men @{_bot.username} orqali 3 oylik premium (180,000 so\'m) xarid qilmoqchiman. Akauntga kirib olinadi. ID: {user_id}')}"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("👑 1 oylik — 50,000 so'm (Akauntga kirib)", url=url_1),
        types.InlineKeyboardButton("👑 3 oylik — 180,000 so'm (Akauntga kirib)", url=url_3)
    )
    bot.send_message(message.chat.id, "👑 **Telegram Premium do'koni:**\n(Akauntga kirib beriladi)", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "⭐ Stars olish")
def stars_menu(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    _bot = bot.get_me()
    admin_url = f"https://t.me/Hellobroooooo0?text={urllib.parse.quote(f'Salom men @{_bot.username} orqali 50 Stars xarid qilmoqchiman. ID: {message.from_user.id}')}"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⭐ 50 Stars — 10,000 so'm (Karta orqali)", url=admin_url))
    bot.send_message(message.chat.id, "⭐ **Stars do'koni:**", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text in ["💵 Valyuta", "🌐 Telegram akkaunt", "⚠️ Yordam"])
def handle_menu_sections(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    check_user(user_id, message.from_user.first_name, message.from_user.username)
    text = message.text
    
    if text == "💵 Valyuta":
        bot.send_message(message.chat.id, "💵 Xizmatlar so'm orqali, o'yinlarni esa xoh Coin xoh So'm orqali o'ynashingiz mumkin!", parse_mode="Markdown")
    elif text == "🌐 Telegram akkaunt":
        bot.send_message(message.chat.id, "🌐 Tez kunda qo'shiladi!", parse_mode="Markdown")
    elif text == "⚠️ Yordam":
        bot.send_message(message.chat.id, "⚠️ Muammolar bo'yicha adminga murojaat qiling.", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🎮 Donat qilish")
def donat_menu(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    _bot = bot.get_me()
    admin_url = f"https://t.me/Hellobroooooo0?text={urllib.parse.quote(f'Salom men @{_bot.username} orqali 60 UC (13,000 so\'m) xarid qilmoqchiman. ID: {message.from_user.id}')}"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 60 UC — 13,000 so'm (Karta orqali)", url=admin_url))
    bot.send_message(message.chat.id, "🎮 **Donat qilish bo'limi (PUBG UC):**", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_payment_screenshot(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    check_user(user_id, message.from_user.first_name, message.from_user.username)
    
    bot.reply_to(message, "✅ Chekingiz qabul qilindi!\n\nAdmin tez orada tekshirib balansingizni to'ldiradi!")
    
    try:
        safe_name = str(message.from_user.first_name).replace('*', '').replace('_', '').replace('`', '')
        bot.send_message(
            OWNER_ID,
            f"🧾 YANGI TO'LOV CHEKI!\n\n"
            f"👤 Foydalanuvchi: @{message.from_user.username or 'Yoq'} ({safe_name})\n"
            f"🆔 ID: {user_id}\n\n"
            f"So'm qo'shish uchun: /addsom {user_id} [miqdor]"
        )
        bot.copy_message(chat_id=OWNER_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print(f"Adminga yuborishda xatolik: {e}")

@bot.message_handler(func=lambda m: m.text == "🤖 O'z botingizni yarating")
def create_bot_menu(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    _bot = bot.get_me()
    bot_username = _bot.username
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    url_15 = f"https://t.me/Hellobroooooo0?text={urllib.parse.quote(f'Salom men @{bot_username} orqali 15 kunlik bot yaratish tarifini xarid qilmoqchiman. ID: {user_id}')}"
    url_31 = f"https://t.me/Hellobroooooo0?text={urllib.parse.quote(f'Salom men @{bot_username} orqali 31 kunlik bot yaratish tarifini xarid qilmoqchiman. ID: {user_id}')}"
    
    markup.add(
        types.InlineKeyboardButton("⏳ 15 kunlik bot — 22,000 so'm", url=url_15),
        types.InlineKeyboardButton("⏳ 31 kunlik bot — 57,000 so'm", url=url_31),
        types.InlineKeyboardButton("🤖 Bot tokenini kiritish", callback_data="buy_bot_token_flow")
    )
    bot.send_message(message.chat.id, "🤖 **Bot yaratish bo'limi:**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "buy_bot_token_flow")
def ask_bot_plan_flow(call):
    user_id = call.from_user.id
    if not check_channels(user_id):
        send_sub_required(call.message.chat.id)
        return
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("⏳ 15 kunlik bot — 22,000 so'm", callback_data="buy_bot_15"),
        types.InlineKeyboardButton("⏳ 31 kunlik bot — 57,000 so'm", callback_data="buy_bot_31")
    )
    bot.edit_message_text("Tarifni tanlang:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_bot_"))
def buy_bot_plan(call):
    user_id = call.from_user.id
    if not check_channels(user_id):
        send_sub_required(call.message.chat.id)
        return
    check_user(user_id)
    plan = call.data.split("_")[2]
    days = "15 kunlik" if plan == "15" else "31 kunlik"
    price = "22,000 so'm" if plan == "15" else "57,000 so'm"
    user_bot_plan[user_id] = {"days": days, "price": price}
    bot.answer_callback_query(call.id, "Tarif tanlandi!")
    msg = bot.send_message(call.message.chat.id, f"✅ Siz **{days}** tarifini tanladingiz (**{price}**).\n\n🤖 Bot tokenini yuboring:", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_bot_token)

def process_bot_token(message):
    user_id = message.from_user.id
    if is_menu_button(message.text):
        cancel_states(user_id)
        bot.send_message(message.chat.id, "❌ Amaliyot bekor qilindi. Asosiy menyudasiz.", reply_markup=get_main_keyboard(user_id))
        return

    if user_id not in user_bot_plan:
        return
    token_text = message.text.strip()
    plan_info = user_bot_plan[user_id]
    
    if ":" not in token_text or len(token_text) < 20:
        msg = bot.send_message(message.chat.id, "❌ Noto'g'ri token formati! Qaytadan yuboring:")
        bot.register_next_step_handler(msg, process_bot_token)
        return
        
    user_orders[user_id].append({"item": f"🤖 Bot yaratish ({plan_info['days']})", "cost": plan_info['price']})
    bot.send_message(message.chat.id, f"🎉 **Token qabul qilindi!**\nAdmin tasdiqlagach botingiz ishga tushadi! 🚀", parse_mode="Markdown", reply_markup=get_main_keyboard(user_id))
    
    try:
        bot.send_message(OWNER_ID, f"🚨 YANGI BOT TOKENI!\nID: {user_id}\nTarif: {plan_info['days']}\nToken: {token_text}")
    except Exception as e:
        print(f"Adminga yuborishda xatolik: {e}")
    user_bot_plan.pop(user_id, None)

# --- O'YINLAR ---

@bot.message_handler(func=lambda m: m.text == "🎲 1 Kishilik O'yinlar")
def games_1(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(message.from_user.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎲 Zar", callback_data="p1_dice"),
        types.InlineKeyboardButton("🎯 Darts", callback_data="p1_darts"),
        types.InlineKeyboardButton("🏀 Basketbol", callback_data="p1_basket"),
        types.InlineKeyboardButton("⚽ Futbol", callback_data="p1_football"),
        types.InlineKeyboardButton("🍎 Olma o'yini", callback_data="p1_apple")
    )
    bot.send_message(message.chat.id, "🎲 1 kishilik o'yin turini tanlang:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("p1_"))
def p1_select_currency(call):
    user_id = call.from_user.id
    if not check_channels(user_id):
        send_sub_required(call.message.chat.id)
        return
    check_user(user_id)
    game_type = call.data.split("_")[1]
    user_game_choice[user_id] = {"game": game_type}
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🪙 Coin bilan", callback_data="cur_coin_p1"),
        types.InlineKeyboardButton("💵 So'm bilan", callback_data="cur_som_p1")
    )
    bot.edit_message_text("Valyuta turini tanlang:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["cur_coin_p1", "cur_som_p1"])
def p1_ask_bet(call):
    user_id = call.from_user.id
    if not check_channels(user_id):
        send_sub_required(call.message.chat.id)
        return
    if user_id not in user_game_choice:
        return
    currency = "coin" if call.data == "cur_coin_p1" else "som"
    user_game_choice[user_id]['currency'] = currency
    
    curr_name = "coin" if currency == "coin" else "so'm"
    min_bet = 50 if currency == "coin" else 5000
    
    msg = bot.send_message(call.message.chat.id, f"💰 Qancha **{curr_name}** tikmoqchisiz? (Minimal {min_bet}):", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_p1_game)

def process_p1_game(message):
    user_id = message.from_user.id
    if is_menu_button(message.text):
        cancel_states(user_id)
        bot.send_message(message.chat.id, "❌ O'yin bekor qilindi. Asosiy menyudasiz.", reply_markup=get_main_keyboard(user_id))
        return

    check_user(user_id)
    if user_id not in user_game_choice:
        return
    choice_info = user_game_choice[user_id]
    game_type = choice_info['game']
    currency = choice_info.get('currency', 'coin')
    balance_key = 'coin_balance' if currency == 'coin' else 'som_balance'
    min_bet = 50 if currency == 'coin' else 5000
    curr_label = 'coin' if currency == 'coin' else 'so\'m'
    
    try:
        bet = int(message.text)
    except ValueError:
        msg = bot.send_message(message.chat.id, "❌ Faqat raqam kiriting (yoki boshqa menyu tugmasini bosing):")
        bot.register_next_step_handler(msg, process_p1_game)
        return
        
    if bet < min_bet:
        msg = bot.send_message(message.chat.id, f"❌ Minimal tikish {min_bet} {curr_label}! Qaytadan kiriting:")
        bot.register_next_step_handler(msg, process_p1_game)
        return
        
    if users_data[user_id][balance_key] < bet:
        bot.send_message(message.chat.id, f"❌ Balansingiz yetarli emas!", reply_markup=get_main_keyboard(user_id))
        user_game_choice.pop(user_id, None)
        return
        
    users_data[user_id][balance_key] -= bet
    
    if game_type == "apple":
        apple_active_games[user_id] = {
            "bet": bet,
            "currency": currency,
            "balance_key": balance_key,
            "curr_label": curr_label,
            "current_row": 0,
            "total_rows": 5
        }
        bot.send_message(
            message.chat.id,
            f"🍎 **Apple of Fortune (Olma o'yini)**\n\n"
            f"• Tikish: {bet} {curr_label}\n"
            f"• 5 ta qator, har birida 2 ta olma 🍎 va 3 ta mina 💣\n\n"
            f"1-qatordan xavfsiz katakni tanlang:",
            reply_markup=get_apple_keyboard(0),
            parse_mode="Markdown"
        )
        user_game_choice.pop(user_id, None)
        return

    emoji_map = {"dice": "🎲", "darts": "🎯", "basket": "🏀", "football": "⚽"}
    sent_dice = bot.send_dice(message.chat.id, emoji=emoji_map.get(game_type, "🎲"))
    val = sent_dice.dice.value
    
    if val >= 4:
        reward = bet * 2
        users_data[user_id][balance_key] += reward
        bot.send_message(message.chat.id, f"🎉 **Yutdingiz! +{reward} {curr_label}**\n💵 Balans: {users_data[user_id][balance_key]} {curr_label}", parse_mode="Markdown", reply_markup=get_main_keyboard(user_id))
    else:
        bot.send_message(message.chat.id, f"😔 **Yutqazdingiz.** -{bet} {curr_label}\n💵 Balans: {users_data[user_id][balance_key]} {curr_label}", parse_mode="Markdown", reply_markup=get_main_keyboard(user_id))
        
    user_game_choice.pop(user_id, None)

def get_apple_keyboard(row_index):
    markup = types.InlineKeyboardMarkup(row_width=5)
    buttons = []
    for i in range(5):
        buttons.append(types.InlineKeyboardButton(f"❓ {row_index+1}.{i+1}", callback_data=f"apple_choice_{row_index}_{i}"))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("💰 Yutuqni olish (To'xtatish)", callback_data="apple_stop"))
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith("apple_choice_") or call.data == "apple_stop")
def apple_game_process(call):
    user_id = call.from_user.id
    if user_id not in apple_active_games:
        bot.answer_callback_query(call.id, "O'yin topilmadi yoki tugagan!", show_alert=True)
        return
        
    game = apple_active_games[user_id]
    
    if call.data == "apple_stop":
        current_row = game["current_row"]
        bet = game["bet"]
        currency_key = game["balance_key"]
        curr_label = game["curr_label"]
        
        if current_row == 0:
            users_data[user_id][currency_key] += bet
            apple_active_games.pop(user_id, None)
            bot.edit_message_text(f"🏁 O'yin to'xtatildi. Tikilgan {bet} {curr_label} qaytarildi.", call.message.chat.id, call.message.message_id, reply_markup=get_main_keyboard(user_id))
        else:
            multipliers = [1.25, 1.56, 1.97, 2.46, 3.05]
            mult = multipliers[current_row - 1]
            reward = int(bet * mult)
            users_data[user_id][currency_key] += reward
            apple_active_games.pop(user_id, None)
            bot.edit_message_text(
                f"💰 **O'yin to'xtatildi!**\n\n"
                f"🎉 Yutuq: **+{reward} {curr_label}** ({mult}x)\n"
                f"💵 Balans: {users_data[user_id][currency_key]} {curr_label}",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_main_keyboard(user_id),
                parse_mode="Markdown"
            )
        return
        
    parts = call.data.split("_")
    row_idx = int(parts[2])
    col_idx = int(parts[3])
    
    if row_idx != game["current_row"]:
        bot.answer_callback_query(call.id, "Hozir bu qatorda emassiz!", show_alert=True)
        return
        
    random.seed(user_id + row_idx * 999)
    mines = random.sample(range(5), 3)
    
    bet = game["bet"]
    currency_key = game["balance_key"]
    curr_label = game["curr_label"]
    
    if col_idx in mines:
        apple_active_games.pop(user_id, None)
        bot.edit_message_text(
            f"💥 **Mina chiqdi! Yutqazdingiz.**\n\n"
            f"-{bet} {curr_label}\n"
            f"💵 Balans: {users_data[user_id][currency_key]} {curr_label}",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_main_keyboard(user_id),
            parse_mode="Markdown"
        )
    else:
        game["current_row"] += 1
        multipliers = [1.25, 1.56, 1.97, 2.46, 3.05]
        
        if game["current_row"] >= game["total_rows"]:
            mult = multipliers[-1]
            reward = int(bet * mult)
            users_data[user_id][currency_key] += reward
            apple_active_games.pop(user_id, None)
            bot.edit_message_text(
                f"🎉 **Tabriklaymiz! Barcha 5 ta qatordan o'tdingiz!** 🏆\n\n"
                f"Koeffitsiyent: {mult}x\n"
                f"Yutuq: **+{reward} {curr_label}**\n"
                f"💵 Balans: {users_data[user_id][currency_key]} {curr_label}",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_main_keyboard(user_id),
                parse_mode="Markdown"
            )
        else:
            next_row = game["current_row"]
            curr_mult = multipliers[next_row - 1]
            bot.edit_message_text(
                f"✅ **To'g'ri! Olma chiqdi 🍎**\n\n"
                f"Hozirgi koeffitsiyent: **{curr_mult}x**\n"
                f"Keyingi ({next_row + 1})-qatorni tanlang:",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_apple_keyboard(next_row),
                parse_mode="Markdown"
            )

# --- 2 KISHILIK BOSHQA O'YINLAR ---

@bot.message_handler(func=lambda m: m.text == "👥 2 Kishilik O'yinlar")
def games_2(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(message.from_user.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("❌⭕ X-0", callback_data="game_tictactoe"),
        types.InlineKeyboardButton("🃏 21 (Ochko)", callback_data="game_21"),
        types.InlineKeyboardButton("✊ Tosh-Qaychi-Qog'oz", callback_data="game_rps")
    )
    bot.send_message(message.chat.id, "👥 2 kishilik o'yinni tanlang:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data in ["game_tictactoe", "game_21", "game_rps"])
def select_2p_currency(call):
    user_id = call.from_user.id
    if not check_channels(user_id):
        send_sub_required(call.message.chat.id)
        return
    check_user(user_id)
    game_key = call.data
    user_game_choice[user_id] = {"game": game_key}
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🪙 Coin bilan", callback_data="cur_coin_2p"),
        types.InlineKeyboardButton("💵 So'm bilan", callback_data="cur_som_2p")
    )
    bot.edit_message_text("Valyuta turini tanlang:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["cur_coin_2p", "cur_som_2p"])
def ask_2p_bet(call):
    user_id = call.from_user.id
    if not check_channels(user_id):
        send_sub_required(call.message.chat.id)
        return
    if user_id not in user_game_choice:
        return
    currency = "coin" if call.data == "cur_coin_2p" else "som"
    user_game_choice[user_id]['currency'] = currency
    
    curr_name = "coin" if currency == "coin" else "so'm"
    min_bet = 50 if currency == "coin" else 5000
    
    msg = bot.send_message(call.message.chat.id, f"💰 Qancha **{curr_name}** tikmoqchisiz? (Minimal {min_bet}):", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_2p_game_start)

def process_2p_game_start(message):
    user_id = message.from_user.id
    if is_menu_button(message.text):
        cancel_states(user_id)
        bot.send_message(message.chat.id, "❌ O'yin bekor qilindi. Asosiy menyudasiz.", reply_markup=get_main_keyboard(user_id))
        return

    check_user(user_id)
    if user_id not in user_game_choice:
        return
    choice_info = user_game_choice[user_id]
    game_key = choice_info['game']
    currency = choice_info.get('currency', 'coin')
    balance_key = 'coin_balance' if currency == 'coin' else 'som_balance'
    min_bet = 50 if currency == 'coin' else 5000
    curr_label = 'coin' if currency == 'coin' else 'so\'m'
    
    try:
        bet = int(message.text)
    except ValueError:
        msg = bot.send_message(message.chat.id, "❌ Faqat raqam kiriting:")
        bot.register_next_step_handler(msg, process_2p_game_start)
        return
        
    if bet < min_bet:
        msg = bot.send_message(message.chat.id, f"❌ Minimal tikish {min_bet} {curr_label}:")
        bot.register_next_step_handler(msg, process_2p_game_start)
        return
        
    if users_data[user_id][balance_key] < bet:
        bot.send_message(message.chat.id, f"❌ Balansingiz yetarli emas!", reply_markup=get_main_keyboard(user_id))
        user_game_choice.pop(user_id, None)
        return
        
    users_data[user_id][balance_key] -= bet
    
    if game_key == "game_21":
        user_score = random.randint(14, 21)
        bot_score = random.randint(15, 23)
        if bot_score > 21 or user_score > bot_score:
            reward = bet * 2
            users_data[user_id][balance_key] += reward
            bot.send_message(message.chat.id, f"🃏 Siz: {user_score} | Bot: {bot_score}\n🎉 **Yutdingiz! +{reward} {curr_label}**\n💵 Balans: {users_data[user_id][balance_key]} {curr_label}", parse_mode="Markdown", reply_markup=get_main_keyboard(user_id))
        else:
            bot.send_message(message.chat.id, f"🃏 Siz: {user_score} | Bot: {bot_score}\n😔 **Yutqazdingiz!** -{bet} {curr_label}\n💵 Balans: {users_data[user_id][balance_key]} {curr_label}", parse_mode="Markdown", reply_markup=get_main_keyboard(user_id))
            
    elif game_key == "game_rps":
        users_data[user_id]['temp_bet'] = bet
        users_data[user_id]['temp_currency'] = currency
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton("✊ Tosh", callback_data="rps_tosh"),
            types.InlineKeyboardButton("✌️ Qaychi", callback_data="rps_qaychi"),
            types.InlineKeyboardButton("✋ Qog'oz", callback_data="rps_qogoz")
        )
        bot.send_message(message.chat.id, f"✊ **Tosh-Qaychi-Qog'oz** (Tikish: {bet} {curr_label})", reply_markup=markup, parse_mode="Markdown")
        
    elif game_key == "game_tictactoe":
        res = random.choice(["win", "draw", "lose"])
        if res == "win":
            reward = bet * 2
            users_data[user_id][balance_key] += reward
            bot.send_message(message.chat.id, f"🎉 G'alaba! +{reward} {curr_label}\n💵 Balans: {users_data[user_id][balance_key]} {curr_label}", parse_mode="Markdown", reply_markup=get_main_keyboard(user_id))
        elif res == "draw":
            users_data[user_id][balance_key] += bet
            bot.send_message(message.chat.id, f"🤝 Durrang! {bet} {curr_label} qaytarildi.", reply_markup=get_main_keyboard(user_id))
        else:
            bot.send_message(message.chat.id, f"😔 Mag'lubiyat. -{bet} {curr_label}\n💵 Balans: {users_data[user_id][balance_key]} {curr_label}", parse_mode="Markdown", reply_markup=get_main_keyboard(user_id))
            
    if game_key != "game_rps":
        user_game_choice.pop(user_id, None)

@bot.callback_query_handler(func=lambda call: call.data.startswith("rps_"))
def rps_play(call):
    user_id = call.from_user.id
    if not check_channels(user_id):
        send_sub_required(call.message.chat.id)
        return
    check_user(user_id)
    user_choice = call.data.split("_")[1]
    bet = users_data[user_id].get('temp_bet', 50)
    currency = users_data[user_id].get('temp_currency', 'coin')
    balance_key = 'coin_balance' if currency == 'coin' else 'som_balance'
    curr_label = 'coin' if currency == 'coin' else 'so\'m'
    
    choices = ["tosh", "qaychi", "qogoz"]
    bot_choice = random.choice(choices)
    
    if user_choice == bot_choice:
        users_data[user_id][balance_key] += bet
        res_text = f"🤝 **Durrang!** {bet} {curr_label} qaytarildi."
    elif (user_choice == "tosh" and bot_choice == "qaychi") or (user_choice == "qaychi" and bot_choice == "qogoz") or (user_choice == "qogoz" and bot_choice == "tosh"):
        reward = bet * 2
        users_data[user_id][balance_key] += reward
        res_text = f"🎉 **Yutdingiz! +{reward} {curr_label}**"
    else:
        res_text = f"😔 **Bot yutdi!** -{bet} {curr_label}"
        
    bot.send_message(call.message.chat.id, f"{res_text}\n💵 Balans: {users_data[user_id][balance_key]} {curr_label}", parse_mode="Markdown", reply_markup=get_main_keyboard(user_id))
    user_game_choice.pop(user_id, None)

# --- 2 KISHILIK MORTAL KOMBAT ---

@bot.message_handler(func=lambda m: m.text == "⚔️ 2 Kishilik Mortal Kombat")
def mk_menu(message):
    user_id = message.from_user.id
    if not check_channels(user_id):
        send_sub_required(message.chat.id)
        return
    cancel_states(user_id)
    check_user(user_id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🪙 Coin bilan", callback_data="mk_cur_coin"),
        types.InlineKeyboardButton("💵 So'm bilan", callback_data="mk_cur_som")
    )
    bot.send_message(message.chat.id, "⚔️ **Mortal Kombat Arena (Do'st bilan o'ynash)!**\n\nValyuta turini tanlang:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data in ["mk_cur_coin", "mk_cur_som"])
def mk_ask_bet(call):
    user_id = call.from_user.id
    if not check_channels(user_id):
        send_sub_required(call.message.chat.id)
        return
    check_user(user_id)
    currency = "coin" if call.data == "mk_cur_coin" else "som"
    user_game_choice[user_id] = {"game": "mk", "currency": currency}
    
    curr_name = "coin" if currency == "coin" else "so'm"
    min_bet = 50 if currency == "coin" else 5000
    
    msg = bot.send_message(call.message.chat.id, f"💰 Qancha **{curr_name}** tikmoqchisiz? (Minimal {min_bet}):", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_mk_bet_amount)

def process_mk_bet_amount(message):
    user_id = message.from_user.id
    if is_menu_button(message.text):
        cancel_states(user_id)
        bot.send_message(message.chat.id, "❌ O'yin bekor qilindi. Asosiy menyudasiz.", reply_markup=get_main_keyboard(user_id))
        return

    check_user(user_id)
    if user_id not in user_game_choice:
        return
    choice_info = user_game_choice[user_id]
    currency = choice_info['currency']
    min_bet = 50 if currency == "coin" else 5000
    balance_key = 'coin_balance' if currency == "coin" else 'som_balance'
    curr_label = 'coin' if currency == "coin" else 'so\'m'
    
    try:
        bet = int(message.text)
    except ValueError:
        msg = bot.send_message(message.chat.id, "❌ Faqat raqam kiriting:")
        bot.register_next_step_handler(msg, process_mk_bet_amount)
        return
        
    if bet < min_bet:
        msg = bot.send_message(message.chat.id, f"❌ Minimal tikish {min_bet} {curr_label}:")
        bot.register_next_step_handler(msg, process_mk_bet_amount)
        return
        
    if users_data[user_id][balance_key] < bet:
        bot.send_message(message.chat.id, f"❌ Balansingiz yetarli emas!", reply_markup=get_main_keyboard(user_id))
        user_game_choice.pop(user_id, None)
        return
        
    users_data[user_id][balance_key] -= bet
    users_data[user_id]['mk_bet'] = bet
    users_data[user_id]['mk_currency'] = currency
    users_data[user_id]['balance_key'] = balance_key
    users_data[user_id]['curr_label'] = curr_label
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    for idx, f in enumerate(MK_FIGHTERS[:6]):
        markup.add(types.InlineKeyboardButton(f, callback_data=f"mk_creator_fight_{idx}"))
    bot.send_message(message.chat.id, "⚔️ O'z jangchingizni tanlang:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("mk_creator_fight_"))
def mk_creator_chosen(call):
    user_id = call.from_user.id
    if not check_channels(user_id):
        send_sub_required(call.message.chat.id)
        return
    check_user(user_id)
    fighter_idx = int(call.data.split("_")[3])
    fighter = MK_FIGHTERS[fighter_idx]
    
    bet = users_data[user_id].get('mk_bet', 50)
    currency = users_data[user_id].get('mk_currency', 'coin')
    balance_key = users_data[user_id].get('balance_key', 'coin_balance')
    curr_label = users_data[user_id].get('curr_label', 'coin')
    
    mk_battles[user_id] = {
        'bet': bet,
        'currency': currency,
        'balance_key': balance_key,
        'curr_label': curr_label,
        'fighter1': fighter,
        'creator_id': user_id
    }
    
    _bot = bot.get_me()
    invite_link = f"https://t.me/{_bot.username}?start=mk_{user_id}"
    share_url = f"https://t.me/share/url?url={urllib.parse.quote(invite_link)}&text={urllib.parse.quote(f'⚔️ Meni Mortal Kombat jangiga chaqirishdi! Stavka: {bet} {curr_label}. Qo\'shilish uchun bosing:')}"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("👥 Do'stga yuborish (Ulashish)", url=share_url))
    
    bot.edit_message_text(
        f"✅ Jangchi tanlandi: **{fighter}**\n"
        f"💰 Stavka: **{bet} {curr_label}**\n\n"
        f"🔗 Endi pastdagi tugmani bosib, bu turni **do'stingizga yuboring**. Do'stingiz havolani bosib jangga qo'shilgach, g'olib aniqlanadi!",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    user_game_choice.pop(user_id, None)

@bot.callback_query_handler(func=lambda call: call.data.startswith("mk_join_fight_"))
def mk_friend_chosen(call):
    friend_id = call.from_user.id
    if not check_channels(friend_id):
        send_sub_required(call.message.chat.id)
        return
    check_user(friend_id)
    
    if friend_id not in mk_active_matches:
        bot.answer_callback_query(call.id, "❌ Xatolik yuz berdi!", show_alert=True)
        return
        
    creator_id = mk_active_matches[friend_id]
    if creator_id not in mk_battles:
        bot.answer_callback_query(call.id, "❌ Bu jang tugagan yoki bekor qilingan!", show_alert=True)
        return
        
    battle = mk_battles[creator_id]
    bet = battle['bet']
    balance_key = battle['balance_key']
    curr_label = battle['curr_label']
    
    if users_data[friend_id][balance_key] < bet:
        bot.answer_callback_query(call.id, "❌ Balansingiz yetarli emas!", show_alert=True)
        return
        
    users_data[friend_id][balance_key] -= bet
    
    fighter_idx = int(call.data.split("_")[3])
    friend_fighter = MK_FIGHTERS[fighter_idx]
    creator_fighter = battle['fighter1']
    
    winner_id = random.choice([creator_id, friend_id])
    reward = bet * 2
    
    if winner_id == creator_id:
        users_data[creator_id][balance_key] += reward
        creator_text = f"⚔️ Siz ({creator_fighter}) vs Do'stingiz ({friend_fighter})\n🎉 **G'alaba qozundingiz! +{reward} {curr_label}**\n💵 Balans: {users_data[creator_id][balance_key]} {curr_label}"
        friend_text = f"⚔️ Siz ({friend_fighter}) vs Do'stingiz ({creator_fighter})\n😔 **Mag'lubiyat!** -{bet} {curr_label}\n💵 Balans: {users_data[friend_id][balance_key]} {curr_label}"
    else:
        users_data[friend_id][balance_key] += reward
        creator_text = f"⚔️ Siz ({creator_fighter}) vs Do'stingiz ({friend_fighter})\n😔 **Mag'lubiyat!** -{bet} {curr_label}\n💵 Balans: {users_data[creator_id][balance_key]} {curr_label}"
        friend_text = f"⚔️ Siz ({friend_fighter}) vs Do'stingiz ({creator_fighter})\n🎉 **G'alaba qozundingiz! +{reward} {curr_label}**\n💵 Balans: {users_data[friend_id][balance_key]} {curr_label}"
        
    bot.edit_message_text(friend_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=get_main_keyboard(friend_id))
    try:
        bot.send_message(creator_id, creator_text, parse_mode="Markdown", reply_markup=get_main_keyboard(creator_id))
    except:
        pass
        
    mk_battles.pop(creator_id, None)
    mk_active_matches.pop(friend_id, None)

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    bot.polling(none_stop=True)
