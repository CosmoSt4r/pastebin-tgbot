import logging
import telebot

import utils.dpaste as dpaste
import utils.pastebin as pastebin
import utils.tokens as tokens

# Amount of created pastes (global var)
pastes_count: int = 0

# Create bot instance
bot = telebot.TeleBot(tokens.TELEGRAM_BOT_TOKEN)

# Logging settings
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
log = logging.getLogger('logger')


def parse_message(message: telebot.types.Message) -> tuple:
    # Read message from user and parse service (pastebin or dpaste), 
    # name, code and language from it
    
    name = message.reply_to_message.from_user.first_name
    if not name:
        name = "Anonymous"

    service = message.text.split()[0].replace('/', '')   
    lang = ' '.join(message.text.split()[1:])
    code = message.reply_to_message.text

    return service, name, code, lang


@bot.message_handler(func=lambda message : '/pastebin' in message.text or '/dpaste' in message.text)
def handle_paste_command(message: telebot.types.Message) -> telebot.types.Message:
    # Handling '/pastebin' and '/dpaste' commands

    # User must reply to message with code
    if not message.reply_to_message:
        return bot.reply_to(message, 'Вы должны ответить на сообщение с кодом')

    service, name, code, lang = parse_message(message)
    log.info(f'Got {service} request from {message.from_user.first_name} \
        for {lang if lang else "unspecified"} language')

    if service == 'pastebin':
        if tokens.PASTEBIN_API_TOKEN:
            paste = pastebin.create_paste(name, code, lang)
        else:
            paste = 'Невозможно загрузить на Pastebin. Попробуйте /dpaste'

    elif service == 'dpaste':
        paste = dpaste.create_paste(name, code, lang)

    else:
        log.error(f"Got an unexpected service: {service}")
        paste = 'Произошла ошибка'

    return bot.reply_to(message, paste, disable_web_page_preview=True)


@bot.message_handler(commands=['start'])
def handle_start_command(message: telebot.types.Message) -> telebot.types.Message:
    # Handling '/start' command

    log.info(f'{message.from_user.first_name} started bot')
    reply = 'Добро пожаловать!\nВведите /help для получения справки по использованию бота.'

    return bot.send_message(message.from_user.id, reply)


@bot.message_handler(commands=['help'])
def handle_help_command(message: telebot.types.Message) -> telebot.types.Message:
    # Handling '/help' command

    log.info(f'{message.from_user.first_name} reads help message')
    reply = '''
    Для того, чтобы бот загрузил ваш код для начала пришлите ему сообщение\
 с кодом, затем ответьте на него командой /pastebin *язык* или /dpaste *язык*.\n
Например:\n/pastebin c++ или /dpaste питон\n
Бот обработает сообщение и пришлет ссылку на страницу с вашим кодом. \
Каждая ссылка активна ровно 24 часа :)
    '''
    return bot.send_message(message.from_user.id, reply)


if __name__ == '__main__':
    log.info('Bot started')
    bot.polling()
    log.info('Bot shutdown')
