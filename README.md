
# Pastebin бот для Telegram

Бот, позволяющий загрузить отрывки вашего кода на [Pastebin](https://pastebin.com/) и [Dpaste](https://dpaste.org/)


## Как использовать?

- Переходим в [бота](https://t.me/thepastebinbot) и нажимаем **start**

- Отправляем свой отрывок кода

- Отвечаем на сообщение с кодом командой 

  - /pastebin _язык_
  - /dpase _язык_

- Получаем ссылку

Бот может работать не только в диалоге, но и в группах.

Примеры:
__________
![Example](https://raw.githubusercontent.com/CosmoSt4r/pastebin-tgbot/assets/screenshot.jpg?raw=true)
__________

## Как запустить?

В командной строке:

```bash
  git clone https://github.com/CosmoSt4r/pastebin-tgbot
  cd pastebin-tgbot
  python main.py
```

Для запуска бота необходимо инициализировать три переменные окружения

| Переменная | Описание                |
| :-------- | :----------------------- |
| `PASTEBIN_API_TOKEN` |**API** токен от Pastebin. Выдается при регистрации. |
| `PASTEBIN_USER_TOKEN` | **User** токен от Pastebin. Выдается по запросу. |
| `TELEGRAM_BOT_TOKEN` | Токен вашего Telegram бота |

Также, бота можно загрузить на [Heroku](https://dashboard.heroku.com/):

```bash
  heroku login
  heroku git:clone -a pastebin-tgbot
  git push heroku master
```