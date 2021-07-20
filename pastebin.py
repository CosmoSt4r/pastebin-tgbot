import requests

from languages import normalize_language
import tokens
from main import log, pastes_count


def catch_api_errors(api_response):
    # Catch various Pastebin API response errors
    # Logs the error and returns user-friendly error message
    
    if 'pastebin.com' in api_response:
        global pastes_count
        pastes_count += 1
        log.info(f'New paste created at {api_response}. Total: {pastes_count}')
        return api_response
    if 'api_paste_format' in api_response:
        log.warning('Undefined language')
        return 'Не понял язык. Попробуйте по-другому'
    if 'api_dev_key' in api_response:
        log.warning('Pastebin API dev key is wrong')
        return 'Неверный API ключ. Обратитесь к администратору'
    if 'api_user_key' in api_response:
        log.warning('Pastebin user key is wrong')
        return 'Неверный API ключ. Обратитесь к администратору'
    if 'maximum pastes' in api_response:
        log.warning('Pastebin limit exceeded')
        return 'Превышен лимит. Попробуйте позже'
    
    return 'Произошла ошибка'


def create_paste(name, code, lang):
    # Create paste with given parameters with 1 day time limit
    
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

        # If maximum pastes as user reached try to paste as guest
        # ( gives 10 additional pastes )
        if 'maximum pastes' in response.text:
            data['api_paste_private'] = 0
            data.pop('api_user_key')
            response = requests.post('https://pastebin.com/api/api_post.php', data=data)

    result = catch_api_errors(response.text)
        
    return result
