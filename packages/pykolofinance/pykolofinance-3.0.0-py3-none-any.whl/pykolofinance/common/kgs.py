from datetime import datetime
from time import time
import random

from django.conf import settings

from cuid2 import Cuid

CUID_GENERATOR: Cuid = Cuid(length=24)


def generate_unique_id() -> str:
    return CUID_GENERATOR.generate()


def generate_reference_code(length=14, prefix=None) -> str:
    generator: Cuid = Cuid(length=length)
    code = generator.generate().upper()
    if prefix:
        return f"{prefix}{code}"
    return code




def __generate_transaction_ref():
    random_number = random.randint(1, 999)
    salt = str(random_number).zfill(3)
    time_ref = str(time()).replace('.', '')[6:15]

    return f'{salt}{time_ref}'


def generate_session_id():
    """
    30 chars long
    1-6 - Source Bank Code
    7-18 - date time in yymmddHHmmss, with HH in 24 hours format
    19-30 - 12 char unique code
    """
    bank_code = settings.KOLOMONI_INSTITUTION_CODE
    date_ref = datetime.now().strftime('%y%m%d%H%M%S')
    tx_ref = __generate_transaction_ref()
    x = f'{bank_code}{date_ref}{tx_ref}'
    print(len(x))
    return x
