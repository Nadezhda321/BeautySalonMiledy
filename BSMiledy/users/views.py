from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import RegisterForm
from django.contrib.auth import login

@login_required
def profile(request):
    return render(request, 'users/profile.html')

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)