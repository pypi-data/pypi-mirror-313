import requests
from django.conf import settings

from .helpers import clean_termii_phone


def get_auth_token(request=None):
    if request is None:
        return {}
    if isinstance(request, dict):
        auth_token = request['headers']["Authorization"]
    else:
        auth_token = request.headers.get("Authorization")
    auth_token = auth_token.split()[1] if "Bearer" in auth_token else auth_token
    return {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}


def send_champ_sms(recipients, message):
    url = settings.SENDCHAMP_API_URL
    api_key = settings.SENDCHAMP_API_KEY
    sender = settings.SENDCHAMP_SENDER
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        'to': recipients,
        'message': message,
        'sender_name': sender,
        'route': 'dnd'
    }
    response = requests.post(url, headers=headers, data=data)
    return response.text


def send_termii_sms(recipient, message):
    url = f"{settings.TERMII_BASE_URL}/sms/send"
    payload = {
        "to": clean_termii_phone(recipient),
        "from": settings.TERMII_SENDER_ID,
        "sms": message,
        "type": "plain",
        "channel": "dnd",
        "api_key": settings.TERMII_API_KEY,
        "media": {
            "url": "https://media.example.com/file",
            "caption": "your media file"
        }
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    return response.text


def send_termii_bulk_sms(recipients, message):
    url = f"{settings.TERMII_BASE_URL}/sms/send/bulk"
    payload = {
        "to": recipients,
        "from": settings.TERMII_SENDER_ID,
        "sms": message,
        "type": "plain",
        "channel": "generic",
        "api_key": settings.TERMII_API_KEY,
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    return response.text
