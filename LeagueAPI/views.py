# Create your views here.
from django.utils import timezone
from idna import unicode
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.views import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from League.models import Score, Game, Player, Season, Week
from .serializers import ScoreSerializer, SeasonSerializer, WeekSerializer, SteamAuthTokenSerializer


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.filter(finishing_at__gte=timezone.now().date())
    serializer_class = SeasonSerializer


class WeekViewSet(viewsets.ModelViewSet):
    queryset = Week.objects.filter(finishing_at__gte=timezone.now().date())
    serializer_class = WeekSerializer


#
class ScoreView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        pass
        serializer_class = ScoreSerializer(
            Score.objects.filter(
                user=request.user,
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
        game = request.data.get('game')
        score.game = game
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


class SeasonGame(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    """
    Retrieve, update or delete a Season instance.
    """

    def get(self, request, pk, format=None):
        serializer_class = SeasonSerializer(Season.objects.filter(game=pk), many=True,
                                            context={'request': self.request})
        valid_data = []
        for data in serializer_class.data:
            if not data['is_applied'] != True and data['is_season_started'] == True:
                valid_data.append(data)
        return Response(valid_data)

    def get_serializer_context(self):
        return {'request': self.request}


class giveMeMyFuckingToken(ObtainAuthToken):
    serializer_class = SteamAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
