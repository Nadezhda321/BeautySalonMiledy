from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Master, Service, Appointment
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def create_appointment(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, service=service, user=request.user)
        if form.is_valid():
            appointment = form.save()
            return redirect('appointment:success')
    else:
        form = AppointmentForm(service=service, user=request.user)
    
    return render(request, 'appointment/create.html', {
        'form': form,
        'service': service
    })

@login_required
def available_slots(request):
    master_id = request.GET.get('master_id')
    date_str = request.GET.get('date')
    duration = int(request.GET.get('duration', 60))
    
    try:
        master = Master.objects.get(pk=master_id)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (Master.DoesNotExist, ValueError, TypeError):
        return JsonResponse({'slots': []})
    
    schedule = master.schedule
    start_time = schedule.default_start
    end_time = schedule.default_end
    lunch_start = schedule.lunch_start
    lunch_end = schedule.lunch_end
    
    slots = []
    current_time = datetime.combine(date, start_time)
    end_datetime = datetime.combine(date, end_time)
    
    while current_time + timedelta(minutes=duration) <= end_datetime:

        current_time_time = current_time.time()
        if not (lunch_start <= current_time_time < lunch_end):

            if master.is_available_at(current_time, duration):
                slots.append({
                    'time': current_time.strftime('%H:%M'),
                    'datetime': current_time.isoformat()
                })
        
        current_time += timedelta(minutes=30)
    
    return JsonResponse({'slots': slots})

@login_required
def appointment_success(request):
    return render(request, 'appointment/success.html')


@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    
    if appointment.status == 'active':
        appointment.status = 'canceled'
        appointment.save()
        messages.success(request, 'Запись успешно отменена')
    else:
        messages.error(request, 'Нельзя отменить эту запись')
    
    return redirect('users:profile')