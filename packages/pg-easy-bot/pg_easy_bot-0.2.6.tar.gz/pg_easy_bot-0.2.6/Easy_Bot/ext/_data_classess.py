
class MessagesHandlers:
    def __init__(self,
        all : callable = None,
        bot_filter: callable = None,
        callbacks: callable = None,
        channel_chat_created: callable = None,
        text: callable = None,
        caption: callable = None,
        document: callable = None,
        audio: callable = None,
        video: callable = None,
        voice: callable = None,
        sticker: callable = None,
        contact: callable = None,
        location: callable = None,
        reply: callable = None,
        poll: callable = None,
        new_chat_member: callable = None,
        left_chat_memeber: callable = None,
        new_chat_title: callable = None,
        new_chat_photo: callable = None,
        pinned_message : callable = None,
        all_status : callable = None,
    ):
        """
        Initialize a MessagesHandlers instance.

        This class is used to store callback functions for the MessageHandler.

        Args:
            text: A callable that will be called when a text message is received.
            caption: A callable that will be called when a message with a caption is received.
            document: A callable that will be called when a document is received.
            audio: A callable that will be called when an audio is received.
            video: A callable that will be called when a video is received.
            voice: A callable that will be called when a voice message is received.
            sticker: A callable that will be called when a sticker is received.
            contact: A callable that will be called when a contact is received.
            location: A callable that will be called when a location is received.
            reply: A callable that will be called when a reply is received.
            poll: A callable that will be called when a poll is received.
            new_chat_member: A callable that will be called when a new chat member is received.
            left_chat_memeber: A callable that will be called when a chat member leaves the chat.
            new_chat_title: A callable that will be called when a chat title is changed.
            new_chat_photo: A callable that will be called when a chat photo is changed.
            message_auto_delete_timer_changed: A callable that will be called when the auto delete timer for a message is changed.
            pinned_message: A callable that will be called when a message is pinned.
            all_status: A callable that will be called when any of the above events are triggered.
        """
        self.all = all
        self.callbacks = callbacks
        self.bot_filter = bot_filter
        self.channel_chat_created = channel_chat_created
        self.text = text
        self.caption = caption
        self.document = document
        self.audio = audio
        self.video = video
        self.voice = voice
        self.sticker = sticker
        self.contact = contact
        self.location = location
        self.reply = reply
        self.poll = poll
        self.new_chat_member = new_chat_member
        self.left_chat_memeber = left_chat_memeber
        self.new_chat_title = new_chat_title
        self.new_chat_photo = new_chat_photo
        self.pinned_message = pinned_message
        self.all_status = all_status


class Handlers:
    def __init__(self,
        commands : str = None,
        messages : MessagesHandlers = None,
        callback : callable = None,
        inline : callable = None,
        join_request : callable = None,
        greeting : callable =None,
    ):
        """
        Initialize a HANDLERS instance.

        This class is used to store callback functions for the Bot.

        Args:
            start_function: A callable that will be called when the Bot is started.
            commands: A string with the path to the commands folder.
            messages: A MessagesHandlers instance with the callback functions for the MessageHandler.
            callback: A callable that will be called when a callback query is received.
            inline: A callable that will be called when an inline query is received.
            join_request: A callable that will be called when a join request is received.
            reaction: A callable that will be called when a message reaction is received.
            error: A callable that will be called when an error occurs.
        """
        self.commands = commands
        self.messages = messages
        self.callback = callback
        self.inline = inline
        self.join_request = join_request
        self.greeting = greeting


class Bot:
    def __init__(
            self,
            name: str, 
            api_id: int, 
            api_hash: str, 
            token: str, 
            handler: Handlers = None,
            in_memory: bool = False, 
            workers: int=200,
            web : bool = False
            ):
        """
        Initialize a Bot instance.

        Args:
            name (str): The name of the bot.
            api_id (int): The API ID of the bot.
            api_hash (str): The API hash of the bot.
            token (str): The token of the bot.
            in_memory (bool): Whether to store the bot's data in memory.
            workers (int, optional): The number of workers to use for the bot. Defaults to 200.
        """
        self.name = name
        self.web = web
        self.api_id = api_id
        self.api_hash = api_hash
        self.token = token
        self.in_memory = in_memory
        self.workers = workers
        self.handler = handler

class User:
    def __init__(
            self,
            name: str, 
            api_id: int, 
            api_hash: str, 
            sesstion: str, 
            handler: Handlers = None,
            in_memory: bool = False, 
            workers: int=200,
            web: bool = True,
            ):
        """
        Initialize a Bot instance.

        Args:
            name (str): The name of the bot.
            api_id (int): The API ID of the bot.
            api_hash (str): The API hash of the bot.
            sesstion (str): The session string for the bot.
            in_memory (bool): Whether to store the bot's data in memory.
            workers (int, optional): The number of workers to use for the bot. Defaults to 200.
            web (bool, optional): Whether to enable web mode. Defaults to False.
        """
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash
        self.sesstion = sesstion
        self.in_memory = in_memory
        self.workers = workers
        self.handler = handler
        self.web = web
