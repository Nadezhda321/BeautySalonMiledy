from django import forms
from django.utils import timezone
from services.models import Master
from datetime import datetime
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.CharField(widget=forms.HiddenInput())  # Будет заполняться JS
    
    class Meta:
        model = Appointment
        fields = ['master', 'date', 'time', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.service = kwargs.pop('service', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if 'date' in self.fields:
            self.fields['date'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%d')
            self.fields['date'].widget.attrs['max'] = (
                timezone.now() + timezone.timedelta(days=30)
            ).strftime('%Y-%m-%d')
        
        if self.service:
            self.fields['master'].queryset = Master.objects.filter(
                specializations__specialization=self.service.type_service
            )
    
    def clean(self):
        cleaned_data = super().clean()
        master = cleaned_data.get('master')
        date = cleaned_data.get('date')
        time_str = cleaned_data.get('time')
        service = self.service
        
        if master and date and time_str and service:
            try:
                time_obj = datetime.strptime(time_str, '%H:%M').time()
                datetime_obj = timezone.make_aware(
                    datetime.combine(date, time_obj)
                )
                
                if datetime_obj < timezone.now():
                    raise forms.ValidationError("Нельзя записаться на прошедшее время")
                
                if not master.is_available_at(datetime_obj, service.duration):
                    raise forms.ValidationError("Выбранное время недоступно")
                
                cleaned_data['datetime'] = datetime_obj
            except ValueError:
                raise forms.ValidationError("Неверный формат времени")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.datetime = self.cleaned_data['datetime']
        instance.user = self.user
        instance.service = self.service
        
        if commit:
            instance.save()
        return instance