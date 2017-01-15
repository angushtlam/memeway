from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^welcome$', welcome, name="welcome"),
    url(r'^my-account$', my_account, name="my_account"),
    url(r'^chat$', chat_room_init, name="chat_room_init"),
    url(r'^chat/(?P<chat_key>[0-9A-Za-z]+)$', chat_room, name="chat"),
    url(r'^chat/(?P<chat_key>[0-9A-Za-z]+)/add$', chat_room_add, name="chat_add"),
    url(r'^random$', random_meme, name="random"),
    url(r'^random-ten$', load_ten_random, name="random_ten"),
    url(r'^save-meme$', save_meme_to_account, name="save_meme"),
    url(r'^delete-meme$', delete_meme_from_account, name="delete_meme"),
    url(r'^upvote$', upvote, name="upvote"),
    url(r'^downvote$', downvote, name="downvote"),
    url(r'^view/(?P<username>[0-9A-Za-z]+)$', view_profile, name="view_profile"),
]