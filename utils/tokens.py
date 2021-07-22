import os

PASTEBIN_API_TOKEN = os.environ.get('PASTEBIN_API_TOKEN')
PASTEBIN_USER_TOKEN = os.environ.get('PASTEBIN_USER_TOKEN')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError('You must specify Telegram bot token')
