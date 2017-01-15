from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^welcome$', welcome, name="welcome"),
    url(r'^chat/(?P<chat_key>[0-9A-Za-z]+)$', chat_room, name="chat"),
    url(r'^chat/(?P<chat_key>[0-9A-Za-z]+)/add$', chat_room, name="chat"),
    url(r'^random$', random_meme, name="random"),
    url(r'^random-ten$', load_ten_random, name="random_ten"),
    url(r'^save-meme$', save_meme_to_account, name="save_meme"),
]