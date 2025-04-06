from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import RegisterForm




@login_required #помечаем как требующую логина пользователя
def profile(request):
    return render(request, 'users/profile.html')

class RegiserView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)