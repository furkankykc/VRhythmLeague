from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import validators
from django.utils import timezone
from django.db import models

# Create your models here.
_max_length = 20


class Game(models.Model):
    name = models.CharField(max_length=_max_length)
    logo = models.FileField(upload_to='documents/%Y/%m/%d/', default="", null=True)

    def __str__(self):
        return '{}'.format(self.name)


class Song(models.Model):
    name = models.CharField(max_length=_max_length)
    picture = models.CharField(max_length=30, blank=True, null=True)
    keywords = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    # published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '{}'.format( self.name)


class Player(models.Model):
    name = models.CharField(max_length=_max_length)
    total_point = models.IntegerField(default=0)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Player.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.player.save()

    def calculate_total_point(self):
        # bugune kadar toplam lig puani
        pass

    def calculate_current_seaso_point(self):
        # suanki sezondak puani
        pass
    def __str__(self):
            return '{}'.format(self.name)


class Type(models.Model):
    name = models.CharField(max_length=_max_length)
    week_count = models.IntegerField(validators=[
            MaxValueValidator(24),
            MinValueValidator(1)
        ])

    def __str__(self):
        return '{}'.format(self.name)


class Season(models.Model):
    name = models.CharField(max_length=_max_length)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return '{}'.format(self.name)


class PlayList(models.Model):
    name = models.CharField(max_length=_max_length)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    songs = models.ManyToManyField(Song)
    # songs.queryset &= models.Q(
    #             game=game,
    #         )
    # filters = models.Q()

    # def __enter__(self):
    #     # First pop your kwargs that may bother the parent __init__ method
    #     # Then, let the ModelForm initialize:
    #
    #     # Finally, access the fields dict that was created by the super().__init__ call
    #     if self.game!= None:
    #         self.filters &= models.Q(
    #             game=self.game,
    #         )
    #     self.songs.queryset = Song.objects.filter(self.filters)

    def __str__(self):
        return '{}'.format(self.name)


class Week(models.Model):
    name = models.CharField(max_length=_max_length)
    description = models.TextField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE,null=False)
    playlist = models.ForeignKey(PlayList, on_delete=models.SET_NULL,null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return '{}'.format(self.name)


class Achievement(models.Model):
    name = models.CharField(max_length=_max_length)
    description = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return '{}'.format(self.name)


class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, null=False)
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    score = models.IntegerField(default=0)
    date = models.DateTimeField(blank=True, null=True)

    # def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
    #     self.date = timezone.now()
    #     super()

    def __str__(self):
        return 'Player {3}, recorded {4} score on {1} in {2} game at {0}'.format(self.date,
                                                              self.song.name,
                                                              self.game.name,
                                                              self.player,
                                                              self.score)
