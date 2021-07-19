import logging
import pastebin
import telebot
import tokens

# Create bot instance
bot = telebot.TeleBot(tokens.TELEGRAM_BOT_TOKEN)

# Logging settings
logging.basicConfig(filename='logs.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
log = logging.getLogger('logger')


def parse_message(message):
    # Read message from user and parse name, 
    # code and language from it
    
    name = message.reply_to_message.from_user.first_name
    if not name:
        name = "Anonymous"
        
    try:
        lang = message.text[message.text.find(' '):].strip()
    except IndexError:
        # if language isn't specified
        # ( bare '/pastebin' command passed )
        lang = 'cpp'
        
    code = message.reply_to_message.text

    return name, code, lang


@bot.message_handler(func=lambda message : '/pastebin' in message.text)
def handle_command(message):
    # Handling '/pastebin' command

    # User must reply to message with code
    if not message.reply_to_message:
        return bot.reply_to(message, 'Вы должны ответить на сообщение с кодом')

    name, code, lang = parse_message(message)
    log.info(f'Got request from {name} for {lang} language')

    return bot.reply_to(message, pastebin.create_paste(name, code, lang), disable_web_page_preview=True)


if __name__ == '__main__':
    log.info('Bot started')
    bot.polling()
    log.info('Bot shutdown')
