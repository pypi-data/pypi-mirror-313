from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required

from skyhook_timer.models import SkyhookTimer
from skyhook_timer.forms import SkyhookTimerForm
import logging
logger = logging.getLogger(__name__)

@permission_required("skyhook_timer.view_skyhooktimer")
def skyhook_timer_view(request):
    # Get all timers for the member to view
    timers = SkyhookTimer.objects.all()
    sorted_timers = sorted(
        timers,
        key=lambda t: (t.time_remaining is None, t.time_remaining)
    )
    logger.info("Rendering the view_skyhook_timers template")
    # Render the view, allow "Members" to see but not interact with the data
    return render(request, 'skyhook_timer/view_skyhook_timers.html', {'timers': sorted_timers})


@permission_required('skyhook_timer.add_skyhooktimer', raise_exception=True)
def add_timer_view(request):
    """View for adding a new Skyhook Timer."""
    if request.method == "POST":
        form = SkyhookTimerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('skyhook_timer:view_timers')
    else:
        form = SkyhookTimerForm()
    return render(request, 'skyhook_timer/add_timer.html', {'form': form})
