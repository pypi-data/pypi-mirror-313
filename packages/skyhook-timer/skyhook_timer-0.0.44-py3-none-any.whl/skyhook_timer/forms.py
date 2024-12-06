from django import forms
from skyhook_timer.models import SkyhookTimer

class SkyhookTimerForm(forms.ModelForm):
    class Meta:
        model = SkyhookTimer
        fields = ['eve_system', 'planet_number', 'countdown_time']
