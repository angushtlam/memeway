from django import template

register = template.Library()


@register.filter
def get_other(user, chat):
    return chat.get_other_user(user).username


@register.filter
def has_memecat(chat):
    for user in chat.users.all():
        if user.username == "memecat":
            return True
    return False
