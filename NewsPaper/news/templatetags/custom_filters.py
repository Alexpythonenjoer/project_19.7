from django import template
import re

register = template.Library()

@register.filter()
def censor_filter(input_text):
    swear_words = ["swear1", "swear2", "swear3"]
    for word in swear_words:
        input_text = re.sub(r'\\b' + word + r'\\b', word[0] + "*"*(len(word)-1), input_text, flags=re.IGNORECASE)
    return input_text

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()