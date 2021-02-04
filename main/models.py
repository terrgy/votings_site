from datetime import datetime
from random import randint

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


def image_directory_path(instance, filename):
    return 'user_uploaded/{}_{}'.format(datetime.now().timestamp(), randint(100000, 999999))


class Image(models.Model):
    image = models.ImageField(upload_to=image_directory_path)


class User(AbstractUser):
    status = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(to=Image, on_delete=models.SET_NULL, null=True)


class UserSettings(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)


class Folovers(models.Model):
    folover = models.IntegerField(default=0)
    to_user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)


class MyFolovers(models.Model):
    folover = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    to_user = models.IntegerField(default=0)


class Voting(models.Model):
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    published = models.DateTimeField(default=timezone.now)
    finished = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    type = models.IntegerField(default=2)
    image = models.ForeignKey(to=Image, on_delete=models.SET_NULL, null=True)

    def get_chosen_variants_ids(self, user):
        variants = self.votevariant_set.all()
        chosen_variants = variants.filter(votefactvariant__fact__author=user)
        return set([variant.pk for variant in chosen_variants])

    def is_voted(self, user):
        return self.votevariant_set.filter(votefactvariant__fact__author=user).exists()

    def is_favourite(self, user):
        return self.favouritevoting_set.filter(author=user).exists()


class VoteVariant(models.Model):
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)


class VoteFact(models.Model):
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)


class VoteFactVariant(models.Model):
    fact = models.ForeignKey(to=VoteFact, on_delete=models.CASCADE)
    variant = models.ForeignKey(to=VoteVariant, on_delete=models.CASCADE)


class Complaint(models.Model):
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=255)


class FavouriteVoting(models.Model):
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
