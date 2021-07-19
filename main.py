import logging
import pastebin
import telebot
import tokens

bot = telebot.TeleBot(tokens.TELEGRAM_BOT_TOKEN)
logging.basicConfig(filename='logs.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
log = logging.getLogger('logger')

def parse_message(message):

    name = message.reply_to_message.from_user.first_name
    if not name:
        name = "Anonymous"
    try:
        lang = message.text[message.text.find(' '):].strip()
    except IndexError:
        lang = 'cpp'
    code = message.reply_to_message.text

    return name, code, lang

@bot.message_handler(func=lambda message : '/pastebin' in message.text)
def handle_command(message):

    if not message.reply_to_message:
        return bot.reply_to(message, 'Вы должны ответить на сообщение с кодом')

    name, code, lang = parse_message(message)
    log.info(f'Got request from {name} for {lang} language')

    if code:
        paste_link = pastebin.create_paste(name, code, lang)
    else:
        return bot.reply_to(message, 'Я не вижу кода')

    log.info(f'Responded to {message.from_user.first_name}')
    return bot.reply_to(message, paste_link, disable_web_page_preview=True)

if __name__ == '__main__':
    log.info('Bot started')
    bot.polling()
    log.info('Bot shutdown')
