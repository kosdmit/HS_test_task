from django.db import models

from api.services import ReferralCodeService
from hs_test_task.custom_settings import REFERRAL_CODE_LENGTH


# Create your models here.
class Customer(models.Model):
    phone_number = models.CharField(max_length=20)
    own_referral_code = models.CharField(max_length=REFERRAL_CODE_LENGTH)
    activated_referral_code = models.CharField(max_length=REFERRAL_CODE_LENGTH, null=True)

    @staticmethod
    def create_customer(phone_number):
        existing_customer = Customer.objects.filter(phone_number=phone_number).first()
        assert existing_customer is None

        Customer.objects.create(phone_number=phone_number,
                                own_referral_code=ReferralCodeService.generate_code())
