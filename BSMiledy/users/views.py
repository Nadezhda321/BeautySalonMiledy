from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import RegisterForm
from django.contrib.auth import login
from appointment.models import Appointment

@login_required
def profile(request):
    active_appointments = Appointment.objects.filter(
        user=request.user,
        status='active'
    ).order_by('datetime')
    
    archived_appointments = Appointment.objects.filter(
        user=request.user
    ).exclude(status='active').order_by('-datetime')
    
    return render(request, 'users/profile.html', {
        'active_appointments': active_appointments,
        'archived_appointments': archived_appointments,
    })

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)