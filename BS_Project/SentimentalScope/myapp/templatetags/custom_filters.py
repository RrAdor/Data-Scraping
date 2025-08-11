from django import template

register = template.Library()

@register.filter
def div(value, arg):
    """Divides the value by the argument."""
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def duration_format(seconds):
    """Format seconds into MM:SS format."""
    try:
        seconds = int(float(seconds))
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02d}"
    except (ValueError, TypeError):
        return "0:00"
