from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
import random
from django.db.models import CASCADE


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
    def create_user(self, username, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have a username.')

        user = self.model(
            username=username.lower(),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    username = models.CharField(
        max_length=255,
        unique=True,
    )

    GENDER_CHOICES = (
        ("m", "Male"),
        ("f", "Female"),
        ("a", "Bread"),
        ("a", "All"),
    )

    gender_match = models.CharField(default="m", max_length=2, help_text="Gender for the user's match.",
                                    choices=GENDER_CHOICES)

    first_name = models.CharField(default="", max_length=128, help_text="The user's first name.")

    last_name = models.CharField(default="", max_length=128, help_text="The user's last name.")

    # memes = ForeignKey(ChosenMeme)

    liked = models.ManyToManyField("self", blank=True, related_name="liked_me")

    matches = models.ManyToManyField("self", blank=True, related_name="my_matches")

    # If they are an active user or not.
    is_active = models.BooleanField(default=True)

    # If they are P+P admin
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = "users"
        verbose_name_plural = "MemeConnect Users"
        verbose_name = "MemeConnect User"

    def get_full_name(self):
        # The user is identified by their email address
        return "%s %s %s" % (self.get_prefix_display(), self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):              # __unicode__ on Python 2
        return "%s : %s" % (self.get_short_name(), self.username)

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


class MemeImage(models.Model):

    meme = models.ForeignKey(Meme, related_name="images", on_delete=CASCADE)

    users_who_liked = models.ManyToManyField(User, related_name="liked_images")

    url = models.CharField(default="", max_length=256)

    class Meta:
        db_table = "meme_images"

    def __str__(self):
        return self.url

    @property
    def serialize(self):
        return {"title": self.meme.title, "url": self.url, "image_id": self.id, "meme_id": self.meme.id}
