import datetime as dt
import statistics

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Max, Min, StdDev, Sum
from django.utils import timezone
from django.utils.text import slugify
from smart_selects.db_fields import ChainedManyToManyField

from League.mixins import normpdf
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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(PageModel, self).save()
        self.slug = slugify(self.name)

    #  self.full_clean()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        url = "/%s/" % self.slug
        page = self
        while page.parent:
            url = "/%s%s" % (page.parent.slug, url)
            page = page.parent
        return url


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
    easy = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='easy', blank=True, null=True)
    normal = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='normal', blank=True, null=True)
    hard = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='hard', blank=True, null=True)
    expert = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='expert', blank=True, null=True)
    expert_plus = models.OneToOneField(Difficulty, on_delete=models.CASCADE, related_name='expert_plus', blank=True,
                                       null=True)

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
    description = models.CharField(max_length=500)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    picture = models.ImageField(upload_to='season_pics/%Y/%m/%d/', default="documents/vrlogo.png", null=False,
                                blank=True)
    starting_at = models.DateField(null=False)
    finishing_at = models.DateField(null=True, blank=True)
    user_list = models.ManyToManyField(User, blank=True,
                                       related_name='applied_users')

    class Meta:
        verbose_name = "League Season"
        verbose_name_plural = "League Seasons"

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

    @property
    def get_photo_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        else:
            return "/static/league/img/vrom.jpg"

    @property
    def is_season_started(self):
        return self.starting_at <= dt.datetime.now().date()

    @property
    def is_season_finished(self):
        if self.finishing_at is None:
            self.calculate_finishing_date()
            print(self.finishing_at)
        return self.finishing_at < dt.datetime.now().date()

    # todo bunun daha efficent hali var yaziver bi zahmet
    @property
    def current_week(self):
        return self.get_current_week

    def get_current_week(self):
        if self.is_season_finished:
            current_week = self.week.last()
        else:
            current_week = self.week.first()
        for week in self.week.all():
            if week.is_active:
                current_week = week

        return current_week

    def history(self):
        return self.week.filter(finishing_at__lt=timezone.now().date()) | self.week.filter(
            pk=self.get_current_week().pk)

    def calculate_finishing_date(self):
        self.finishing_at = self.starting_at + dt.timedelta(weeks=self.type.count)

    def get_difficulty(self):
        return dict(self.difficulties)[self.difficulty]

    @property
    def week(self):
        return Week.objects.filter(season=self)

    def clean(self):
        pass

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        super(Season, self).save()
        if self.finishing_at is None:
            self.calculate_finishing_date()

    def __str__(self):
        return '{}'.format(self.name.__str__())

    @property
    def parent(self):
        return self.game

    def get_absolute_url(self):
        url = "/%s/" % self.slug
        page = self
        while page.parent:
            url = "/%s%s" % (page.parent.slug, url)
            page = page.parent
        return url

    def get_season_score(self, user: User = None):
        slist = []
        [slist.extend(list(week.calculate_winners())) if week.is_finished else None for week in self.week.all()]

        if user is not None:
            seasonScoreDict = {}

            for s in slist:
                if s['user'] in seasonScoreDict:
                    seasonScoreDict[s['user']] += s['score']
                else:
                    seasonScoreDict[s['user']] = s['score']
            if user.id in seasonScoreDict:
                return seasonScoreDict[user.id]
            else:
                return 0
        return slist

    @property
    def highscores(self):
        high = self.get_season_score()[:10]
        # for hg in high:
        #     hg['user'] = User.objects.get(pk=hg['user'])
        return high


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
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=False, editable=False, related_name='season_week')
    # playlist = models.ForeignKey(PlayList, on_delete=models.SET_NULL, null=True)
    # game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    starting_at = models.DateField(null=False, editable=False)
    finishing_at = models.DateField(null=False, editable=False)
    weight = models.IntegerField(null=False, default=1)
    songs = models.ManyToManyField(Song,
                                   verbose_name="songs",
                                   blank=True
                                   )

    def __str__(self):
        return '{} | {} | {}'.format(self.season.game.name, self.name, self.season.get_difficulty_display())

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     self.full_clean()
    #     super(Week, self).save()

    def clean(self):
        # max_releations(self.songs, self.song_count())

        pass

    def set_name(self, id=-1):

        if id > -1:
            week_count = Week.objects.filter(season=self.season).count()
            max_week_count = self.season.type.count
            if self.season.type.count > week_count:
                if self.season.type.is_daily:

                    self.name = "{1} {0} of {2} {0}s".format("day", id + 1,
                                                             max_week_count)
                else:

                    self.name = "{1} {0} of {2} {0}s".format("week", id + 1,
                                                             max_week_count)
                self.slug = slugify("%s" % self.name.split('of')[0])

            else:
                raise ValueError("hasbeen Reached Maximum Week Count ")

    @property
    def parent(self):
        return self.season

    def get_absolute_url(self):
        url = "/%s/" % self.slug
        page = self
        while page.parent:
            url = "/%s%s" % (page.parent.slug, url)
            page = page.parent
        return url

    @property
    def is_active(self):
        return self.starting_at < timezone.now().date() <= self.finishing_at

    @property
    def is_finished(self):
        return self.finishing_at > timezone.now().date()

    @property
    def highscores(self):
        # self.week_scores.filter(user).aggregate(StdDev('total_score'))['total_score__stddev']
        # return self.week_scores.values('user').annotate(score=Sum('score')).order_by('score')[:10]
        return self.week_scores.values('user').annotate(score=Sum('score')).order_by('-score')

    @property
    def get_highscores(self):
        # self.week_scores.filter(user).aggregate(StdDev('total_score'))['total_score__stddev']
        # return self.week_scores.values('user').annotate(score=Sum('score')).order_by('score')[:10]
        high = self.highscores[:10]
        for hg in high:
            hg['user'] = User.objects.get(pk=hg['user'])
        return high

    def get_user_score(self, user: User):
        try:
            highscore_user = self.highscores.get(user=user)
            return highscore_user['score']
        except ObjectDoesNotExist:
            return 0

    def get_user_rank(self, user: User):
        # self.week_scores.filter(user).aggregate(StdDev('total_score'))['total_score__stddev']
        # return self.week_scores.values('user').annotate(score=Sum('score')).order_by('score')[:10]
        hs = self.highscores
        for index, userScore in enumerate(hs):
            if user.pk == userScore['user']:
                return index + 1
        return 0

    def week_statistics(self, user: User):
        stats = {}
        songsPlayed = Score.objects.filter(week=self, user=user).values('song').distinct().count()
        stats.update(songs_played=songsPlayed)
        return stats

    def calculate_winners(self):
        win_len = 3
        high_scores = self.highscores[:win_len]
        for i in range(len(high_scores)):
            point = (win_len - i) * self.weight
            high_scores[i]['score'] = point
        return high_scores


class Achievement(models.Model):
    name = models.CharField(max_length=_max_length)
    description = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return '{}'.format(self.name)


class Score(TimeStampMixin):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
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

    # todo must contain daily missions
    week = models.ManyToManyField(Week, blank=True, related_name='week_scores')

    def apply_weeks(self):
        weeks = Week.objects.filter(songs__pk__exact=self.song.pk, season__user_list__in=[self.user],
                                    season__user_list__is_active=True)
        [self.week.add(week) for week in weeks.all()]

    def clean(self):
        player = Player.objects.get(user=self.user)
        player.total_score += self.score
        player.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(Score, self).save()
        self.apply_weeks()
    # def __str__(self):
    #     return 'Player {3}, recorded {4} score on {1} in {2} game at {0}'.format(
    #         humanize.naturaltime(timezone.now() - self.created_at),
    #         self.song.name,
    #         self.game.name,
    #         self.user,
    #         self.score)


class Post(TimeStampMixin):
    user = models.ForeignKey(User, models.CASCADE)
    detail = models.CharField(max_length=500)
    game_detail = models.CharField(max_length=80, blank=True, null=True)


class Player(PageModel):
    name = models.CharField(max_length=_max_length)
    total_score = models.IntegerField(default=0)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True, related_name='player')
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
    seasons = models.ManyToManyField(Season, related_name='player_seasons')
    BRONZE = 'Bronze'
    SILVER = 'Silver'
    PLATINIUM = 'Platinium'
    DIAMOND = 'Diamond'

    RANKS = [
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (PLATINIUM, 'Platinium'),
        (DIAMOND, 'Diamond'),
        # (EXPERTPLUS, 'Expert Plus'),
    ]

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Player.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.player.save()
    @classmethod
    def get_max_point_ever(cls) -> int:
        score = Player.objects.only('total_score').aggregate(Max('total_score'))['total_score__max']

        return score if score is not None else 0

    @classmethod
    def get_min_point_ever(cls) -> int:
        score = Player.objects.filter(total_score__gt=0).aggregate(Min('total_score'))['total_score__min']
        return score if score is not None else 0

    @classmethod
    def get_total_player_count(cls) -> int:
        return Player.objects.filter(total_score__gt=0).count()

    @classmethod
    def score_diffrence(cls) -> int:
        score_diffrence = cls.get_max_point_ever() - cls.get_min_point_ever()
        # score_norm = score_diffrence/cls.get_total_player_count()
        return score_diffrence

    @classmethod
    def score_diff_avg(cls) -> float:
        total_player_count = cls.get_total_player_count()
        score_norm = (Player.score_diffrence() / total_player_count) if total_player_count != 0 else 0
        return score_norm

    @classmethod
    def standart_deviation(cls):
        return Player.objects.filter(total_score__gt=0).aggregate(StdDev('total_score'))['total_score__stddev']

    @classmethod
    def mean(cls):
        player_list = Player.objects.filter(total_score__gt=0).values_list('total_score', flat=True)
        mean = statistics.mean(player_list) if player_list.count() > 0 else 0
        return mean

    def normalized_sore(self) -> float:
        return (50 - (
                self.total_score - Player.get_min_point_ever()) / Player.score_diffrence()) if Player.score_diffrence() != 0 else 0

    @property
    def calculate_normal(self):
        vary = Player.score_diff_avg()
        pdf = normpdf(self.total_score, Player.mean(), vary)
        # if self.total_score - Player.score_diff_avg():
        score_multiplier = Player.get_total_player_count() * 1000
        pd_score = pdf * (score_multiplier if self.total_score - Player.score_diff_avg() > 0 else -score_multiplier)
        if self.season_rank < 0:
            rank = ""
        elif pd_score > 0:
            if pd_score < 0.25:
                rank = self.DIAMOND
            elif pd_score < 0.5:
                rank = self.PLATINIUM
            else:
                rank = self.SILVER
        else:
            if pd_score > -0.25:
                rank = self.SILVER
            else:
                rank = self.BRONZE
        return rank
        #

    # def calculate_total_point(self):
    #     # bugune kadar toplam lig puani
    #     pass

    @property
    def season_rank(self):
        return (1 - self.normalized_sore()) * 50


class AlphaUsers(models.Model):
    steam_id = models.CharField(max_length=50)

    def __str__(self):
        try:
            return Player.objects.get(steam_uid=self.steam_id).user.username
        except ObjectDoesNotExist:
            return self.steam_id
