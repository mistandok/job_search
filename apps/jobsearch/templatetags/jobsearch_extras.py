from django import template
from ..helpers.plural import plural_word

register = template.Library()


@register.filter()
def plural_ru(count, word):
    return plural_word(word, int(count))
