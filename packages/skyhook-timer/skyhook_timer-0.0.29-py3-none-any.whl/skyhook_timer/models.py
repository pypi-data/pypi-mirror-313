from django.db import models
from django.utils.timezone import now

class SkyhookTimer(models.Model):
    eve_system = models.CharField(max_length=100)
    planet_number = models.PositiveIntegerField()
    countdown_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def time_remaining(self):
        """Calculate remaining time for the timer."""
        delta = self.countdown_time - now()
        return delta if delta.total_seconds() > 0 else None
    
    @property
    def hours_remaining(self):
        """Calculate the remaining hours from the time delta."""
        remaining = self.time_remaining()
        return remaining.seconds // 3600 if remaining else None

    def __str__(self):
        return f"{self.eve_system} - Planet {self.planet_number} - {self.countdown_time}"

