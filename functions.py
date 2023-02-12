import config
import asyncio
from pyrogram import Client
from pyrogram.raw.functions.contacts import ResolveUsername
from config import token

class Func:
    def GetAdmin(member_status: str):
        if(member_status == "creator"):
            member_status = "administrator"
            return member_status
        elif(member_status == "administrator"):
            member_status = "administrator"
            return member_status
        else:
            return member_status
