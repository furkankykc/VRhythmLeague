from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from rest_framework import routers
from . import views
from django.contrib.auth import views as auth_views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    url(r'dashboard/$', views.dashboard, name='dashboard'),
    url(r'home/$', views.home, name='home'),
    url(r'games/$', views.home, name='games'),
    url(r'leagues/$', views.leagues, name='leagues'),
    url('^contacts/$', views.week, name='contacts'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'playlists/$', views.playlist, name='playlist'),

    url(r'songs/$', views.songs, name='songs'),
    url(r'^search/', views.autocompleteModel, name='search'),

    path('profile/<int:user_id>', views.profile, name='profile'),
    path('playlist/game/<int:game_pk>', views.playlist_game, name='playlist_game'),
    path('playlist/<int:playlist_pk>', views.playlist_pk, name='playlist_pk'),
    path('song/<int:song_pk>', views.playlist_pk, name='song_pk'),
    path('season/<int:season_pk>', views.week, name='weeks'),
    path('game/<int:game_pk>', views.week, name='game'),

    # url(r'^login/$', LoginView.as_view(template_name='league/login.html'), name='login'),
    url(r'^login/$', views.CustomLoginView.as_view(), name='login'),

    url(r'^logout/$', LogoutView.as_view(next_page='login'), name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate,
        name='activate'),

    url(r'^$', views.pink, name='pink'),
    path('news/', views.pink, name='pink_news'),
    path('matches/', views.pink, name='pink_matches'),
    path('teams/', views.pink, name='pink_our_teams'),
    path('aboutus/', views.pink, name='pink_about_us'),
    path('sponsors/', views.pink, name='pink_sponsors')
]
