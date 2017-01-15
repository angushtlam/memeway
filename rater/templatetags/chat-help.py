from django import template

register = template.Library()


@register.filter
def get_other(user, chat):
    return chat.get_other_user(user).username
