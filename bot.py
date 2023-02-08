import config
import telebot
from telebot import async_telebot
import time
from datetime import datetime, timedelta
from random import randrange

from functions import *

from keyboard_buttons import main

from inline_buttons import add_to_chat
MSK = config.MSK
token = config.token
botId = config.botId

bot = async_telebot.AsyncTeleBot(token)
bot_func = Client('bot_func', config.api_id, config.api_hash, bot_token=config.token)



@bot.message_handler(content_types=['text'])
async def messages(message: telebot.types.Message):
    if(message != None):
        if(message.text != None):

            #start command
            if message.text.lower() == "/start" or message.text.lower() == "/start@albi_cm_bot":
                if(message.from_user.id == message.chat.id):
                    await bot.send_message(message.chat.id, f"<b>Привет, <a href=\"tg://user?id={message.from_user.id}\">{message.from_user.first_name}</a>!</b>\nМеня звать Эльби, я чат-менеджер бот, который будет следить за порядком и помогать админам чата😊", reply_markup=main.markup, parse_mode='html')
                elif(message.chat.id != message.from_user.id):
                    await bot.send_message(message.chat.id, "Здрасьте, нужна помощь?\nПиши /help")
            if (message.text.lower() == "/start@albi_cm_bot start"):
                await bot.send_message(message.chat.id, "Ухх, спасибо, что я теперь вам нужна😊!")
            
            #admins commands
            if(message.text.lower() == "бан"):
                if(message.chat.id != message.from_user.id):
                    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
                    if(message.reply_to_message == None):
                        await bot.send_message(message.chat.id, "❗️Вы не указали участника, которого вы хотели забанить")
                    elif(message.reply_to_message.from_user.id == botId):
                        await bot.send_message(message.chat.id, "Размечтался меня забанить🥱")
                    elif(message.reply_to_message.from_user.id == message.from_user.id):
                        await bot.send_message(message.chat.id, "Если тебе не удобно быть в этом чате, то ты можешь просто взять и ливнуть🙄")
                    else:
                        user_reply = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                        Bot = await bot.get_chat_member(message.chat.id, botId)
                        userStatus = Func.GetAdmin(user.status)
                        userReplyStatus = Func.GetAdmin(user_reply.status)
                        if(Bot.status != 'administrator'):
                            await bot.send_message(message.chat.id, "Я не имею админки😕")
                        elif(userStatus != "administrator"):
                            await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.first_name}</a>, вам не положено такое право😏", parse_mode='html', disable_web_page_preview=True)
                        elif(userReplyStatus == "administrator"):
                            await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> не может быть забанен(а), пока он(а) админ чата✋🏻", parse_mode='html', disable_web_page_preview=True)
                        else:
                            await bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                            await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> выгнан из чата!", parse_mode='html', disable_web_page_preview=True)
            if(message.text.lower() == "мут"):
                if(message.chat.id != message.from_user.id):
                    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
                    if(message.reply_to_message == None):
                        await bot.send_message(message.chat.id, "❗️Вы не указали участника, которого вы хотели забанить")
                    elif(message.reply_to_message.from_user.id == botId):
                        await bot.send_message(message.chat.id, "Размечтался меня забанить🥱")
                    elif(message.reply_to_message.from_user.id == message.from_user.id):
                        await bot.send_message(message.chat.id, "Если тебе не удобно быть в этом чате, то ты можешь просто взять и ливнуть🙄")
                    else:
                        user_reply = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                        Bot = await bot.get_chat_member(message.chat.id, botId)
                        userStatus = Func.GetAdmin(user.status)
                        userReplyStatus = Func.GetAdmin(user_reply.status)
                        if(Bot.status != 'administrator'):
                            await bot.send_message(message.chat.id, "Я не имею админки😕")
                        elif(userStatus != "administrator"):
                            await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.first_name}</a>, вам не положено такое право😏", parse_mode='html', disable_web_page_preview=True)
                        elif(userReplyStatus == "administrator"):
                            await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> не может быть отправлен(а) в мут, пока он(а) админ чата✋🏻", parse_mode='html', disable_web_page_preview=True)
                        else:
                            await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False, until_date=datetime.datetime.utcnow() + MSK + datetime.timedelta(minutes=15))
                            await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на 15 минут🤐", parse_mode='html', disable_web_page_preview=True)
            if(message.text.lower().startswith("мут ")):
                if(message.chat.id != message.from_user.id):
                    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
                    if(message.reply_to_message == None):
                        await bot.send_message(message.chat.id, "❗️Вы не указали участника, которого вы хотели забанить")
                    elif(message.reply_to_message.from_user.id == botId):
                        await bot.send_message(message.chat.id, "Размечтался меня забанить🥱")
                    elif(message.reply_to_message.from_user.id == message.from_user.id):
                        await bot.send_message(message.chat.id, "Если тебе не удобно быть в этом чате, то ты можешь просто взять и ливнуть🙄")
                    else:
                        user_reply = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                        Bot = await bot.get_chat_member(message.chat.id, botId)
                        userStatus = Func.GetAdmin(user.status)
                        userReplyStatus = Func.GetAdmin(user_reply.status)
                        if(Bot.status != 'administrator'):
                            await bot.send_message(message.chat.id, "Я не имею админки😕")
                        elif(userStatus != "administrator"):
                            await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.first_name}</a>, вам не положено такое право😏", parse_mode='html', disable_web_page_preview=True)
                        elif(userReplyStatus == "administrator"):
                            await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> не может быть отправлен(а) в мут, пока он(а) админ чата✋🏻", parse_mode='html', disable_web_page_preview=True)
                        else:
                            try:
                                time = int(message.text.split(' ')[1])
                                format_time = message.text.split(' ')[2].lower()
                                match format_time:
                                    #minutes region
                                    case "минут":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(minutes=time))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} минут🤐", parse_mode='html', disable_web_page_preview=True)
                                    case "минуты":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(minutes=time))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} минут🤐", parse_mode='html', disable_web_page_preview=True)
                                    case "минута":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(minutes=time))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} минута🤐", parse_mode='html', disable_web_page_preview=True)
                                    case "минуту":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(minutes=time))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} минуту🤐", parse_mode='html', disable_web_page_preview=True)

                                    #hours region
                                    case "час":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(hours=time))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} час🤐", parse_mode='html', disable_web_page_preview=True)
                                    case "часа":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(hours=time))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} часов🤐", parse_mode='html', disable_web_page_preview=True)
                                    case "часов":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(hours=time))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} часов🤐", parse_mode='html', disable_web_page_preview=True)

                                    #days region
                                    case "день":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(days=time))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} день🤐", parse_mode='html', disable_web_page_preview=True)
                                    case "дня":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(days=time))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} дня🤐", parse_mode='html', disable_web_page_preview=True)
                                    case "дней":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(days=time))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} дней🤐", parse_mode='html', disable_web_page_preview=True)

                                    #weeks region
                                    case "неделю":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(weeks=time))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} неделю🤐", parse_mode='html', disable_web_page_preview=True)
                                    case "недель":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(weeks=time))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} недель🤐", parse_mode='html', disable_web_page_preview=True)

                                    #mounths region
                                    case "месяц":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(days=(30 * time)))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} месяц🤐", parse_mode='html', disable_web_page_preview=True)
                                    case "месяца":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(days=(30 * time)))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} месяца🤐", parse_mode='html', disable_web_page_preview=True)
                                    case "месяцев":
                                        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, datetime.utcnow() + MSK + timedelta(days=(30 * time)))
                                        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> получил(а) мут на {str(time)} месяцев🤐", parse_mode='html', disable_web_page_preview=True)

                                    #else region
                                    case _:
                                        await bot.send_message(message.chat.id, f"👺Формат времени \"{format_time}\" не существует!")
                            except ValueError:
                                await bot.send_message(message.chat.id, "📛Вы не указали время")
            if(message.text.lower() == "разбан"):
                if(message.chat.id != message.from_user.id):
                    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
                    if(message.reply_to_message == None):
                        await bot.send_message(message.chat.id, "❗️Вы не указали участника, которого вы хотели забанить")
                    elif(message.reply_to_message.from_user.id == botId):
                        await bot.send_message(message.chat.id, "Размечтался меня забанить🥱")
                    elif(message.reply_to_message.from_user.id == message.from_user.id):
                        await bot.send_message(message.chat.id, "Если тебе не удобно быть в этом чате, то ты можешь просто взять и ливнуть🙄")
                    else:
                        user_reply = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                        Bot = await bot.get_chat_member(message.chat.id, botId)
                        userStatus = Func.GetAdmin(user.status)
                        userReplyStatus = Func.GetAdmin(user_reply.status)
                        if(Bot.status != 'administrator'):
                            await bot.send_message(message.chat.id, "Я не имею админки😕")
                        elif(userStatus != "administrator"):
                            await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.first_name}</a>, вам не положено такое право😏", parse_mode='html', disable_web_page_preview=True)
                        elif(userReplyStatus == "administrator"):
                            await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> не может быть забанен(а), пока он(а) админ чата✋🏻", parse_mode='html', disable_web_page_preview=True)
                        else:
                            await bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                            await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> теперь может вернуться обратно🤗", parse_mode='html', disable_web_page_preview=True)
                            try:
                                chat = await bot.get_chat(message.chat.id)
                                link = chat.invite_link
                                await bot.send_message(message.reply_to_message.from_user.id, f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.first_name}</a> разбанил Вас в чате, ссылка на беседу:\n{link}", parse_mode='html', disable_web_page_preview=True)
                            except telebot.apihelper.ApiTelegramException:
                                return
            if(message.text.lower() == "размут"):
                    if(message.chat.id != message.from_user.id):
                        user = await bot.get_chat_member(message.chat.id, message.from_user.id)
                        if(message.reply_to_message == None):
                            await bot.send_message(message.chat.id, "❗️Вы не указали участника, которого вы хотели забанить")
                        elif(message.reply_to_message.from_user.id == botId):
                            await bot.send_message(message.chat.id, "Размечтался меня забанить🥱")
                        elif(message.reply_to_message.from_user.id == message.from_user.id):
                            await bot.send_message(message.chat.id, "Если тебе не удобно быть в этом чате, то ты можешь просто взять и ливнуть🙄")
                        else:
                            user_reply = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                            Bot = await bot.get_chat_member(message.chat.id, botId)
                            userStatus = Func.GetAdmin(user.status)
                            userReplyStatus = Func.GetAdmin(user_reply.status)
                            if(Bot.status != 'administrator'):
                                await bot.send_message(message.chat.id, "Я не имею админки😕")
                            elif(userStatus != "administrator"):
                                await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.first_name}</a>, вам не положено такое право😏", parse_mode='html', disable_web_page_preview=True)
                            elif(userReplyStatus == "administrator"):
                                await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> не может быть забанен(а), пока он(а) админ чата✋🏻", parse_mode='html', disable_web_page_preview=True)
                            else:
                                await bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                                await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.reply_to_message.from_user.id}\">{message.reply_to_message.from_user.first_name}</a> теперь может говорить🗣️", parse_mode='html', disable_web_page_preview=True)
            if(message.text.lower().startswith("эль инфа")):
                await bot.send_message(message.chat.id, f"💫Я думаю, что такое возможно на {randrange(0, 100)}%")
            if message.text.startswith("@"):
                user = await Func.GetUserByUsername("LanceMinecraft", bot_func)
                print(user.id)
                print(user.first_name)
            #buttons
            if(message.text == "О ботеℹ️" and message.from_user.id == message.chat.id):
                await bot.send_message(message.chat.id, "<b>🧿Мой создатель: Lance - владелец FBA Team</b>\n<i>Я была создана, чтобы помогать админам управлять чатом, замещать своих подруг в работе, если они вдруг \"заснули\"</i>\n\nМои подруги:\n- <a href=\"t.me/Laura_cm_bot\">Лаура</a>", parse_mode='html')
                #await bot.send_message(message.chat.id, "<b>🧿Мой создатель: Lance - владелец FBA Team</b>\n<i>Я была создана, чтобы помогать админам управлять чатом, замещать своих подруг в работе, если они вдруг \"заснули\"</i>\n\nМои подруги:\n- <a href=\"t.me/Laura_cm_bot\">Лаура</a>\n- <a href=\"https://t.me/QuentyCMBot\">Квенти/Quenty</a>", parse_mode='html')
            if(message.text == "Как использовать❔" and message.from_user.id == message.chat.id):
                await bot.send_message(message.chat.id, "Бот пока что в разработкке❌\nСейчас бот на стадии EA(Early Access)")
            if(message.text == "Добавить в чат🧿" and message.from_user.id == message.chat.id):
                await bot.send_message(message.chat.id, "Отлично! Вы можете нажать на кнопку ниже, чтобы добавить меня в чат🤗.\n❗️Все необходимые права уже приписаны в кнопке", reply_markup=add_to_chat.markup)
            print(str(datetime.utcnow() + MSK) + " " + message.text)

@bot.message_handler(content_types=['new_chat_members'])
async def handler_new_member(message):
    if(message.new_chat_members[0].id == botId):
        await bot.send_message(message.chat.id, "Ухх, спасибо, что я теперь вам нужна😊!")
    else:
        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.new_chat_members[0].id}\">{message.new_chat_members[0].first_name}</a>, добро пожаловать к нам в хату <b>\"{message.chat.title}\"</b>!", parse_mode='html', disable_web_page_preview=True)

@bot.message_handler(content_types=['left_chat_member'])
async def handler_left_member(message):
    if(message.left_chat_member.id == botId):
        return
    elif(message.from_user.id != message.left_chat_member.id):
        return
    else:
        await bot.send_message(message.chat.id, f"<a href=\"tg://user?id={message.left_chat_member.id}\">{message.left_chat_member.first_name}</a> ливнул с чата☹️", parse_mode='html', disable_web_page_preview=True)

asyncio.run(bot.infinity_polling(skip_pending=True))