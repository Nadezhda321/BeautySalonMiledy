from django.contrib.auth.forms import UserCreationForm
from .models import Client

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Client
        fields = UserCreationForm.Meta.fields + ("email", )