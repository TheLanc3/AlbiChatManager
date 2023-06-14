import telebot
import asyncio
import config
import time
from datetime import datetime as DateTime, timedelta as Delta
from random import randrange

import json_reader
import json_writer
import functions

from telebot import async_telebot

from user_records import UserRecords

from buttons import main

from inline_buttons import add_to_chat

bot = async_telebot.AsyncTeleBot(config.TOKEN)
bot_users = json_reader.load_users()
users_antispam = dict()
BotData = asyncio.run(bot.get_me())

@bot.message_handler(content_types='dice')
async def sticker_handler(msg: telebot.telebot.types.Message):
    if users_antispam.get(msg.from_user.id) is not None:
        if users_antispam[msg.from_user.id] > DateTime.now():
            await bot.send_message(msg.chat.id, f"<b>Не так быстро✋🏻!</b>\nВы сможете снова сыграть в игру через {round((users_antispam[msg.from_user.id] - DateTime.now()).total_seconds())} секунд", parse_mode='html')
            return
    users_antispam[msg.from_user.id] = DateTime.now() + Delta(seconds=8)
    await asyncio.sleep(2.75)
    match msg.dice.emoji:
        case "🏀":
            new_value = 0
            message = ""
            if msg.dice.value < 3:
                message = "<b>Ужасный бросок😒!</b> Очки по баскетболу🏀: "
                new_value = 1
            elif msg.dice.value >= 3 and msg.dice.value < 5:
                message = "<b>👍🏻Неплохая попытка!</b> Очки по баскетболу🏀: "
                new_value = 3
            else:
                message = "<b>Потрясающее попадение🥳!</b> Очки по баскетболу🏀: "
                new_value = 5

            if msg.from_user.id in bot_users:
                bot_users[msg.from_user.id].basketball = bot_users[msg.from_user.id].basketball + new_value
            else:
                bot_users[msg.from_user.id] = UserRecords(new_value, 0, 0, 0, 0)
            await json_writer.update_user(msg.from_user.id, bot_users[msg.from_user.id])
            await bot.send_message(msg.chat.id, message + f"<code>{str(bot_users[msg.from_user.id].basketball)}</code>", reply_to_message_id=msg.message_id, parse_mode='html')
        case "⚽":
            new_value = 0
            message = ""
            if msg.dice.value < 3:
                message = "<b>Ужасный бросок😒!</b> Очки по футболу⚽️: "
                new_value = 1
            elif msg.dice.value >= 3 and msg.dice.value < 5:
                message = "<b>👍🏻Неплохой бросок!</b> Очки по футболу⚽️: "
                new_value = 3
            else:
                message = "<b>Отличный бросок🙂!</b> Очки по футболу⚽️: "
                new_value = 5
            if msg.from_user.id in bot_users:
                bot_users[msg.from_user.id].football = bot_users[msg.from_user.id].football + new_value
            else:
                bot_users[msg.from_user.id] = UserRecords(0, new_value, 0, 0, 0)
            await json_writer.update_user(msg.from_user.id, bot_users[msg.from_user.id])
            await bot.send_message(msg.chat.id, message + f"<code>{str(bot_users[msg.from_user.id].football)}</code>", reply_to_message_id=msg.message_id, parse_mode='html')
        case "🎯":
            new_value = 0
            message = ""
            if msg.dice.value < 3:
                message = "<b>Слишком далеко😒!</b> Очки по дарту🎯: "
                new_value = 1
            elif msg.dice.value >= 3 and msg.dice.value < 6:
                message = "<b>👍🏻Неплохо бросил!</b> Очки по дарту🎯: "
                new_value = 3
            else:
                message = "<b>Точно в цель!</b> Очки по дарту🎯: "
                new_value = 5
            if msg.from_user.id in bot_users:
                bot_users[msg.from_user.id].dart = bot_users[msg.from_user.id].dart + new_value
            else:
                bot_users[msg.from_user.id] = UserRecords(0, 0, new_value, 0, 0)
            await json_writer.update_user(msg.from_user.id, bot_users[msg.from_user.id])
            await bot.send_message(msg.chat.id, message + f"<code>{str(bot_users[msg.from_user.id].dart)}</code>", reply_to_message_id=msg.message_id, parse_mode='html')
        case "🎲":
            new_value = 0
            message = ""
            if msg.dice.value < 3:
                message = "<b>Неудачный бросок😕!</b> Очки по ИК🎲: "
                new_value = 2
            elif msg.dice.value >= 3 and msg.dice.value < 6:
                message = "<b>👍🏻Неплохо бросил!</b> Очки по ИК🎲: "
                new_value = 4
            else:
                message = "<b>Удача на вашей стороне🍀!</b> Очки по ИК🎲: "
                new_value = 6
            if msg.from_user.id in bot_users:
                bot_users[msg.from_user.id].dice = bot_users[msg.from_user.id].dice +new_value
            else:
                bot_users[msg.from_user.id] = UserRecords(0, 0, 0, new_value, 0)
            await json_writer.update_user(msg.from_user.id, bot_users[msg.from_user.id])
            await bot.send_message(msg.chat.id, message + f"<code>{str(bot_users[msg.from_user.id].dice)}</code>", reply_to_message_id=msg.message_id, parse_mode='html')
        case "🎳":
            new_value = 0
            message = ""
            if msg.dice.value < 3:
                message = "<b>Ужасно развалил😑!</b> Очки по боулингу🎳: "
                new_value = 0
            elif msg.dice.value >= 3 and msg.dice.value < 6:
                message = "<b>👍🏻Неплохо бросил!</b> Очки по боулингу🎳: "
                new_value = 2
            else:
                message = "<b>Всех одним ударом✊🏻!</b> Очки по боулингу🎳: "
                new_value = 4
            if msg.from_user.id in bot_users:
                bot_users[msg.from_user.id].balling = bot_users[msg.from_user.id].balling + new_value
            else:
                bot_users[msg.from_user.id] = UserRecords(0, 0, 0, 0, new_value)
            await json_writer.update_user(msg.from_user.id, bot_users[msg.from_user.id])
            await bot.send_message(msg.chat.id, message + f"<code>{str(bot_users[msg.from_user.id].balling)}</code>", reply_to_message_id=msg.message_id, parse_mode='html')

@bot.message_handler(content_types='text')
async def message_handler(msg: telebot.telebot.types.Message):
    #commands
    if msg.text.lower() == "/start" or msg.text.lower() == "/start@albi_chatbot":
        if msg.chat.id == msg.from_user.id:
            await bot.send_message(msg.chat.id, f"<b>👋🏻Привет, <a href=\"tg://user?id={msg.from_user.id}\">{msg.from_user.full_name}</a>!</b>\nЯ базовый чат-менеджер бот с рп-командами, заменяю ботов FBA, которые легли, рп команды:\n\n<code>⚽️</code>\n<code>🏀</code>\n<code>🎲</code>\n<code>🎯</code>\n<code>🎳</code>", reply_markup=main.markup , parse_mode='html')
        else:
            await bot.send_message(msg.chat.id, f"<b>Я никуда не пропала🙃!</b>\nРП команды:\n\n<code>⚽️</code>\n<code>🏀</code>\n<code>🎲</code>\n<code>🎯</code>\n<code>🎳</code>", parse_mode='html')
    if msg.text.lower() == "/top" or msg.text.lower() == "/top@albi_chatbot":
        top_users = dict()
        keys = list(bot_users.keys())
        for i in range(len(keys)):
            if len(top_users) == 15:
                break
            user = bot_users[keys[i]]
            top_users[keys[i]] = user.football + user.basketball + user.balling + user.dart + user.dice
        top_users = dict(sorted(top_users.items(), key=lambda x: x[1], reverse=True))
        keys = list(top_users.keys())
        text = "<b>🍀Топ игроков за всё время:</b>\n"
        for i in range(len(keys)):
            user_name = await bot.get_chat_member(keys[i], keys[i])
            text += f"\n{i+1}. <b>{user_name.user.full_name} - {top_users[keys[i]]}</b>"
        await bot.send_message(msg.chat.id, text, parse_mode='html')
    if msg.text.lower() == "/profile" or msg.text.lower() == "/profile@albi_chatbot":
        if msg.reply_to_message is not None and msg.reply_to_message.from_user.id is not BotData.id:
            if bot_users[msg.reply_to_message.from_user.id] is None:
                json_writer.update_user(msg.reply_to_message.from_user.id, UserRecords(0, 0, 0, 0, 0))
                bot_users[msg.reply_to_message.from_user.id] = UserRecords(0, 0, 0, 0, 0)
            await bot.send_message(msg.chat.id, f"<b>Профиль игрока <a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.full_name}</a>:</b>\n\n⚽️Очки по футболу: {bot_users[msg.reply_to_message.from_user.id].football}\n🏀Очки по баскетболу: {bot_users[msg.reply_to_message.from_user.id].basketball}\n🎯Очки по дарту: {bot_users[msg.reply_to_message.from_user.id].dart}\n🎲Очки по ИК: {bot_users[msg.reply_to_message.from_user.id].dice}\n🎳Очки по боулингу: {bot_users[msg.reply_to_message.from_user.id].balling}", reply_to_message_id=msg.message_id, parse_mode='html')   
        else:
            if bot_users[msg.from_user.id] is None:
                json_writer.update_user(msg.from_user.id, UserRecords(0, 0, 0, 0, 0))
                bot_users[msg.from_user.id] = UserRecords(0, 0, 0, 0, 0)
            await bot.send_message(msg.chat.id, f"<b>Профиль игрока <a href=\"tg://user?id={msg.from_user.id}\">{msg.from_user.full_name}</a>:</b>\n\n⚽️Очки по футболу: {bot_users[msg.from_user.id].football}\n🏀Очки по баскетболу: {bot_users[msg.from_user.id].basketball}\n🎯Очки по дарту: {bot_users[msg.from_user.id].dart}\n🎲Очки по ИК: {bot_users[msg.from_user.id].dice}\n🎳Очки по боулингу: {bot_users[msg.from_user.id].balling}", reply_to_message_id=msg.message_id, parse_mode='html')
    if msg.text.lower() == "/help" or msg.text.lower() == "/help@albi_chatbot":
        await bot.send_message(msg.chat.id, "<b>Мой список команд:</b>\n\n- бан - бан пользователя в чате\n- разбан - разбан пользователя в чате\n- мут - мут пользователя в чате(без указания времени пользователь получит мут 15 минут)\n- размут - размут пользователя в чате\n\n❗️<b>Команды обязательно писать в ответ выбранного пользователя, чтобы бот увидел данного пользователя(кроме /top и рп-команд)</b>", parse_mode='html')
    
    #rp-commands
    if(msg.text.lower().startswith("эль инфа")):
        await bot.send_message(msg.chat.id, f"💫Я думаю, что такое возможно на {randrange(0, 100)}%")
    
    #buttons
    if(msg.text == "Добавить в чат🧿" and msg.from_user.id == msg.chat.id):
        await bot.send_message(msg.chat.id, "Отлично! Вы можете нажать на кнопку ниже, чтобы добавить меня в чат🤗.\n❗️Все необходимые права уже приписаны в кнопке", reply_markup=add_to_chat.markup)
    if(msg.text == "О ботеℹ️" and msg.from_user.id == msg.chat.id):
        await bot.send_message(msg.chat.id, "<b>🧿Мой создатель: Lance - владелец FBA Team</b>\n<i>Я была создана, чтобы помогать админам управлять чатом, замещать своих ботов-друзей в работе, если они вдруг \"заснули\"</i>\n\nМои друзья:\n- <a href=\"t.me/Laura_cm_bot\">Лаура</a>(удалена со стороны телеграма)", parse_mode='html')
    #admins commands
    if(msg.text.lower() == "бан"):
        if(msg.chat.id != msg.from_user.id):
            user = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
            if(msg.reply_to_message == None):
                await bot.send_message(msg.chat.id, "❗️Вы не указали участника, которого вы хотели забанить")
            elif(msg.reply_to_message.from_user.id == BotData.id):
                await bot.send_message(msg.chat.id, "Размечтался меня забанить🥱")
            elif(msg.reply_to_message.from_user.id == msg.from_user.id):
                await bot.send_message(msg.chat.id, "Если тебе не удобно быть в этом чате, то ты можешь просто взять и ливнуть🙄")
            else:
                user_reply = await bot.get_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
                Bot = await bot.get_chat_member(msg.chat.id, BotData.id)
                userStatus = functions.Func.GetAdmin(user.status)
                userReplyStatus = functions.Func.GetAdmin(user_reply.status)
                if(Bot.status != 'administrator'):
                    await bot.send_message(msg.chat.id, "Я не имею админки😕")
                elif(userStatus != "administrator"):
                    await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.from_user.id}\">{msg.from_user.first_name}</a>, вам не положено такое право😏", parse_mode='html', disable_web_page_preview=True)
                elif(userReplyStatus == "administrator"):
                    await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> не может быть забанен(а), пока он(а) админ чата✋🏻", parse_mode='html', disable_web_page_preview=True)
                else:
                    await bot.kick_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
                    await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> выгнан из чата!", parse_mode='html', disable_web_page_preview=True)
    if(msg.text.lower() == "мут"):
        if(msg.chat.id != msg.from_user.id):
            user = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
            if(msg.reply_to_message == None):
                await bot.send_message(msg.chat.id, "❗️Вы не указали участника, которого вы хотели забанить")
            elif(msg.reply_to_message.from_user.id == BotData.id):
                await bot.send_message(msg.chat.id, "Размечтался меня забанить🥱")
            elif(msg.reply_to_message.from_user.id == msg.from_user.id):
                await bot.send_message(msg.chat.id, "Если тебе не удобно быть в этом чате, то ты можешь просто взять и ливнуть🙄")
            else:
                user_reply = await bot.get_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
                Bot = await bot.get_chat_member(msg.chat.id, BotData.id)
                userStatus = functions.Func.GetAdmin(user.status)
                userReplyStatus = functions.Func.GetAdmin(user_reply.status)
                if(Bot.status != 'administrator'):
                    await bot.send_message(msg.chat.id, "Я не имею админки😕")
                elif(userStatus != "administrator"):
                    await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.from_user.id}\">{msg.from_user.first_name}</a>, вам не положено такое право😏", parse_mode='html', disable_web_page_preview=True)
                elif(userReplyStatus == "administrator"):
                    await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> не может быть отправлен(а) в мут, пока он(а) админ чата✋🏻", parse_mode='html', disable_web_page_preview=True)
                else:
                    await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False, until_date=DateTime.utcnow() + config.MSK + Delta(minutes=15))
                    await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на 15 минут🤐", parse_mode='html', disable_web_page_preview=True)
    if(msg.text.lower().startswith("мут ")):
        if(msg.chat.id != msg.from_user.id):
            user = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
            if(msg.reply_to_message == None):
                await bot.send_message(msg.chat.id, "❗️Вы не указали участника, которого вы хотели забанить")
            elif(msg.reply_to_message.from_user.id == BotData.id):
                await bot.send_message(msg.chat.id, "Размечтался меня забанить🥱")
            elif(msg.reply_to_message.from_user.id == msg.from_user.id):
                await bot.send_message(msg.chat.id, "Если тебе не удобно быть в этом чате, то ты можешь просто взять и ливнуть🙄")
            else:
                user_reply = await bot.get_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
                Bot = await bot.get_chat_member(msg.chat.id, BotData.id)
                userStatus = functions.Func.GetAdmin(user.status)
                userReplyStatus = functions.Func.GetAdmin(user_reply.status)
                if(Bot.status != 'administrator'):
                    await bot.send_message(msg.chat.id, "Я не имею админки😕")
                elif(userStatus != "administrator"):
                    await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.from_user.id}\">{msg.from_user.first_name}</a>, вам не положено такое право😏", parse_mode='html', disable_web_page_preview=True)
                elif(userReplyStatus == "administrator"):
                    await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> не может быть отправлен(а) в мут, пока он(а) админ чата✋🏻", parse_mode='html', disable_web_page_preview=True)
                else:
                    try:
                        time = int(msg.text.split(' ')[1])
                        format_time = msg.text.split(' ')[2].lower()
                        match format_time:
                            #minutes region
                            case "минут":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(minutes=time))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} минут🤐", parse_mode='html', disable_web_page_preview=True)
                            case "минуты":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(minutes=time))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} минут🤐", parse_mode='html', disable_web_page_preview=True)
                            case "минута":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(minutes=time))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} минута🤐", parse_mode='html', disable_web_page_preview=True)
                            case "минуту":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(minutes=time))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} минуту🤐", parse_mode='html', disable_web_page_preview=True)


                            #hours region
                            case "час":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(hours=time))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} час🤐", parse_mode='html', disable_web_page_preview=True)
                            case "часа":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(hours=time))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} часов🤐", parse_mode='html', disable_web_page_preview=True)
                            case "часов":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(hours=time))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} часов🤐", parse_mode='html', disable_web_page_preview=True)


                            #days region
                            case "день":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(days=time))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} день🤐", parse_mode='html', disable_web_page_preview=True)
                            case "дня":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(days=time))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} дня🤐", parse_mode='html', disable_web_page_preview=True)
                            case "дней":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(days=time))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} дней🤐", parse_mode='html', disable_web_page_preview=True)


                            #weeks region
                            case "неделю":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(weeks=time))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} неделю🤐", parse_mode='html', disable_web_page_preview=True)
                            case "недель":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(weeks=time))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} недель🤐", parse_mode='html', disable_web_page_preview=True)


                            #mounths region
                            case "месяц":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(days=(30 * time)))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} месяц🤐", parse_mode='html', disable_web_page_preview=True)
                            case "месяца":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(days=(30 * time)))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} месяца🤐", parse_mode='html', disable_web_page_preview=True)
                            case "месяцев":
                                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, DateTime.utcnow() + config.MSK + Delta(days=(30 * time)))
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} месяцев🤐", parse_mode='html', disable_web_page_preview=True)


                            #else region
                            case _:
                                await bot.send_message(msg.chat.id, f"👺Формат времени \"{format_time}\" не существует!")
                    except ValueError:
                        await bot.send_message(msg.chat.id, "📛Вы не указали время")
            if(msg.text.lower() == "разбан"):
                if(msg.chat.id != msg.from_user.id):
                    user = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
                    if(msg.reply_to_message == None):
                        await bot.send_message(msg.chat.id, "❗️Вы не указали участника, которого вы хотели забанить")
                    elif(msg.reply_to_message.from_user.id == BotData.id):
                        await bot.send_message(msg.chat.id, "Размечтался меня забанить🥱")
                    elif(msg.reply_to_message.from_user.id == msg.from_user.id):
                        await bot.send_message(msg.chat.id, "Если тебе не удобно быть в этом чате, то ты можешь просто взять и ливнуть🙄")
                    else:
                        user_reply = await bot.get_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
                        Bot = await bot.get_chat_member(msg.chat.id, BotData)
                        userStatus = functions.Func.GetAdmin(user.status)
                        userReplyStatus = functions.Func.GetAdmin(user_reply.status)
                        if(Bot.status != 'administrator'):
                            await bot.send_message(msg.chat.id, "Я не имею админки😕")
                        elif(userStatus != "administrator"):
                            await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.from_user.id}\">{msg.from_user.first_name}</a>, вам не положено такое право😏", parse_mode='html', disable_web_page_preview=True)
                        elif(userReplyStatus == "administrator"):
                            await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> не может быть забанен(а), пока он(а) админ чата✋🏻", parse_mode='html', disable_web_page_preview=True)
                        else:
                            await bot.unban_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
                            await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> теперь может вернуться обратно🤗", parse_mode='html', disable_web_page_preview=True)
                            try:
                                chat = await bot.get_chat(msg.chat.id)
                                link = chat.invite_link
                                await bot.send_message(msg.reply_to_message.from_user.id, f"<a href=\"tg://user?id={msg.from_user.id}\">{msg.from_user.first_name}</a> разбанил Вас в чате, ссылка на беседу:\n{link}", parse_mode='html', disable_web_page_preview=True)
                            except telebot.apihelper.ApiTelegramException:
                                return
            if(msg.text.lower() == "размут"):
                    if(msg.chat.id != msg.from_user.id):
                        user = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
                        if(msg.reply_to_message == None):
                            await bot.send_message(msg.chat.id, "❗️Вы не указали участника, которого вы хотели забанить")
                        elif(msg.reply_to_message.from_user.id == BotData.id):
                            await bot.send_message(msg.chat.id, "Размечтался меня забанить🥱")
                        elif(msg.reply_to_message.from_user.id == msg.from_user.id):
                            await bot.send_message(msg.chat.id, "Если тебе не удобно быть в этом чате, то ты можешь просто взять и ливнуть🙄")
                        else:
                            user_reply = await bot.get_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
                            Bot = await bot.get_chat_member(msg.chat.id, BotData.id)
                            userStatus = functions.Func.GetAdmin(user.status)
                            userReplyStatus = functions.Func.GetAdmin(user_reply.status)
                            if(Bot.status != 'administrator'):
                                await bot.send_message(msg.chat.id, "Я не имею админки😕")
                            elif(userStatus != "administrator"):
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.from_user.id}\">{msg.from_user.first_name}</a>, вам не положено такое право😏", parse_mode='html', disable_web_page_preview=True)
                            elif(userReplyStatus == "administrator"):
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> не может быть забанен(а), пока он(а) админ чата✋🏻", parse_mode='html', disable_web_page_preview=True)
                            else:
                                await bot.promote_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
                                await bot.send_message(msg.chat.id, f"<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">{msg.reply_to_message.from_user.first_name}</a> теперь может говорить🗣️", parse_mode='html', disable_web_page_preview=True)

@bot.message_handler(content_types=['new_chat_members'])
async def handler_new_member(message):
    if message.new_chat_members[0].id == BotData.id:
        await bot.send_message(message.chat.id, "Ухх, спасибо, что я теперь вам нужна😊!")
    else:
        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.new_chat_members[0].id}\">{message.new_chat_members[0].first_name}</a>, добро пожаловать к нам в хату <b>\"{message.chat.title}\"</b>!", parse_mode='html', disable_web_page_preview=True)


@bot.message_handler(content_types=['left_chat_member'])
async def handler_left_member(message):
    if message.left_chat_member.id == BotData.id :
        return
    elif message.from_user.id != message.left_chat_member.id:
        return
    else:
        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.left_chat_member.id}\">{message.left_chat_member.first_name}</a> ливнул с чата☹️", parse_mode='html', disable_web_page_preview=True)

asyncio.run(bot.infinity_polling(skip_pending=True))
