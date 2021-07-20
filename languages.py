# Dictionary for flexible casting languages into proper Pastebin formats
languages = {'с++': 'cpp', 'c++': 'cpp', 'си++' : 'cpp', 'с плюс плюс' : 'cpp', 'си плюс плюс' : 'cpp',
             'си': 'c', 'с' : 'c',
             'питон': 'python', 'питхон': 'python', 'пайтон': 'python'}


def normalize_language(lang):
    # Try to cast language into proper format
    # if failed return passed value
    return languages.get(lang) if languages.get(lang) else lang