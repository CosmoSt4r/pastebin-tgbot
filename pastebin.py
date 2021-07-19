import requests
import tokens
from main import log

languages = {'с++': 'cpp', 'c++': 'cpp', 'си++' : 'cpp', 'с плюс плюс' : 'cpp', 'си плюс плюс' : 'cpp',
             'си': 'c', 'с' : 'c',
             'питон': 'python'}

def normalize_language(lang):
    return languages.get(lang) if languages.get(lang) else lang


def catch_api_errors(api_response):
    if 'pastebin.com' in api_response:
        log.info(f'New paste created at {api_response}')
        return api_response
    if 'api_dev_key' in api_response:
        log.warning('API key is expired')
        return 'Неверный API ключ. Обратитесь к администратору'
    if 'maximum pastes' in api_response:
        log.warning('Pastebin limit exceeded')
        return 'Превышен лимит. Попробуйте позже'
    if 'api_paste_format' in api_response:
        log.warning('Undefined language')
        return 'Не понял язык. Попробуйте по-другому'

    return 'Произошла ошибка'


def create_paste(name, code, lang):
    data = {'api_dev_key': tokens.PASTEBIN_API_TOKEN,
            'api_option': 'paste',
            'api_paste_code': code,
            'api_paste_private': '1',
            'api_paste_name': name,
            'api_paste_expire_date': '1D',
            'api_user_key': tokens.PASTEBIN_USER_TOKEN,
            'api_paste_format': normalize_language(lang)}

    response = requests.post('https://pastebin.com/api/api_post.php', data=data)
    if response.status_code != 200:
        log.error('API error. Response: ' + response.text)
    result = catch_api_errors(response.text)

    return result
