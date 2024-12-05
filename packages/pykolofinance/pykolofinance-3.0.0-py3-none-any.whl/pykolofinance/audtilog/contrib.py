import re
from django.conf import settings
import jwt

SENSITIVE_KEYS = ['password', 'token', 'access', 'refresh', 'Authorization', 'pin', 'tx_pin']

if hasattr(settings, 'API_LOGGER_EXCLUDE_KEYS'):
    if type(settings.DRF_API_LOGGER_EXCLUDE_KEYS) in (list, tuple):
        SENSITIVE_KEYS.extend(settings.DRF_API_LOGGER_EXCLUDE_KEYS)


def get_headers(request=None):
    """
        Function:       get_headers(self, request)
        Description:    To get all the headers from request
    """
    regex = re.compile('^HTTP_')
    return dict((regex.sub('', header), value) for (header, value)
                in request.META.items() if header.startswith('HTTP_'))


def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except:
        return ''


def mask_sensitive_data(data, mask_api_parameters=True):
    mask_value = "***FILTERED***"
    # Check if data is a dictionary
    if isinstance(data, dict):
        # Create a copy of the dictionary to avoid modifying the original
        masked_data = {}
        for key, value in data.items():
            # If the key is in sensitive fields, mask the value
            if key in SENSITIVE_KEYS:
                masked_data[key] = mask_value
            else:
                # Recursively process nested structures
                masked_data[key] = mask_sensitive_data(value, mask_api_parameters)
        return masked_data

    # If data is a list, apply the function to each item in the list
    elif isinstance(data, list):
        return [mask_sensitive_data(item, mask_api_parameters) for item in data]

    # For other data types, return the data as is
    else:
        return data


def mask_sensitive_data_v1(data, mask_api_parameters=True):
    """
    Hides sensitive keys specified in sensitive_keys settings.
    Loops recursively over nested dictionaries.
    When the mask_api_parameters parameter is set, the function will
    instead iterate over sensitive_keys and remove them from an api
    URL string.
    """
    if type(data) is not dict:
        if mask_api_parameters and type(data) is str:
            for sensitive_key in SENSITIVE_KEYS:
                data = re.sub('({}=)(.*?)($|&)'.format(sensitive_key),
                              '\g<1>***FILTERED***\g<3>'.format(sensitive_key.upper()), data)
        # new code
        if type(data) is list:
            data = [mask_sensitive_data(item) for item in data]
        return data
    for key, value in data.items():
        if key in SENSITIVE_KEYS:
            data[key] = "***FILTERED***"

        if type(value) is dict:
            data[key] = mask_sensitive_data(data[key])

        if type(value) is list:
            data[key] = [mask_sensitive_data(item) for item in data[key]]

    return data


def decode_jwt_token(request):
    authorization_header = request.headers.get('Authorization', '')
    if authorization_header.startswith('Bearer '):
        token = authorization_header.split(' ')[1]
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            email = decoded_token.get('email')
            user_id = decoded_token.get('user_id')
            fullname = decoded_token.get('fullname')
            return email, user_id, fullname
        except jwt.DecodeError:
            # Handle decoding error (e.g., log it, return default values)
            return '', '', ''
    else:
        return '', '', ''
