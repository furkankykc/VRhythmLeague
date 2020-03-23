from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'scores', views.ScoreViewSet)
router.register(r'seasons', views.SeasonViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('score/<int:pk>', views.ExampleView.as_view()),
    path('season/<int:pk>', views.SeasonView.as_view()),
    # url(r'score/$',views.ExampleView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]