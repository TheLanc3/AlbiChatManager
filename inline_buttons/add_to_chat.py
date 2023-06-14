from telebot import types

markup = types.InlineKeyboardMarkup()
button = types.InlineKeyboardButton(url="t.me/Albi_ChatBot?startgroup=start&admin=change_info+restrict_members+delete_messages+pin_messages+invite_users", text="Добавить✅")
markup.add(button)
