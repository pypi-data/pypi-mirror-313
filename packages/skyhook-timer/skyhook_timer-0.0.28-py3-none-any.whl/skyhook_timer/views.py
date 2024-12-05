from django.shortcuts import render

from .models import SkyhookTimer
import logging
logger = logging.getLogger(__name__)
# from django.contrib.auth.decorators import state_required

# @state_required(['Member'])
def skyhook_timer_view(request):
    # Get all timers for the member to view
    timers = SkyhookTimer.objects.all()
    sorted_timers = sorted(
        timers,
        key=lambda t: (t.time_remaining is None, t.time_remaining)
    )
    logger.info("Rendering the view_timers template")
    # Render the view, allow "Members" to see but not interact with the data
    return render(request, 'skyhook_timer/view_timers.html', {'timers': sorted_timers})
