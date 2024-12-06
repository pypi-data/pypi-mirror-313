from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from allianceauth.services.hooks import get_extension_logger

from secretsanta.app_settings import (
    SECRETSANTA_GENERATE_PAIRS_PRIORITY, SECRETSANTA_NOTIFY_PRIORITY,
)
from secretsanta.models import Application, SantaPair, User, Year

from .tasks import generate_pairs, notify_outstanding_santees, notify_santas

logger = get_extension_logger(__name__)


def get_users_santee(year: Year, user: User) -> User | str:
    try:
        return SantaPair.objects.get(year=year, santa=user).santee
    except SantaPair.DoesNotExist:
        try:
            if Application.objects.filter(year=year, user=user).exists():
                return "Not Yet Assigned"
            else:
                ""
        except Exception:
            return ""
        return ""


def render_year(request, year) -> str:
    year_obj = Year.objects.get(year=year)

    context = {
        "year": year_obj,
        "application_exists": Application.objects.filter(year=year_obj, user=request.user).exists(),
        "santapair_exists": SantaPair.objects.filter(year=year_obj, santee=request.user).exists(),
        "gift_delivered": SantaPair.objects.filter(year=year_obj, santee=request.user, delivered=True).exists(),
        "users_santee": get_users_santee(year=year_obj, user=request.user),
    }
    return render_to_string("secretsanta/year.html", context, request)


@login_required
@permission_required("secretsanta.basic_access")
def index(request) -> HttpResponse:
    context = {'year_renders': []}
    for year in Year.objects.all().order_by("-year"):
        context['year_renders'].append(render_year(request, year=year.year))
    return render(request, "secretsanta/index.html", context)


@login_required
@permission_required("secretsanta.manager")
def pairs(request, year) -> HttpResponse:
    year_obj = Year.objects.get(year=year)
    context = {
        "year": year_obj,
        "pairs": SantaPair.objects.filter(year=year_obj)
    }
    return render(request, "secretsanta/pairs.html", context)


@login_required
@permission_required("secretsanta.manager")
def applications(request, year) -> HttpResponse:
    year_obj = Year.objects.get(year=year)
    context = {
        "year": year_obj,
        "applications": Application.objects.filter(year=year_obj)
    }
    return render(request, "secretsanta/applications.html", context)


@login_required
@permission_required("secretsanta.basic_access")
def apply(request, year) -> HttpResponse:
    year_obj = Year.objects.get(year=year)
    if year_obj.open is not True:
        messages.error(request, _('This year is not open for applications'))
        return redirect("secretsanta:index")
    try:
        Application.objects.create(year=year_obj, user=request.user)
        messages.success(request, _("Joined Secret Santa for {year}").format(year=year))
        return redirect("secretsanta:index")
    except ValidationError:
        messages.error(request, _("You may only join once"))
    except Exception as e:
        logger.error(f"secretsanta.views.apply() {request.user} {e}")
        messages.error(request, _('An unexpected error ocurred '))
    return redirect("secretsanta:index")


@login_required
@permission_required("secretsanta.basic_access")
def mark_received(request, year) -> HttpResponse:
    try:
        year_obj = Year.objects.get(year=year)
        sp = SantaPair.objects.get(year=year_obj, santee=request.user)
        sp.delivered = True
        sp.save()
        messages.success(request, _("Gift marked as received for {year}").format(year=year))
        return redirect("secretsanta:index")
    except ValidationError:
        messages.error(request, _("You have already received your gift"))
    except Exception as e:
        logger.error(f"secretsanta.views.mark_received() {request.user} {e}")
        messages.error(request, _('An unexpected error ocurred'))
    return redirect("secretsanta:index")


@login_required
@permission_required("secretsanta.manager")
def admin_delete_application(request, id) -> HttpResponse:
    try:
        year_obj = Application.objects.get(id=id)
        year_obj.delete()
        messages.success(request, _("Deleted SS Application"))
        return redirect("secretsanta:index")
    except ValidationError:
        messages.error(request, _("You have already received your gift"))
    except Exception as e:
        logger.error(f"secretsanta.views.admin_delete_application() {request.user} {e}")
        messages.error(request, _('An unexpected error occurred'))
    return redirect("secretsanta:index")


@login_required
@permission_required("secretsanta.manager")
def queue_generate_pairs(request, year) -> HttpResponse:
    try:
        generate_pairs.apply_async(
            args=[year], priority=SECRETSANTA_GENERATE_PAIRS_PRIORITY)
        messages.success(request, _("Celery Task Queued to Generate Secret Santa for {year}").format(year=year))
        return redirect("secretsanta:index")
    except Exception as e:
        logger.error(f"secretsanta.views.queue_generate_pairs() {request.user} {e}")
        messages.error(request, _('An unexpected error ocurred'))
    return redirect("secretsanta:index")


@login_required
@permission_required("secretsanta.manager")
def queue_notify_santas(request, year) -> HttpResponse:
    try:
        notify_santas.apply_async(
            args=[year], priority=SECRETSANTA_NOTIFY_PRIORITY)
        messages.success(request, _("Celery Task queue_notify_santas for {year}").format(year=year))
        return redirect("secretsanta:index")
    except Exception as e:
        logger.error(f"secretsanta.views.queue_generate_pairs() {request.user} {e}")
        messages.error(request, _('An unexpected error ocurred'))
    return redirect("secretsanta:index")


@login_required
@permission_required("secretsanta.manager")
def queue_notify_outstanding_santees(request, year) -> HttpResponse:
    try:
        notify_outstanding_santees.apply_async(
            args=[year], priority=SECRETSANTA_NOTIFY_PRIORITY)
        messages.success(request, _("Celery Task queue_notify_outstanding_santees for {year}").format(year=year))
        return redirect("secretsanta:index")
    except Exception as e:
        logger.error(f"secretsanta.views.queue_generate_pairs() {request.user} {e}")
        messages.error(request, _('An unexpected error ocurred'))
    return redirect("secretsanta:index")
