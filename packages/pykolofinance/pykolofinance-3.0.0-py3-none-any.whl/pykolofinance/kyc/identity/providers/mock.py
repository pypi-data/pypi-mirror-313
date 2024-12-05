import random

from faker import Faker

from .base import BaseIdentityService, LookupResponse


class MockIdentityService(BaseIdentityService):
    def lookup_bvn(self, bvn):
        fake = Faker()
        return LookupResponse(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            middle_name=fake.name_female(),
            date_of_birth=str(fake.date_of_birth()),
            gender=random.choice(['Male', 'Female']),
            photo='',
            phone_number=self.generate_nigerian_phone_number(),
            match=bool(random.randint(0, 1)),
            confidence_value='90.000'

        )

    def lookup_advanced_bvn(self, bvn):
        fake = Faker()
        return LookupResponse(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            middle_name=fake.name_female(),
            date_of_birth=str(fake.date_of_birth()),
            gender=random.choice(['Male', 'Female']),
            photo='',
            phone_number=self.generate_nigerian_phone_number(),
            match=bool(random.randint(0, 1)),
            confidence_value='90.000',
            nin=str(random.randint(10000000000, 99999999999))

        )

    def lookup_nin(self, nin):
        fake = Faker()
        return LookupResponse(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            middle_name=fake.name_female(),
            date_of_birth=str(fake.date_of_birth()),
            gender=random.choice(['Male', 'Female']),
            photo='',
            phone_number=str(fake.phone_number()),
            match=bool(random.randint(0, 1)),
            confidence_value='80.000'

        )

    def lookup_bvn_with_image(self, bvn, image):
        fake = Faker()
        confidence_value = round(random.uniform(10.0, 100.0), 2)

        return LookupResponse(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            middle_name=fake.name_female(),
            date_of_birth=str(fake.date_of_birth()),
            gender=random.choice(['Male', 'Female']),
            photo=image,
            phone_number=self.generate_nigerian_phone_number(),
            match=True,
            confidence_value=str(confidence_value)

        )

    @staticmethod
    def generate_nigerian_phone_number():
        country_code = "+234"
        first_digit = random.choice(['70', '80', '81', '90', '91'])
        remaining_digits = random.randint(10000000, 99999999)

        phone_number = f"{country_code}{first_digit}{remaining_digits}"
        return phone_number
