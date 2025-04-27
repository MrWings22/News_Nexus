from django import template
import math

register = template.Library()


@register.filter(name='reading_time')
def reading_time(content):
    if not content:
        return 0  # Return 0 if empty
    words_per_minute = 200  # Average reading speed
    word_count = len(content.split())  # Total words
    return math.ceil(word_count / words_per_minute)  # Reading time in minutes
   

@register.filter(name='wordcount')
def wordcount(content):
    return len(content.split()) if content else 0