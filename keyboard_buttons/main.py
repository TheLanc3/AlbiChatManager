from telebot import types

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
help = types.KeyboardButton("Как использовать❔")
info = types.KeyboardButton("О ботеℹ️")
add_to_chat = types.KeyboardButton("Добавить в чат🧿")
markup.add(help, info)
markup.add(add_to_chat)