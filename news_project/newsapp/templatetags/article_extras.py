from django import template
import math

register = template.Library()

@register.filter
def reading_time(content):
    if not content:
        return 1
    words_per_minute = 200
    word_count = len(content.split())
    return math.ceil(word_count / words_per_minute)
