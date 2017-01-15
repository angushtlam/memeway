from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
import random
from django.db.models import CASCADE
from django.utils import timezone
from memeway import random_generator


class Tag(models.Model):

    text = models.CharField(default="", max_length=128)

    class Meta:
        db_table = "tags"

    @property
    def number_of_memes(self):
        return len(self.memes.all())

    def __str__(self):
        return self.text


class Meme(models.Model):

    title = models.CharField(default="", max_length=256)

    tags = models.ManyToManyField(Tag, blank=True, related_name="memes")

    class Meta:
        db_table = "memes"

    NONTAGS = ["a", "the", "of", "an", "with", "from", "but", "that", "that's"]

    def build_tags(self):
        # Iterate through by words
        for word in self.title.lower().split(" "):

            if word in Meme.NONTAGS:
                continue

            associated_tags = Tag.objects.filter(text__contains=word).all()

            if len(associated_tags) > 0:
                for tag in associated_tags:
                    tag.memes.add(self)
                    tag.save()
            else:
                self.tags.create(text=word)
                self.save()

    @property
    def number_picked(self):
        count = 0
        for image in self.images.all():
            count += len(image.users_who_liked.all())
        return count

    @property
    def get_random_url(self):
        return random.choice(self.images.all()).url

    def __str__(self):
        return self.title


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have a username.')

        user = self.model(
            username=username.lower(),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MemeImage(models.Model):

    meme = models.ForeignKey(Meme, related_name="images", on_delete=CASCADE)

    url = models.CharField(default="", max_length=256)

    class Meta:
        db_table = "meme_images"

    def __str__(self):
        return "%s Image: %s" % (self.meme.title, self.id)

    @property
    def serialize(self):
        return {"title": self.meme.title, "url": self.url, "image_id": self.id, "meme_id": self.meme.id}


class User(AbstractBaseUser):

    username = models.CharField(
        max_length=255,
        unique=True,
    )

    GENDER_CHOICES = (
        ("m", "Male"),
        ("f", "Female"),
        ("a", "Bread"),
        ("o", "Other"),
    )

    gender = models.CharField(default="m", max_length=2, help_text="Gender for the user's match.",
                                    choices=GENDER_CHOICES)

    description = models.TextField(default="My life is a meme 'cuz I have no description!")

    # memes = ForeignKey(ChosenMeme)

    downvotes = models.IntegerField(default=0)

    last_viewed = models.ForeignKey("self", related_name="last_viewed_me", null=True)

    memes = models.ManyToManyField(MemeImage, related_name="users_who_liked", blank=True)

    liked = models.ManyToManyField("self", blank=True, related_name="liked_me", symmetrical=False)

    matches = models.ManyToManyField("self", blank=True, related_name="my_matches")

    # If they are an active user or not.
    is_active = models.BooleanField(default=True)

    # If they are P+P admin
    is_admin = models.BooleanField(default=False)

    created_on = models.DateField(default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = "users"
        verbose_name_plural = "MemeConnect Users"
        verbose_name = "MemeConnect User"

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class ChatRoom(models.Model):

    key = models.CharField(default=random_generator, max_length=16)

    users = models.ManyToManyField(User, related_name="chats")

    class Meta:
        db_table = "chatrooms"

    def get_other_user(self, user):
        users = self.users.all()
        if user == users[0]:
            return users[1]
        return users[0]


class Message(models.Model):

    text = models.TextField(default="")

    chat = models.ForeignKey(ChatRoom, related_name="messages", on_delete=CASCADE, null=True)

    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=CASCADE)

    class Meta:
        db_table = "messages"
