from django.contrib.auth.forms import UserCreationForm
from .models import Client
from django import forms
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    first_name = forms.CharField(label=_("First Name"), max_length=150)
    last_name = forms.CharField(label=_("Last Name"), max_length=150)
    phone = forms.CharField(label=_("Phone Number"), max_length=20)
    birth_date = forms.DateField(label=_("Birth Date"), widget=forms.DateInput(attrs={'type': 'date'}))
    consent_pd = forms.BooleanField(label=_("I agree to the processing of personal data"), required=True)
    
    class Meta:
        model = Client
        fields = ('email', 'first_name', 'last_name', 'phone', 'birth_date', 'password1', 'password2', 'consent_pd')