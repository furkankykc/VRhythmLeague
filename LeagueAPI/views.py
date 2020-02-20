from typing import Any

from django.shortcuts import render

# Create your views here.
from idna import unicode
from rest_framework import viewsets, response, views
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ScoreSerializer
from League.models import Score, Game, Player


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer




class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        queryset = Score.objects.all()
        serializer_class = ScoreSerializer(
            Score.objects.filter(
                player=request.user,
                game=Game.objects.get(pk=pk)),
            many=True)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
            'scores': serializer_class.data
        }
        return Response(content)

    def post(self, request):
        score = request.data.get('score')
        score.player = Player.objects.get(user=request.user)
        # Create an score from the above data
        serializer = ScoreSerializer(data=score)
        # serializer.initial_data.game = Game.objects.get(pk=pk)
        # serializer.initial_data.player = request.user

        # if IsAuthenticated:
        #     if serializer.is_valid(raise_exception=True):
        #         serializer.validated_data.player.id = request.user.id
        #         score_saved = serializer.save()
        #         return Response({"success": "Score '{}' created successfully".format(score_saved.score)})
        # else:
        #     return Response({"Fail": "Score '{}' creating failed"})

    # def put(self, request, pk):
    #     saved_score = get_object_or_404(Score.objects.get(player=request.user), game=Game.objects.get(pk=pk))
    #     data = request.data.get('article')
    #     serializer = ScoreSerializer(instance=saved_score, data=data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         saved_score = serializer.save()
    #     return Response({"success": "Article '{}' updated successfully".format(saved_score.pk)})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)



