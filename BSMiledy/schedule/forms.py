from django import forms
from .models import DayOff

class DayOffForm(forms.ModelForm):
    class Meta:
        model = DayOff
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('end_date') and cleaned_data.get('date'):
            if cleaned_data['end_date'] < cleaned_data['date']:
                raise forms.ValidationError("Конечная дата не может быть раньше начальной")
        return cleaned_data