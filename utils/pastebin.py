import requests

import main
import utils.languages as languages
import utils.tokens as tokens


def catch_api_errors(api_response: str) -> str:
    # Catch various Pastebin API response errors
    # Logs the error and returns user-friendly error message
    
    if 'pastebin.com' in api_response:
        global pastes_count
        main.pastes_count += 1
        main.log.info(f'New paste created at {api_response}. Total: {main.pastes_count}')
        return api_response
    if 'api_paste_format' in api_response:
        main.log.warning('Undefined language')
        return 'Не понял язык. Попробуйте по-другому'
    if 'api_dev_key' in api_response:
        main.log.warning('Pastebin API dev key is wrong')
        return 'Неверный API ключ. Обратитесь к администратору'
    if 'api_user_key' in api_response:
        main.log.warning('Pastebin user key is wrong')
        return 'Неверный API ключ. Обратитесь к администратору'
    if 'maximum pastes' in api_response:
        main.log.warning('Pastebin limit exceeded')
        return 'Превышен лимит. Попробуйте позже'
    
    return 'Произошла ошибка'


def create_paste(name: str, code: str, lang: str) -> str:
    # Create paste with given parameters and 1 day time limit
    
    data = {'api_dev_key':              tokens.PASTEBIN_API_TOKEN,
            'api_option':               'paste',
            'api_paste_code':           code,
            'api_paste_private':        '1',
            'api_paste_name':           name,
            'api_paste_expire_date':    '1D',
            'api_user_key':             tokens.PASTEBIN_USER_TOKEN,
            'api_paste_format':         languages.normalize(lang)}

    if not tokens.PASTEBIN_USER_TOKEN:
        data['api_paste_private'] = 0
        data.pop('api_user_key')

    response = requests.post('https://pastebin.com/api/api_post.php', data=data)
    
    if response.status_code != 200:
        main.log.error('API error. Response: ' + response.text)

        # If user pastes limit exceeded try to paste as guest
        # ( gives 10 additional pastes )
        if 'maximum pastes' in response.text and tokens.PASTEBIN_USER_TOKEN:
            data['api_paste_private'] = 0
            data.pop('api_user_key')

            response = requests.post('https://pastebin.com/api/api_post.php', data=data)

    result = catch_api_errors(response.text)
        
    return result
