import requests
from django.conf import settings

from .base import BaseIdentityService, LookupResponse


class DojahIdentityService(BaseIdentityService):
    def __init__(self, **kwargs):
        self.base_url = settings.DOJAH_API_URL
        if settings.DOJAH_APP_ID is None or settings.DOJAH_API_KEY is None:
            raise Exception("Dojah API credentials not set")
        self.headers = {
            "AppId": settings.DOJAH_APP_ID,
            "Authorization": settings.DOJAH_API_KEY,
        }

    def lookup_advanced_bvn(self, bvn):
        params = {"bvn": bvn}
        response = requests.get(f"{self.base_url}/kyc/bvn/advance", headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            data = data.get("entity")
            selfie_verification = data.get("selfie_verification", {})
            return LookupResponse(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                middle_name=data.get("middle_name"),
                date_of_birth=data.get("date_of_birth"),
                photo=data.get("image"),
                gender=data.get("gender"),  # Todo: parse to Male or Female
                phone_number=data.get("phone_number1"),
                match=selfie_verification.get('match', False),
                confidence_value=selfie_verification.get("confidence_value"),
                nin=data.get("nin"),
            )
        return None

    def lookup_bvn(self, bvn):
        params = {"bvn": bvn}
        response = requests.get(f"{self.base_url}/kyc/bvn/full", headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            data = data.get("entity")
            selfie_verification = data.get("selfie_verification", {})
            return LookupResponse(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                middle_name=data.get("middle_name"),
                date_of_birth=data.get("date_of_birth"),
                photo=data.get("image"),
                gender=data.get("gender"),  # Todo: parse to Male or Female
                phone_number=data.get("phone_number1"),
                match=selfie_verification.get('match', False),
                confidence_value=selfie_verification.get("confidence_value")
            )
        return None

    def lookup_bvn_with_image(self, bvn, image):
        body = {"bvn": bvn, "selfie_image": image}
        url = f"{self.base_url}/kyc/bvn/verify"
        response = requests.post(url="https://api.dojah.io/api/v1/kyc/bvn/verify", headers=self.headers, json=body)
        if response.status_code == 200:
            data = response.json()
            data = data.get("entity")
            selfie_verification = data.get("selfie_verification", {})
            return LookupResponse(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                middle_name=data.get("middle_name"),
                date_of_birth=data.get("date_of_birth"),
                photo=data.get("image"),
                gender=data.get("gender"),  # Todo: parse to Male or Female
                phone_number=data.get("phone_number1"),
                match=selfie_verification.get('match', False),
                confidence_value=selfie_verification.get("confidence_value"),
            )
        return None

    def lookup_nin(self, nin):
        params = {"nin": nin}
        response = requests.get(f"{self.base_url}/kyc/nin", headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            data = data.get("entity")
            selfie_verification = data.get("selfie_verification", {})
            return LookupResponse(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                middle_name=data.get("middle_name"),
                date_of_birth=data.get("date_of_birth"),
                photo=data.get("photo"),
                gender=data.get("gender"),  # Todo: parse to Male or Female
                phone_number=data.get("phone_number1"),
                match=selfie_verification.get('match', False),
                confidence_value=selfie_verification.get("confidence_value"),
            )
        return None
