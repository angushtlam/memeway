from django import template

register = template.Library()


@register.filter
def get_other(user, chat):
    if user == chat.user_1:
        return chat.user_2.username
    return chat.user_1.username
