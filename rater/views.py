from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rater.models import *


@login_required
def index(request):
    return render(request, "rater/rater_index.html")


@login_required
def load_ten_random(request):
    memes = random.sample(list(Meme.objects.all()), 10)
    images = []

    for meme in memes:
        images.append(random.choice(meme.images.all()).serialize)
    return JsonResponse(images, safe=False)


@login_required
def random_meme(request):

    if request.method == "POST":
        meme_img = MemeImage.objects.filter(id=request.POST.get("pk", 0)).first()
        if int(request.POST.get("quality", 1)) == 0:
            meme_img.delete()

    meme = random.choice(Meme.objects.all())
    image = random.choice(meme.images.all())

    return render(request, "random.html", {"url": image.url, 'pk': image.id})
