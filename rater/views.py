import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rater.models import *


@login_required
def index(request):
    return render(request, "discover/discover.html")


@login_required
def welcome(request):
    if len(request.user.memes.all()) > 0:
        return redirect("rater:index")
    memes = random.sample(list(Meme.objects.all()), 15)
    images = []
    for meme in memes:
        images.append(random.choice(meme.images.all()))
    return render(request, "rater/welcome.html", {"images": images})


@login_required
def load_ten_random(request):
    memes = random.sample(list(Meme.objects.all()), 10)
    images = []
    for meme in memes:
        images.append(random.choice(meme.images.all()).serialize)
    return JsonResponse({"response": "ok", "message": "Successfully loaded da memes.", "memes": images}, safe=False)


@login_required
@csrf_exempt
def save_meme_to_account(request):

    if not request.user.is_authenticated:
        return JsonResponse({"response": "error", "message": "Dude, don't impersonate people."})

    if request.method != "POST":
        return JsonResponse({"response": "error", "message": "You don' messed up, boy. Can not satisfy. :o"})

    json_str = request.body.decode(encoding='UTF-8')
    data = json.loads(json_str)

    image = MemeImage.objects.filter(id=int(data["image_id"])).first()

    if not image:
        return JsonResponse({"response": "error", "message": "Not a valid image! DOPE!"})

    image.users_who_liked.add(request.user)
    image.save()

    return JsonResponse({"response": "ok", "message": "Ya memes are poppin' for good now!"})


@login_required
def random_meme(request):

    if request.method == "POST":
        meme_img = MemeImage.objects.filter(id=request.POST.get("pk", 0)).first()
        if int(request.POST.get("quality", 1)) == 0:
            meme_img.delete()

    meme = random.choice(Meme.objects.all())
    image = random.choice(meme.images.all())

    return render(request, "random.html", {"url": image.url, 'pk': image.id})
