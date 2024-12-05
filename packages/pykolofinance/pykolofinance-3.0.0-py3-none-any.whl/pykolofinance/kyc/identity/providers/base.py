from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class LookupResponse:
    first_name: str
    last_name: str
    middle_name: str
    date_of_birth: str
    photo: str
    gender: str
    phone_number: str
    confidence_value: str
    match: bool
    nin: Optional[str] = ""

    def to_dict(self):
        # Todo: normalize date of birth
        gender = {
            "m": "Male",
            "male": "Male",
            "f": "Female",
            "female": "Female",
        }
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "date_of_birth": self.date_of_birth,
            "photo": self.photo,
            "gender": gender[self.gender.lower()],
            "phone_number": self.phone_number,
            "match": self.match,
            "confidence_value": self.confidence_value,
            "nin": self.nin,
        }


class BaseIdentityService(ABC):
    @abstractmethod
    def lookup_bvn(self, bvn) -> LookupResponse:
        pass

    @abstractmethod
    def lookup_nin(self, nin) -> LookupResponse:
        pass

    @abstractmethod
    def lookup_advanced_bvn(self, bvn) -> LookupResponse:
        pass



    @abstractmethod
    def lookup_bvn_with_image(self, bvn, image) -> LookupResponse:
        pass


