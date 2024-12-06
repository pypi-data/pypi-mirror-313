import re

from django.apps import apps
from django.conf import settings


def get_site_url():  # regex sso url
    regex = r"^(.+)\/s.+"
    matches = re.finditer(regex, settings.ESI_SSO_CALLBACK_URL, re.MULTILINE)
    url = "http://"

    for m in matches:
        url = m.groups()[0]  # first match

    return url


def discordbot_active() -> bool:
    return apps.is_installed("aadiscordbot")


SECRETSANTA_GENERATE_PAIRS_PRIORITY = getattr(settings, "SECRETSANTA_GENERATE_PAIRS_PRIORITY", 1)
SECRETSANTA_NOTIFY_PRIORITY = getattr(settings, "SECRETSANTA_NOTIFY_PRIORITY", 5)
