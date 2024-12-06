from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import models, urls


class SecretSantaMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _("Secret Santa"),
            "fas fa-gifts fa-fw",
            "secretsanta:index",
            navactive=["secretsanta:"],
        )

    def render(self, request):
        if request.user.has_perm("secretsanta.basic_access"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu() -> SecretSantaMenuItem:
    return SecretSantaMenuItem()


@hooks.register("url_hook")
def register_urls() -> UrlHook:
    return UrlHook(urls, "secretsanta", r"^secretsanta/")


@hooks.register("secure_group_filters")
def filters():
    return [models.ActiveSecretSantaFilter]
