from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    url(r'dashboard/$', views.dashboard, name='dashboard'),
    url(r'home/$', views.home, name='home'),
    url(r'games/$', views.home, name='games'),
    path('leagues/', views.leagues, name='leagues'),
    url('contacts/$', views.week, name='contacts'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'playlists/$', views.playlist, name='playlist'),
    #
    url(r'songs/$', views.songs, name='songs'),
    url(r'search/', views.autocompleteModel, name='search'),
    #
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('playlist/game/<int:game_pk>', views.playlist_game, name='playlist_game'),
    path('playlist/<int:playlist_pk>', views.playlist_pk, name='playlist_pk'),
    path('song/<int:song_pk>', views.playlist_pk, name='song_pk'),
    path('season/<int:season_pk>', views.week, name='weeks'),
    path('game/<int:game_pk>', views.week, name='game'),
    #
    # url(r'^login/$', LoginView.as_view(template_name='league.html'), name='login'),
    url(r'^login/$', views.CustomLoginView.as_view(), name='login'),
    #
    url(r'^logout/$', LogoutView.as_view(next_page=''), name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate,
        name='activate'),

    url(r'^$', views.pink, name='pink'),
    path('news/', views.pink, name='pink_news'),
    path('aboutleague/', views.pink, name='pink_matches'),
    path('teams/', views.pink, name='pink_our_teams'),
    path('aboutus/', views.pink, name='pink_about_us'),
    path('sponsors/', views.pink, name='pink_sponsors'),
    path('games/<slug:game_slug>/', views.GameDetailView.as_view(), name='show_seasons'),
    path('games/<slug:game_slug>/leagues/<slug:season_slug>/', views.SeasonDetailView.as_view(), name='show_weeks'),
    path('games/<slug:game_slug>/leagues/<slug:season_slug>/weeks/<slug:week_slug>/', views.WeekDetailView.as_view(),
         name='show_songs'),
    # url(r'^(?P<full_slug>(.*))/$', views.pages, name='show_ll')

]
