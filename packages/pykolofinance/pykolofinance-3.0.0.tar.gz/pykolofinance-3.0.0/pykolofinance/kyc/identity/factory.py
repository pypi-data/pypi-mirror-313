from .providers.base import BaseIdentityService
from .providers.dojah import DojahIdentityService
from .providers.mock import MockIdentityService


class IdentityFactory:
    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config
        self.providers = {
            "DOJAH": DojahIdentityService,
            'MOCK': MockIdentityService
        }

    def get_service(self, provider) -> BaseIdentityService:
        return self.providers[provider](**self.config)
