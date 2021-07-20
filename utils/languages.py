# Dictionary for flexible casting languages into proper Pastebin formats
languages = {'cpp'      : ['c++', 'с++', 'си++', 'сплюсплюс', 'сиплюсплюс', 'спп'],
             'c'        : ['с', 'си'],
             'python'   : ['питон', 'пайтон', 'питхон', 'pyton', 'piton'],
             'java'     : ['джава', 'жава', 'жаба', 'ява'],
             'js'       : ['жс', 'джс', 'javascript', 'жаваскрипт', 'джаваскрипт', 'жабаскрипт'],
             'csharp'   : ['c#', 'с#', 'сишарп', 'сишарп', 'сшарп']}


def normalize(lang):
    # Try to cast language to proper name
    # if failed return passed value

    lang = lang.replace(' ', '')

    if languages.get(lang):
        return lang
    
    for normalized, versions in zip(languages.keys(), languages.values()):
        if lang in versions:
            return normalized

    return lang