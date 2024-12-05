from rest_framework import exceptions


def clean_phone_number(phone_number: str) -> str:
    if len(phone_number) < 10 or len(phone_number) > 14:
        raise exceptions.ValidationError({'phone': f'Invalid phone number: {phone_number}'})
    if phone_number.startswith('+234') and len(phone_number) < 14:
        raise exceptions.ValidationError({'phone': f'Invalid phone number: {phone_number}'})
    if phone_number.startswith('234') and len(phone_number) == 13:
        return f"+{phone_number}"
    if phone_number.startswith('0') and len(phone_number) == 11:
        return f"+234{phone_number[1:]}"
    return phone_number


def clean_termii_phone(phone_number: str) -> str:
    return clean_phone_number(phone_number)[1:]
