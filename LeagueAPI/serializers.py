# serializers.py
from rest_framework import serializers

from .models import Hero
from League.models import Score


class ScoreSerializer(serializers.ModelSerializer):
    # game = serializers.HyperlinkedIdentityField(view_name="LeagueAPI:game-detail")
    # song = serializers.HyperlinkedIdentityField(view_name="LeagueAPI:song-detail")
    player = serializers.HiddenField(default="")

    class Meta:
        model = Score
        fields = ('game', 'song','score','player')


    def create(self, validated_data):
        if 'user' not in validated_data:
            validated_data['player'] = self.context['request'].user
        return Score.objects.create(**validated_data)