from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^random$', random_meme, name="random"),
    url(r'^random-ten$', load_ten_random, name="random_ten"),
]