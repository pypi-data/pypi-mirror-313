from django.urls import path
from skyhook_timer import views

app_name = 'skyhook_timer'

urlpatterns = [
    path('', views.skyhook_timer_view, name='view_skyhook_timers'),
    path('add_skyhook_timer/', views.add_skyhook_timer_view, name='add_skyhook_timer'),
]
