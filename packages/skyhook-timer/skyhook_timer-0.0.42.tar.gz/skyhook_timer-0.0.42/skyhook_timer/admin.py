from django.contrib import admin
from .models import SkyhookTimer

class SkyhookTimerAdmin(admin.ModelAdmin):
    list_display = ('eve_system', 'planet_number', 'countdown_time', 'time_remaining')
    search_fields = ('eve_system',)
    list_filter = ('countdown_time',)

    # Restrict the permission to add or change timers
    def has_add_permission(self, request):
        # Only allow admins to add new timers
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        # Only allow admins to change timers
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # Only allow admins to delete timers
        return request.user.is_superuser

admin.site.register(SkyhookTimer, SkyhookTimerAdmin)
