from django import forms

class LoginForm(forms.Form):
    phone_number = forms.CharField(
        label='Phone:',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'value': '+7',
                                      'placeholder': 'Phone number'}),
    )

    auth_code = forms.CharField(
        label='Authorization code:',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Code'}),
    )


class ReferrerCodeForm(forms.Form):
    referrer_code = forms.CharField(
        label='Referrer code:',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Code'}),
    )