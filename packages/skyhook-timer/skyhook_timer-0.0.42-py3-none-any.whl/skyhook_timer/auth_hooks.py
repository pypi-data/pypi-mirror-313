from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import timedelta

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from .models import SkyhookTimer
from . import urls


class SkyhookTimerMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _("skyhook_timer"),
            "fas fa-clock",
            "skyhook_timer:view_skyhook_timers",
            navactive=["skyhook_timer:"],
        )

    def _calculate_count_for_user(self):
        """Calculate the number of timers with time remaining within 1 hour."""
        one_hour_from_now = now() + timedelta(hours=1)
        vulnerable_skyhooks = SkyhookTimer.objects.filter(
            countdown_time__lte=one_hour_from_now,  # Time within the next hour
            countdown_time__gt=now()               # Time still in the future
        ).count()
        return vulnerable_skyhooks if vulnerable_skyhooks > 0 else None

    def render(self, request):
        if request.user.has_perm('skyhook_timer.view_skyhooktimer'):
            self.count = self._calculate_count_for_user()
            return MenuItemHook.render(self, request)
        return ''


@hooks.register("menu_item_hook")
def register_menu():
    return SkyhookTimerMenuItem()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "skyhook_timer", r"^view_skyhook_timers/")
