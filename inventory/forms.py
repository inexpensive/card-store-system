from django import forms
from django.forms import extras
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_countries import countries
from localflavor.ca.forms import CAPhoneNumberField, CAPostalCodeField, CAProvinceField, CAProvinceSelect

from inventory.models import Profile


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Required')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )


class ProfileForm(forms.ModelForm):
    model = Profile
    street_address = forms.CharField(max_length=150)
    other_address = forms.CharField(max_length=150, required=False)
    city = forms.CharField(max_length=100)
    province = CAProvinceField(widget=CAProvinceSelect)
    country = forms.ChoiceField(choices=list(countries))
    postal_code = CAPostalCodeField
    birth_date = forms.DateField(widget=extras.SelectDateWidget)
    phone_number = CAPhoneNumberField()

    class Meta:
        model = Profile
        fields = (
            'street_address',
            'other_address',
            'city',
            'province',
            'country',
            'postal_code',
            'birth_date',
            'phone_number',
        )
