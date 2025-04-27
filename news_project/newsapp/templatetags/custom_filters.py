# In your_app/templatetags/custom_filters.py
from django import template
from django.utils.timesince import timesince
from django.utils.timezone import now
import math

register = template.Library()

@register.filter
def get(dictionary, key):
    return dictionary.get(key)

def timesince_without_hours(value):
    # Generate the timesince string
    time_string = timesince(value, now())
    # Remove the "hours" portion
    if "hours" in time_string:
        time_string = time_string.split(",")[0]  # Keep only the first part (e.g., "2 days")
    return time_string


