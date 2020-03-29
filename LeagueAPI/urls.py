from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here

router = routers.DefaultRouter()
router.register(r'scores', views.ScoreViewSet)
router.register(r'seasons', views.SeasonViewSet)
router.register(r'weeks', views.WeekViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('score/<int:pk>', views.ScoreView.as_view()),
    path('score/', views.ScoreView.as_view()),
    path('season/game/<int:pk>', views.SeasonGame.as_view()),
    path('api-token-auth/', views.giveMeMyFuckingToken.as_view(), name='api_token_auth'),
    # url(r'score/$',views.ScoreView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]