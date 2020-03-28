# serializers.py
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from League.models import Score, Season, Week, Song
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

        return Score.objects.create(**validated_data)


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['key', 'name', 'bpm']


class WeekSerializer(serializers.ModelSerializer):
    songs = SongSerializer(read_only=True, many=True)
    highscores = HighScoreSerializer(read_only=True, many=True)

    class Meta:
        model = Week
        fields = ['name', 'songs', 'highscores']
        read_only_fields = [f.name for f in Week._meta.get_fields()]

    def create(self, validated_data):
        pass


class SeasonSerializer(serializers.ModelSerializer):
    current_week = WeekSerializer(read_only=True)
    # game = serializers.PrimaryKeyRelatedField(read_only=True)
    is_applied = SerializerMethodField()

    class Meta:
        model = Season
        fields = ['name', 'is_season_started', 'current_week', 'is_applied', 'get_difficulty']
        read_only_fields = fields

    def create(self, validated_data):
        pass

    def get_is_applied(self, obj):
        season_list = obj.user_list.filter(id=self.context['request'].user.id)
        if season_list.count():
            return True
        else:

            return reverse('apply', args=[
                obj.id])


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
