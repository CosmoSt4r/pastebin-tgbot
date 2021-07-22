import requests

import main
import utils.languages as languages


def catch_api_errors(api_response: str) -> str:
    # Catch various Dpaste API response errors
    # Logs the error and returns user-friendly error message
    api_response = api_response.strip()

    if 'dpaste.com' in api_response:
        global pastes_count
        main.pastes_count += 1
        main.log.info(f'New paste created at {api_response}. Total: {main.pastes_count}')
        return api_response
        
    if 'Unknown syntax' in api_response:
        main.log.warning('Undefined language')
        return 'Не понял язык. Попробуйте по-другому'

    return 'Произошла ошибка'


def create_paste(name: str, code: str, lang: str) -> str:
    # Create paste with given parameters with 1 day time limit
    
    data = {'content':      code,
            'syntax':       languages.normalize(lang),
            'title':        name,
            'expiry_days':  1}

    response = requests.post('https://dpaste.com/api/v2/', data=data)
    
    if response.status_code != 201:
        main.log.error('API error. Response code is ' + str(response.status_code))
    result = catch_api_errors(response.text)
        
    return result
