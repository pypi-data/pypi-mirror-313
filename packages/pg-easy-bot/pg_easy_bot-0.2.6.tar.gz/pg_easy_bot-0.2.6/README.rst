Introduction
============

We’ve built the bot framework you’ve been waiting for!
======================================================

Unlock seamless Telegram bot development with our intuitive, powerful framework. Tap into our thriving community for support and inspiration

Installing
==========

You can install or upgrade ``pg-easy-bot`` via

.. code:: shell

    $ pip install pg-easy-bot --upgrade

To install a pre-release, use the ``--pre`` `flag <https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-pre>`_ in addition.


Quick Start
===========
::

    from Easy_Bot.ext import pyroClient , Bot , Handlers , MessagesHandlers

    API_ID = ''
    API_HASH = ''
    TOKEN = ''

    app = pyroClient(
        bot = Bot(
            name = "test01",
            api_id=API_ID,
            api_hash=API_HASH,
            token=TOKEN,
            workers=200,
            in_memory=True,
            web = True
        ),
        handlers =  Handlers(
            commands='Bot/Commands'
        )
    )

    if __name__ == "__main__":
        app.start()

        
