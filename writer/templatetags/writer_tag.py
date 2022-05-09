from django import template
from django.utils.timezone import timedelta
from datetime import datetime

from projects.models import Project

register = template.Library()


@register.filter(is_safe=True)
def format_color(status):
    """Format the numbers decimal separator"""
    return {
        Project.CREATED: "#5797fc",
        Project.DRAFT: "#5797fc",
        Project.SEND: "#5797fc",
        Project.FOR_CORRECTION: "#DC3225FF",
        Project.IN_CORRECTION: "#FFCC29FF",
        Project.QUALIFIED: "#4ecc48",
    }.get(status)
