from setuptools import setup, find_packages
from pathlib import Path
import codecs
import os

VERSION = '0.2.5'
DESCRIPTION = 'A module for create telegram bot easy'

def get_setup_kwargs(raw: bool = False):
    """Builds a dictionary of kwargs for the setup function"""

    raw_ext = "-raw" if raw else ""
    with open('README.rst') as r:
        readme = r.read()
    return {
        "name":"pg-easy-bot",
        "version":VERSION,
        "author":"Pamod Madubahana",
        "author_email":"premiumqtrst@gmail.com",
        "packages":find_packages(),
        "install_requires":['pyrofork','TgCrypto','pymongo','psutil','requests','aiohttp'],
        "keywords":['python', 'telegram bot', 'Easy Bots'],
        "description":"A module for create pyrogram bot with easy and fast",
        "long_description":readme,
        "long_description_content_type" : "text/x-rst",
        "classifiers": [
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
    }

if __name__ == '__main__':
    setup(**get_setup_kwargs(raw=False))


