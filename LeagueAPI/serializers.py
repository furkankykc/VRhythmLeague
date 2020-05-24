# serializers.py
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from django.core.exceptions import ObjectDoesNotExist

from League.models import Score, Season, Week, Song, Player
from LeagueAPI import Crypter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class HighScoreSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    score = serializers.IntegerField()

    def get_user(self, value):
        return User.objects.get(id=value['user']).username


class ScoreSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Score
        fields = ['game', 'song', 'score', 'user', 'full_combo']

    def create(self, validated_data):
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
            try:
                _song = Song.objects.get(hash=validated_data['song'])
                validated_data['song'] = _song.key
                print(_song.key)
            except ObjectDoesNotExist as ex:
                pass

            return Score.objects.create(**validated_data)


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['key', 'hash', 'name', 'bpm']


class WeekSerializer(serializers.ModelSerializer):
    songs = SongSerializer(read_only=True, many=True)
    highscores = HighScoreSerializer(read_only=True, many=True)
    songs_played = SerializerMethodField()
    user_score = SerializerMethodField()
    user_rank = SerializerMethodField()

    class Meta:
        model = Week
        fields = ['name', 'songs', 'highscores', 'songs_played', 'user_score', 'user_rank']
        read_only_fields = [f.name for f in Week._meta.get_fields()]

    def create(self, validated_data):
        pass

    def get_songs_played(self, obj):
        return obj.week_statistics(self.context['request'].user)['songs_played']

    def get_user_score(self, obj):
        return obj.get_user_score(self.context['request'].user)

    def get_user_rank(self, obj):
        return obj.get_user_rank(self.context['request'].user)


class SeasonSerializer(serializers.ModelSerializer):
    current_week = WeekSerializer(read_only=True)
    # game = serializers.PrimaryKeyRelatedField(read_only=True)
    highscores = HighScoreSerializer(read_only=True, many=True)
    is_applied = SerializerMethodField()
    cover_url = SerializerMethodField()
    season_score = SerializerMethodField()
    season_rank = SerializerMethodField()

    class Meta:
        model = Season
        fields = ['name', 'is_season_started', 'current_week', 'is_applied', 'get_difficulty', 'cover_url',
                  'description', 'finishing_at', 'season_score', 'season_rank', 'highscores']
        read_only_fields = fields

    def create(self, validated_data):
        pass

    def get_cover_url(self, obj):
        return obj.get_photo_url

    def get_is_applied(self, obj):
        season_list = obj.user_list.filter(id=self.context['request'].user.id)
        if season_list.count():
            return True
        else:

            return reverse('apply', args=[
                obj.id])

    def get_season_score(self, obj):
        return obj.get_season_score(user=self.context['request'].user)

    def get_season_rank(self, obj):
        return Player(user_id=self.context['request'].user.id).calculate_normal


class SteamAuthTokenSerializer(serializers.Serializer):
    steamid = serializers.CharField(label=_("Steamid"),
                                    style={'input_type': 'password'}
                                    )

    def validate(self, attrs):
        encrypted_steamid = attrs.get('steamid')
        # password = attrs.get('key')

        # if username and password:
        #     user = authenticate(request=self.context.get('request'),
        #                         username=username, password=password)
        if encrypted_steamid:
            user = User.objects.get(player__steam_uid=Crypter.decrypt(encrypted_steamid))
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = _('Must include "steamid" and "key".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
