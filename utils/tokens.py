import os

PASTEBIN_API_TOKEN = os.environ.get('PASTEBIN_API_TOKEN')
PASTEBIN_USER_TOKEN = os.environ.get('PASTEBIN_USER_TOKEN')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not (PASTEBIN_API_TOKEN and PASTEBIN_USER_TOKEN and TELEGRAM_BOT_TOKEN):
    raise ValueError('You must specify all tokens and set them as env variables')
