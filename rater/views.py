import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rater.models import *


def get_chat(user, chat_key):
    chat = user.chats.filter(key=chat_key).first()

    if chat is None:
        chat = user.ignore_me_ignore_me.filter(key=chat_key).first()

    return chat


def random_chat(user):
    chat = random.choice(user.chats.all())

    print(chat)

    if chat is None:
        chat = random.choice(user.ignore_me_ignore_me.all())
        print(chat)
    return chat


@login_required
def index(request):

    if len(request.user.memes.all()) == 0:
        return redirect("rater:welcome")

    # if len(request.user.memes.all()) > 0:
    #     meme_to_compare = random.choice(request.user.memes.all())
    # else:
    #     meme_to_compare = random.choice(MemeImage.objects.all())
    #
    # tag_to_compare = random.choice(meme_to_compare.meme.tags.all())
    #
    # meme_to_use = random.choice(tag_to_compare.memes.all())
    #
    # image_to_use = random.choice(meme_to_use.images.all())
    #
    # if len(image_to_use.users_who_liked.all()) > 0:
    #     account = random.choice(image_to_use.users_who_liked.all())
    # else:
    account = random.choice(User.objects.all())

    while account == request.user:
        account = random.choice(User.objects.all())

    request.user.last_viewed = account
    request.user.save()

    return render(request, "discover/discover.html", {"account": account})


@login_required
def welcome(request):
    if len(request.user.memes.all()) > 0:
        return redirect("rater:index")
    memes = random.sample(list(Meme.objects.all()), 15)
    images = []
    for meme in memes:
        images.append(random.choice(meme.images.all()))
    return render(request, "discover/welcome.html", {"images": images})


@login_required
def load_ten_random(request):
    memes = random.sample(list(Meme.objects.all()), 10)
    images = []
    for meme in memes:
        images.append(random.choice(meme.images.all()).serialize)
    return JsonResponse({"response": "ok", "message": "Successfully loaded da memes.", "memes": images}, safe=False)


@login_required
def save_meme_to_account(request):

    if not request.user.is_authenticated:
        return JsonResponse({"response": "error", "message": "Dude, don't impersonate people."})

    if request.method != "POST":
        return JsonResponse({"response": "error", "message": "You don' messed up, boy. Can not satisfy. :o"})

    json_str = request.body.decode(encoding='UTF-8')
    data = json.loads(json_str)

    for entry in data:
        image = MemeImage.objects.filter(id=int(entry["image_id"])).first()

        if not image:
            return JsonResponse({"response": "error", "message": "Not a valid image! DOPE!"})

        if image not in request.user.memes.all():
            image.users_who_liked.add(request.user)

    image.save()

    return JsonResponse({"response": "ok", "message": "Ya memes are poppin' for good now!"})


@login_required
def downvote(request):
    account = request.user.last_viewed
    account.downvotes += 1
    account.save()

    return redirect("rater:index")


@login_required
def upvote(request):
    account = request.user.last_viewed
    request.user.liked.add(account)
    request.user.save()

    if request.user in account.liked.all():
        request.user.matches.add(account)
        account.matches.add(request.user)
        account.save()
        request.user.save()

    return redirect("rater:index")


@login_required
def random_meme(request):

    if request.method == "POST":
        meme_img = MemeImage.objects.filter(id=request.POST.get("pk", 0)).first()
        if int(request.POST.get("quality", 1)) == 0:
            if meme_img:
                meme_img.delete()
                print("Deleted meme.")

    meme = random.choice(Meme.objects.all())

    while len(meme.images.all()) == 0:
        meme = random.choice(Meme.objects.all())

    image = random.choice(meme.images.all())

    return render(request, "random.html", {"url": image.url, 'pk': image.id, "title": meme.title})


@login_required
def chat_room_init(request):
    if len(request.user.chats.all()) > 0:
        return redirect("rater:chat", chat_key=random_chat(request.user).key)
    messages.error(request, "You need to match with people before you can chat!")
    return redirect("rater:index")


@login_required
def chat_room(request, chat_key):
    chat = get_chat(request.user, chat_key)

    if chat is None:
        return redirect("rater:index")

    chats = request.user.chats.all()
    return render(request, "discover/chat.html", {"chats": chats, "chat": chat})


@login_required
def chat_room_add(request, chat_key):

    if request.method != "POST":
        return redirect("rater:chat", chat_key=chat_key)

    chat = get_chat(request.user, chat_key)

    if chat is None:
        return redirect("rater:index")

    message = Message.objects.create(text=request.POST.get("text", ""), chat=chat, sender=request.user)
    message.save()
    return redirect("rater:chat", chat_key=chat_key)


