from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from League.tokens import account_activation_token
from . import models,forms


# Create your views here.


def home(request):
    games = models.Game.objects.all()
    context = {'games': games}
    return render(request, 'league/index.html', context)


def dashboard(request):
    # my_scores = models.Score.objects.filter(player=request.user)
    my_scores = models.Score.objects.all()
    context = {'scores': my_scores}
    return render(request, 'league/dashboard.html', context)


def profile(request):
    me = request.user
    context = {'me': me}
    return render(request, 'league/profile.html', context)


def leagues(request):
    _leagues = models.Season.objects.all()
    current_league = models.Season.objects.last()
    context = {'leagues': _leagues, 'c_league': current_league}
    return render(request, 'league/leagues.html', context)


def week(request, game_pk=1, season_pk=1):
    # season = models.Season.objects.get(pk=season_pk)
    # game = models.Game.objects.get(pk=game_pk)
    weeks = models.Week.objects.filter(season=season_pk, game=game_pk)
    current_week = models.Week.objects.last()
    context = {'weeks': weeks, 'c_week': current_week}
    return render(request, 'league/weeks.html', context)


def playlist(request):
    playlist = models.PlayList.objects.all()
    context = {'playlists': playlist}
    return render(request, 'league/playlists.html', context)


def playlist_pk(request, playlist_pk):
    playlist = models.PlayList.objects.get(pk=playlist_pk)
    context = {'playlist': playlist}
    return render(request, 'league/playlist.html', context)


def playlist_game(request, game_pk):
    playlist = models.PlayList.objects.filter(game=game_pk)
    context = {'playlists': playlist}
    return render(request, 'league/playlists.html', context)


def gameSite(request):
    return render(request,template_name='gameSite/index.html')



def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('league/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = forms.SignUpForm()
    return render(request, 'league/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'league/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.player.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'league/account_activation_invalid.html')