import datetime as dt

import humanize
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from smart_selects.db_fields import ChainedManyToManyField

from .validators import *

# Create your models here.

_max_length = 50


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PageModel(TimeStampMixin):
    slug = models.SlugField(verbose_name='Page URL', blank=True, allow_unicode=True)
    name = models.CharField(max_length=_max_length)

    class Meta:
        abstract = True

    #
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     super(PageModel, self).save()
    #     self.full_clean()
    #     self.slug = slugify(self.name)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return '{}'.format(self.name)


class Game(PageModel):
    logo = models.FileField(upload_to='documents/%Y/%m/%d/', default="", null=True)


class Difficulty(models.Model):
    # name = models.CharField(max_length=_max_length)
    # max_score = models.IntegerField()
    # stars = models.FloatField()
    length = models.IntegerField()
    duration = models.FloatField()
    bombs = models.IntegerField()
    notes = models.IntegerField()
    obstacles = models.IntegerField()
    njs = models.IntegerField()
    njs_offset = models.IntegerField()

    # ranked = models.BooleanField()

    class Meta:
        abstract = False


#
# class Difficulties(models.Model):
#     easy = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='diff1')
#     normal = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='diff_normal')
#     hard = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='diff_hard')
#     expert = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='diff_ex')
#     expert_plus = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='diff_exp_1')

#
# class Vote(models.Model):
#     count = models.BigIntegerField()
#
#     class Meta:
#         abstract = False
#
#
# class Votes(models.Model):
#     up_votes = models.OneToOneField(Vote, on_delete=models.CASCADE, related_name='Votes_up_votes')
#     down_votes = models.OneToOneField(Vote, on_delete=models.CASCADE, related_name='Votes_down_votes')


class Song(PageModel):
    key = models.CharField(max_length=40, primary_key=True, blank=True)
    picture = models.CharField(max_length=30, blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=150)
    hash = models.CharField(max_length=40)
    sub_name = models.CharField(max_length=_max_length)
    song_author_name = models.CharField(max_length=_max_length)
    level_author_name = models.CharField(max_length=_max_length)
    # diffs = models.OneToOneField(Difficulties, on_delete=models.CASCADE,related_name='diff_ez')
    easy = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='easy', null=True)
    normal = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='normal', null=True)
    hard = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='hard', null=True)
    expert = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='expert', null=True)
    expert_plus = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='expert_plus', null=True)

    up_votes = models.BigIntegerField()
    down_votes = models.BigIntegerField()

    downloads = models.BigIntegerField()
    plays = models.BigIntegerField()
    direct_download = models.URLField()
    download_url = models.URLField()
    cover_url = models.URLField()

    bpm = models.FloatField()
    heat = models.FloatField()
    rating = models.FloatField()

    def __str__(self):
        return '{}'.format(self.name)

    @classmethod
    def difficulties(cls):
        return ['easy', 'normal', 'hard', 'expert', 'expert_plus']

    # @property
    # def calculate_performance_point(self, difficulty: int):
    #     return self.difficulties()[difficulty] * self.rating

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.created_at = timezone.now()
        super(Song, self).save()


class Player(PageModel):
    name = models.CharField(max_length=_max_length)
    total_point = models.IntegerField(default=0)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    steam_link = models.URLField(blank=True)
    steam_uid = models.TextField(blank=True)
    profile_pic = models.URLField(blank=True)
    country = models.CharField(max_length=3, blank=True)
    real_name = models.CharField(max_length=_max_length, blank=True)
    timezone = models.CharField(max_length=_max_length, blank=True, null=True)

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Player.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.player.save()

    def calculate_total_point(self):
        # bugune kadar toplam lig puani
        pass

    def calculate_current_season_point(self):
        # suanki sezondak puani
        pass


class Type(models.Model):
    name = models.CharField(max_length=_max_length)
    is_daily = models.BooleanField()
    count = models.IntegerField(validators=[
        MaxValueValidator(24),
        MinValueValidator(1)
    ])
    song_count = models.IntegerField(validators=[
        MaxValueValidator(20),
        MinValueValidator(1)
    ])

    # difficulty = models.

    @property
    def time(self):
        return self.count if self.is_daily else self.count * 7

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Type, self).save()


class Season(PageModel):
    name = models.CharField(max_length=_max_length)
    sponsor_name = models.CharField(max_length=_max_length)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)

    starting_at = models.DateField(null=False)
    finishing_at = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = ("League Season")
        verbose_name_plural = ("League Seasons")

    EASY = 'EZ'
    NORMAL = 'NM'
    HARD = 'HD'
    EXPERT = 'EX'
    EXPERTPLUS = 'EP'
    difficulties = [
        (EASY, 'Easy'),
        (NORMAL, 'Normal'),
        (HARD, 'Hard'),
        (EXPERT, 'Expert'),
        (EXPERTPLUS, 'Expert Plus'),
    ]
    difficulty = models.CharField(
        max_length=2,
        choices=difficulties,
        default=HARD
    )

    #
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     self.full_clean()
    #     super(Season, self).save()
    #
    # def _do_update(self, base_qs, using, pk_val, values, update_fields, forced_update):
    #     self.finishing_at = self.starting_at + dt.timedelta(weeks=self.type.count)

    @property
    def is_season_started(self):
        return self.starting_at <= dt.datetime.now().date()

    @property
    def is_season_finished(self):
        if self.finishing_at is None:
            self.calculate_finishing_date()
            print(self.finishing_at)
        return self.finishing_at < dt.datetime.now().date()

    @classmethod
    def get_current_season(cls):
        seasons = cls.objects.filter(starting_at__lte=timezone.now(), finishing_at__gt=timezone.now())
        return seasons

    def calculate_finishing_date(self):
        self.finishing_at = self.starting_at + dt.timedelta(weeks=self.type.count)

    def get_difficulty(self, difficulty_code):
        return dict(self.difficulties)[difficulty_code]

    def clean(self):
        pass

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        super(Season, self).save()
        if self.finishing_at is None:
            self.calculate_finishing_date()

    def __str__(self):
        return '{}'.format(self.name.__str__())


class PlayList(PageModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    songs = ChainedManyToManyField(Song,
                                   horizontal=True,
                                   verbose_name="songs",
                                   chained_field="game",
                                   auto_choose=True,
                                   chained_model_field="game", blank=True)

    EASY = 'EZ'
    NORMAL = 'NM'
    HARD = 'HD'
    EXPERT = 'EX'
    EXPERTPLUS = 'EP'
    difficulties = [
        (EASY, 'Easy'),
        (NORMAL, 'Normal'),
        (HARD, 'Hard'),
        (EXPERT, 'Expert'),
        (EXPERTPLUS, 'Expert Plus'),
    ]
    difficulty = models.CharField(
        max_length=2,
        choices=difficulties,
        default=HARD
    )

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


class Week(PageModel):
    # name = models.CharField(max_length=_max_length, editable=False)
    description = models.TextField(blank=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=False, editable=False)
    # playlist = models.ForeignKey(PlayList, on_delete=models.SET_NULL, null=True)
    # game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    starting_at = models.DateField(null=False, editable=False)
    songs = models.ManyToManyField(Song,
                                   verbose_name="songs",
                                   blank=True
                                   )

    def __str__(self):
        return '{} | {} | {}'.format(self.season.game.name, self.name, self.season.get_difficulty_display())

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(Week, self).save()

    def clean(self):
        # max_releations(self.songs, self.song_count())
        pass

    def set_name(self, id):
        week_count = Week.objects.filter(season=self.season).count()
        max_week_count = self.season.type.count

        if self.season.type.count > week_count:
            if self.season.type.is_daily:

                self.name = "{1} {0} of {2} {0}s".format("day", id + 1,
                                                         max_week_count)
            else:

                self.name = "{1} {0} of {2} {0}s".format("week", id + 1,
                                                         max_week_count)

        else:
            raise ValueError("hasbeen Reached Maximum Week Count ")


class Achievement(models.Model):
    name = models.CharField(max_length=_max_length)
    description = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return '{}'.format(self.name)


class Score(TimeStampMixin):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, null=False)
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    difficulty_rank = models.FloatField(default=0)
    note_jump_movement_speed = models.FloatField(default=0)
    note_jump_start_beat_offset = models.FloatField(default=0)
    raw_score = models.FloatField(default=0)
    modified_score = models.FloatField(default=0)
    rawscore = models.FloatField(default=0)
    full_combo = models.BooleanField(default=0)
    good_cuts_count = models.IntegerField(default=0)
    bad_cuts_count = models.IntegerField(default=0)
    max_combo = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    # def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
    #     self.date = timezone.now()
    #     super()

    def __str__(self):
        return 'Player {3}, recorded {4} score on {1} in {2} game at {0}'.format(
            humanize.naturaltime(timezone.now() - self.created_at),
            self.song.name,
            self.game.name,
            self.player,
            self.score)
