from django import forms
from django.utils.timezone import now, timedelta

from skyhook_timer.models import SkyhookTimer

class SkyhookTimerForm(forms.ModelForm):
    days = forms.IntegerField(min_value=0, label="Days")
    hours = forms.IntegerField(min_value=0, max_value=23, label="Hours")
    minutes = forms.IntegerField(min_value=0, max_value=59, label="Minutes")
    class Meta:
        model = SkyhookTimer
        fields = ['eve_system', 'planet_number', 'countdown_time']
        widgets = {
            'countdown_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',  # HTML5 input type for date-time picker
                'class': 'form-control',
            }),
        }

        def clean(self):
            cleaned_data = super().clean()
            days = cleaned_data.get("days", 0)
            hours = cleaned_data.get("hours", 0)
            minutes = cleaned_data.get("minutes", 0)
            
            if days == 0 and hours == 0 and minutes == 0:
                raise forms.ValidationError("Time remaining cannot be zero.")
            
            countdown_time = now() + timedelta(days=days, hours=hours, minutes=minutes)
            cleaned_data['countdown_time'] = countdown_time
            return cleaned_data
        
        def save(self, commit=True):
            instance = super().save(commit=False)
            instance.countdown_time = self.cleaned_data['countdown_time']
            if commit:
                instance.save()
            return instance
