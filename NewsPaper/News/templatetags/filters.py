from django import template

censor = ['котики', 'подобию', 'стать']
register = template.Library()


@register.filter(name = 'block_words')
def block_words(value):
    News_text = value.split()
    for words in News_text:
        if words.lower() in censor:
            value = value.replace(words, '********')
    return value
