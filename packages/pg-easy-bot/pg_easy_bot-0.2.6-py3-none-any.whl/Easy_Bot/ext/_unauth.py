from pyrogram import Client
from pyrogram.types import Message 
from pyrogram.enums import ParseMode
from Easy_Bot.error import UnauthorizedCommandError


async def unauthorized(client:Client, message:Message):
    text =  "<b>Unauthorized command detected! </b>\n\nYou do not have permission to use this command."
    await message.reply_text(text=text,parse_mode=ParseMode.HTML)
    raise UnauthorizedCommandError