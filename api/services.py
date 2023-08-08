import random
import string
import time

from hs_test_task.custom_settings import REFERRAL_CODE_LENGTH, AUTH_CODE_LENGTH


class AuthCodeService:
    def __init__(self):
        self.auth_code = self.generate_code()
        self.auth_code_sending_status_code = None

    @staticmethod
    def generate_code(length=AUTH_CODE_LENGTH):
        """Generate a random numeric code of a given length."""
        range_start = 10**(length-1)
        range_end = (10**length)-1
        return str(random.randint(range_start, range_end))

    def send_code(self, phone_number):
        """Mock sending the provided code to the provided phone number."""
        time.sleep(random.uniform(1, 2))
        print(f'Sent code {self.auth_code} to {phone_number}')
        self.auth_code_sending_status_code = 200
        return self.auth_code_sending_status_code


class ReferralCodeService:
    @staticmethod
    def generate_code(length=REFERRAL_CODE_LENGTH):
        all_characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(all_characters) for _ in range(length))
        return code
