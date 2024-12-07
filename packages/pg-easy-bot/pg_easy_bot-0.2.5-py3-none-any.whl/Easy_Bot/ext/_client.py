from pyrogram import Client as Application
from pyrogram import filters
from pyrogram.handlers import MessageHandler , CallbackQueryHandler , InlineQueryHandler , ChatJoinRequestHandler , ChatMemberUpdatedHandler, chat_join_request_handler , chat_member_updated_handler , user_status_handler,raw_update_handler,chosen_inline_result_handler,deleted_messages_handler,disconnect_handler,edited_message_handler,handler,inline_query_handler,poll_handler
from ._data_classess import Bot , User , Handlers , MessagesHandlers
from Easy_Bot.error import NoHandler
from pyrogram.errors import FloodWait
from ._commands import get_commands_data
from typing import Optional
from aiohttp import web
from ._web import web_server 
import asyncio
import os
import sys
from ._publicIp import get_public_ip , check_public_ip_reachable

LOGO = """
........................................
.#####...####...##...##...####...#####..
.##..##.##..##..###.###..##..##..##..##.
.#####..######..##.#.##..##..##..##..##.
.##.....##..##..##...##..##..##..##..##.
.##.....##..##..##...##...####...#####..
........................................    
   ├ ᴄᴏᴘʏʀɪɢʜᴛ © 𝟸𝟶𝟸𝟹-𝟸𝟶𝟸𝟺 ᴘᴀᴍᴏᴅ ᴍᴀᴅᴜʙᴀsʜᴀɴᴀ. ᴀʟʟ ʀɪɢʜᴛs ʀᴇsᴇʀᴠᴇᴅ.
   ├ ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ  ɢᴘʟ-𝟹.𝟶 ʟɪᴄᴇɴsᴇ.
   └ ʏᴏᴜ ᴍᴀʏ ɴᴏᴛ ᴜsᴇ ᴛʜɪs ғɪʟᴇ ᴇxᴄᴇᴘᴛ ɪɴ ᴄᴏᴍᴘʟɪᴀɴᴄᴇ ᴡɪᴛʜ ᴛʜᴇ ʟɪᴄᴇɴsᴇ.
"""

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else: 
        os.system('clear')

class client(Application):
    def __init__(
            self,
            bot: Bot = None,
            user: User = None,
            start_function: callable = None,
    ):
        """
        Initialize a client instance.

        Args:
            bot (Bot): The bot class.
        """
        self._bot = None
        self._user = None
        self.web = bot.web if bot else user.web if user else True
        self.start_function = start_function
        if bot:
            self.token = bot.token
            self._bot= Application(
                name = bot.name,
                api_id = bot.api_id,
                api_hash = bot.api_hash,
                bot_token = bot.token,
                workers = bot.workers,
                in_memory = bot.in_memory
            )
        if user:
            self.session = user.sesstion
            self._user = Application(
                name = user.name,
                api_id = user.api_id,
                api_hash = user.api_hash,
                session_string=user.sesstion,
                workers = user.workers,
                in_memory = user.in_memory
            )

    async def trigger_callback(self):
        await self.start_function()
    async def restart(time:int = 0):
        await asyncio.sleep(time)
        os.execl(sys.executable, sys.executable, *sys.argv)
    async def start(self):
        clear_terminal()
        print(LOGO + "\n\n" )
        self._bot_info = None
        self._user_info = None
        if self._bot:
            try:
                await self._bot.start()
                self._bot_info = await self._bot.get_me()
                print(f"Bot Client > {self._bot_info.first_name} - @{self._bot_info.username} Started")
            except FloodWait as e:
                print(f"Bot Client > Flood Wait: {e.value} seconds")
        if self._user:
            try:
                await self._user.start()
                self._user_info = await self._user.get_me()
                print(f"User Client > {self._user_info.first_name} - @{self._user_info.username} Started")
            except FloodWait as e:
                print(f"User Client > Flood Wait: {e.value} seconds")
            
        if self.web:
            try:
                webapp = web.AppRunner(await web_server(self._bot_info or self._user_info or None))
                await webapp.setup()
                await web.TCPSite(webapp, "0.0.0.0", 8080).start()
                my_ip = get_public_ip()
                if str(self.web).startswith('http'):
                    link = self.web
                elif await check_public_ip_reachable(my_ip):
                    link = f"http://{my_ip}:8080"
                else:
                    link = "locally http://0.0.0.0:8080"
                print(f"Webapp running on {link}")
            except Exception as e:print(e)

        if self.start_function:
            await self.trigger_callback()

    async def stop(self, *args):
        clear_terminal()
        if self._bot and self._bot.is_connected:
            print(f"{self._bot_info.first_name} - @{self._bot_info.username} Stoped")
            await self._bot.stop()
        
        if self._user and self._user.is_connected:
            print(f"{self._user_info.first_name} - @{self._user_info.username} Stoped")
            await self._user.stop()

class pyroClient:
    def __init__(
            self,
            bot: Bot = None,
            user: User = None,
            start_function: callable = None
    ):
        """
        Initialize a pyroClient instance.

        Args:
            bot (Bot): The bot class.
            handlers (HANDLERS, optional): Handlers for the bot. Defaults to {}.
        """
        self.app = client(bot ,user,start_function)
        self.bot = self.app._bot
        self.user = self.app._user
        print('Starting...')
        clients:list[dict] = []
        if bot:clients.append({self.bot : bot.handler})
        if user:clients.append({self.user : user.handler})
        for item in clients:
            for cl, handlers in item.items():
                cl: client = cl
                if handlers == {} or handlers ==  None:
                    raise NoHandler
                handlers: Handlers= handlers
                messages:MessagesHandlers = handlers.messages
                commands = handlers.commands
                callback = handlers.callback
                inline = handlers.inline
                join_request = handlers.join_request
                greeting = handlers.greeting
                self.command_list = []

                if commands:
                    commands_dir = commands
                    commands = get_commands_data(commands_dir)
                    
                    for command , cmd_func in commands:
                        cl.add_handler(MessageHandler(cmd_func ,filters.command(command)))
                        self.command_list.append(command)
                        
                if messages:
                    if messages.text:cl.add_handler(MessageHandler(filters.text & ~filters.command(self.command_list),messages.text))
                    if messages.callbacks:cl.add_handler(CallbackQueryHandler(messages.callbacks))
                    if messages.poll:cl.add_handler(MessageHandler(filters.poll,messages.poll))
                    if messages.reply:cl.add_handler(MessageHandler(filters.reply,messages.reply))
                    if messages.audio:cl.add_handler(MessageHandler(filters.audio,messages.audio))
                    if messages.video:cl.add_handler(MessageHandler(filters.video,messages.video))
                    if messages.voice:cl.add_handler(MessageHandler(filters.voice,messages.voice ))
                    if messages.caption:cl.add_handler(MessageHandler(filters.caption,messages.caption))
                    if messages.contact:cl.add_handler(MessageHandler(filters.contact,messages.contact))
                    if messages.location:cl.add_handler(MessageHandler(filters.location,messages.location))
                    if messages.sticker:cl.add_handler(MessageHandler(filters.sticker,messages.sticker))
                    if messages.document:cl.add_handler(MessageHandler(filters.document,messages.document))
                    if messages.new_chat_photo:cl.add_handler(MessageHandler(filters.new_chat_photo,messages.new_chat_photo))
                    if messages.new_chat_title:cl.add_handler(MessageHandler(filters.new_chat_title,messages.new_chat_title))
                    if messages.new_chat_member:cl.add_handler(MessageHandler(filters.new_chat_members,messages.new_chat_member))
                    if messages.left_chat_memeber:cl.add_handler(MessageHandler(filters.left_chat_member,messages.left_chat_memeber))
                    if messages.pinned_message:cl.add_handler(MessageHandler(filters.pinned_message,messages.pinned_message))
                    if messages.all_status:cl.add_handler(MessageHandler(filters.all,messages.all_status))

                if callback:
                    cl.add_handler(CallbackQueryHandler(callback))

                if inline:
                    cl.add_handler(InlineQueryHandler(inline))

                if join_request:
                    cl.add_handler(ChatJoinRequestHandler(join_request))

                if greeting:
                    cl.add_handler(ChatMemberUpdatedHandler(greeting))
        

    def stop(self):
        """
        Stop the bot. This method will stop the bot.
        """
        self.app.stop()



    def start(self):
        """
        Start the bot. This method will start the bot in either webhook or polling mode,
        depending on whether a webhook_url is provided.

        Args:
            drop_pending_updates (bool, optional): Whether to drop pending updates. Defaults to None.

        """
        try:
            self.app.run()
        except Exception as e:
            print(e)
            raise


