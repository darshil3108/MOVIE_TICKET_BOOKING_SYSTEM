from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def currency(value):
    """Format value as currency."""
    try:
        return f"${float(value):.2f}"
    except (ValueError, TypeError):
        return "$0.00"

@register.simple_tag
def seat_status_class(seat, booked_seats):
    """Return CSS class for seat based on its status."""
    if seat.id in booked_seats:
        return "seat-booked"
    return "seat-available"
