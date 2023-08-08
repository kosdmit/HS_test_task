from datetime import datetime, timedelta

from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import LoginForm, ReferrerCodeForm
from api.services import AuthCodeService
from hs_test_task.custom_settings import AUTH_CODE_ACTIVITY_TIME, REFERRAL_CODE_LENGTH, AUTH_ATTEMPTS_COUNT

from api.models import Customer


# Create your views here.
class AuthenticationView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        auth_code = request.data.get('auth_code')
        if auth_code:
            return self.check_auth_code(request, received_code=auth_code)
        elif phone_number:
            return self.send_auth_code(request, phone_number)
        else:
            return Response({'error': 'Phone number or auth code is required'},
                            status=status.HTTP_400_BAD_REQUEST)

    def check_auth_code(self, request, received_code):
        phone_number = request.session['phone_number']
        expire_date = request.session['auth_code_expiry_date']

        if request.session['auth_attempts_count'] == AUTH_ATTEMPTS_COUNT:
            return Response({'error': 'Exceeded the number of failed auth attempts'},
                            status=status.HTTP_400_BAD_REQUEST)

        if expire_date < datetime.now().timestamp():
            return Response({'error': 'Auth code is expired'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.session['auth_code'] == received_code:
            try:
                Customer.objects.get(phone_number=phone_number)
            except Customer.DoesNotExist:
                Customer.create_customer(phone_number)
            request.session['is_authenticated'] = True

            return Response({'auth_status': 'success'},
                            status=status.HTTP_200_OK)
        else:
            request.session['auth_attempts_count'] += 1
            return Response({'auth_status': 'failure'},
                            status=status.HTTP_403_FORBIDDEN)

    def send_auth_code(self, request, phone_number):
        request.session['phone_number'] = phone_number

        auth_code_service = AuthCodeService()
        request.session['auth_code'] = auth_code_service.auth_code
        auth_code_expiry_date = datetime.now() + timedelta(
            seconds=AUTH_CODE_ACTIVITY_TIME)
        request.session['auth_code_expiry_date'] = auth_code_expiry_date.timestamp()
        request.session['auth_attempts_count'] = 0

        status_code = auth_code_service.send_code(phone_number=phone_number)
        return Response(
            {'auth_code_sending_status': 'success' if status_code == 200 else 'failure'},
            status=auth_code_service.auth_code_sending_status_code)


class ProfileView(APIView):
    def get(self, request):
        if not request.session.get('is_authenticated'):
            return Response({'error': 'You are not authorized'},
                            status=status.HTTP_403_FORBIDDEN)

        phone_number = request.session['phone_number']
        customer = Customer.objects.get(phone_number=phone_number)

        referrals = Customer.objects.filter(activated_referral_code=customer.own_referral_code).all()
        referral_list = [referral.phone_number for referral in referrals]

        return Response({'phone_number': customer.phone_number,
                         'own_referral_code': customer.own_referral_code,
                         'activated_referral_code': customer.activated_referral_code,
                         'referrals': referral_list},
                        status=status.HTTP_200_OK)

    def post(self, request):
        if not request.session.get('is_authenticated'):
            return Response({'error': 'You are not authorized'},
                            status=status.HTTP_403_FORBIDDEN)

        phone_number = request.session['phone_number']
        customer = Customer.objects.get(phone_number=phone_number)
        if customer.activated_referral_code:
            return Response({'error': 'The referral code has already been activated'},
                            status=status.HTTP_400_BAD_REQUEST)

        received_code = request.data.get('referral_code')
        if not received_code:
            return Response({'error': 'Referral code is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        if len(received_code) != REFERRAL_CODE_LENGTH:
            return Response({'error': 'The format of referral code is wrong'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            referrer = Customer.objects.get(own_referral_code=received_code)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer with referral code you sent is not exists'},
                            status=status.HTTP_400_BAD_REQUEST)

        if received_code == customer.own_referral_code:
            return Response({'error': 'You can not activate your own referral code'},
                            status=status.HTTP_400_BAD_REQUEST)

        customer.activated_referral_code = received_code
        customer.save()
        return Response({'message': 'success'},
                        status=status.HTTP_200_OK)


class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['login_form'] = LoginForm()
        context['referrer_code_form'] = ReferrerCodeForm()

        return context
