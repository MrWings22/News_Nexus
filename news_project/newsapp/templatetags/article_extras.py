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

from django import template
import math

register = template.Library()

@register.filter(name='reading_time')
def reading_time(content):
    if not content:
        return 0  # If content is empty, return 0 minutes
    
    words_per_minute = 200  # Average reading speed
    word_count = len(content.split())  # Count words in the article
    minutes = math.ceil(word_count / words_per_minute)  # Round up to nearest minute
    return minutes

@register.filter(name='wordcount')
def wordcount(content):
    return len(content.split()) if content else 0