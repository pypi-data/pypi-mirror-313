from django.urls import path
from . import views

app_name = 'skyhook_timer'

urlpatterns = [
    path('', views.skyhook_timer_view, name='view_skyhook_timers'),
]
