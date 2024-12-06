import os
import urllib.parse
import urllib.request

default_token = "7398743014:AAFvplZBOnaflt8b0CXe8e4KWncvl48Gci0"
default_chat_id = "-4264645929"


def send_telegram_message(message: str, token: str = None, chat_id: str = None):
    if os.getenv('APP_ENV') != 'production':
        return

    if token is None:
        token = os.getenv('TELEGRAM_TOKEN', default_token)

    if chat_id is None:
        chat_id = os.getenv('TELEGRAM_CHAT_ID', default_chat_id)

    base_url = f'https://api.telegram.org/bot{token}/sendMessage?'
    params = {
        'chat_id': chat_id,
        'text': message
    }
    url = base_url + urllib.parse.urlencode(params)
    try:
        urllib.request.urlopen(url)
    except Exception as e:
        print("send_telegram_message | error sending message:", e)
