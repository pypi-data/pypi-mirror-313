from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls


class SkyhookTimerMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _("skyhook_timer"),
            "fas fa-clock",
            "skyhook_timer:view_timers",
            navactive=["skyhook_timer:"],
        )

    def render(self, request):
        return MenuItemHook.render(self, request)
        # if request.user.is_member:
        #     return MenuItemHook.render(self, request)
        # return ""


@hooks.register("menu_item_hook")
def register_menu():
    return SkyhookTimerMenuItem()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "skyhook_timer", r"^view_timers/")
