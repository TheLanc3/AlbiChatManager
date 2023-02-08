import config
import asyncio
from pyrogram import Client
from pyrogram.raw.functions.contacts import ResolveUsername
from config import token

class Func:
    async def GetUserByUsername(username: str, bot_func: Client):
        if bot_func.is_connected == True:
            await bot_func.stop()
        await bot_func.start()
        user = await bot_func.invoke(ResolveUsername(username=username))
        await bot_func.stop()
        return user.users[0]
        
    def GetAdmin(member_status: str):
        if(member_status == "creator"):
            member_status = "administrator"
            return member_status
        elif(member_status == "administrator"):
            member_status = "administrator"
            return member_status
        else:
            return member_status