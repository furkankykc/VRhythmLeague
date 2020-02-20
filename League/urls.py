from django.conf.urls import url
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import include, path
from rest_framework import routers
from . import views
from django.contrib.auth import views as auth_views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    url(r'dashboard/$',views.dashboard, name='dashboard'),
    url(r'home/$', views.home, name='home'),
    url(r'game/$', views.gameSite, name='game'),
    url(r'leagues/$', views.leagues, name='leagues'),
    path('league/<int:game_pk>/<int:season_pk>', views.week, name='league'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'playlists/$', views.playlist, name='playlist'),
    path('playlist/game/<int:game_pk>', views.playlist_game, name='playlist_game'),
    path('playlist/id/<int:playlist_pk>', views.playlist_pk, name='playlist_pk'),
    path('season/<int:game_pk>/<int:season_pk>', views.week, name='weeks'),
    # path('season/(?P<game_pk>[0-9]+)/(?P<season_pk>[0-9]+)$', views.week, name='weeks')

    url(r'^login/$', LoginView.as_view(template_name='league/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page='login'), name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate,
        name='activate')

]