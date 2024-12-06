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
        remaining = self.time_remaining
        return remaining.seconds // 3600 if remaining else None
    
    @property
    def minutes_remaining(self):
        """Calculate the remaining minutes from the time delta."""
        remaining = self.time_remaining
        return (remaining.seconds % 3600) // 60 if remaining else None
    
    @property
    def seconds_remaining(self):
        """Calculate the remaining seconds from the time delta."""
        remaining = self.time_remaining
        return remaining.seconds % 60 if remaining else None


    def save(self, *args, **kwargs):
        """
        Override save to ensure only one timer per system and planet exists.
        If a timer with the same eve_system and planet_number exists, it will be overwritten.
        """
        # Check for existing timers with the same system and planet
        existing_timer = SkyhookTimer.objects.filter(
            eve_system=self.eve_system,
            planet_number=self.planet_number,
        ).exclude(pk=self.pk).first()

        # If such a timer exists, delete it
        if existing_timer:
            existing_timer.delete()

        # Save the new/updated timer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.eve_system} - Planet {self.planet_number} - {self.countdown_time}"

