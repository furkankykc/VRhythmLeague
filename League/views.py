from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from League.services import *
from League.tokens import account_activation_token
from . import models, forms
from .mixins import AjaxTemplateMixin


# Create your views here.


def home(request):
    context = {'games': get_games()}
    return render(request, 'league/index.html', context)


def dashboard(request):
    # my_scores = models.Score.objects.filter(player=request.user
    context = {'scores': get_scores()}
    return render(request, 'league/dashboard.html', context)


def profile(request, user_id):
    profile = Player.objects.get(user_id=user_id)
    context = {'profile': profile}
    return render(request, 'components/profile.html', context)


def profile(request, user_id):
    profile = Player.objects.get(user_id=request.user.id)
    context = {'profile': profile}
    return render(request, 'components/profile.html', context)


def leagues(request):
    _leagues = models.Season.objects.all()
    current_league = models.Season.objects.last()
    context = {'leagues': _leagues, 'c_league': current_league}
    return render(request, 'league/leagues.html', context)


def week(request, season_pk=1):
    # season = models.Season.objects.get(pk=season_pk)
    # game = models.Game.objects.get(pk=game_pk)
    weeks = models.Week.objects.filter(season=season_pk)
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
    return render(request, template_name='gameSite/index.html')


@login_required
def songs(request):
    page = request.GET.get('page', 1)
    data = get_songs()
    count = data.count()
    # z = (count / 100) if count != 0 else 0

    paginator = Paginator(data, 100)  # min(500,(count / 100)*100 if count != 0 else 100))

    try:
        songs = paginator.page(page)
    except PageNotAnInteger:
        songs = paginator.page(1)
    except EmptyPage:
        songs = paginator.page(paginator.num_pages)
    context = {'songs': songs}
    return render(request, 'league/songs.html', context)


def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('components/mail/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = forms.SignUpForm()
    return render(request, 'components/auth/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'components/mail/account_activation_sent.html')


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
        return render(request, 'components/mail/account_activation_invalid.html')


class CustomLoginView(AjaxTemplateMixin, LoginView):
    template_name = 'components/auth/login.html'
    form_class = AuthenticationForm


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        print(q)
        search_qs = Song.objects.filter(name__startswith=q)
        results = []
        for r in search_qs[:5]:
            results.append(r.name)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def pink(request):
    path = request.path_info
    print('path=', path)
    if path == '/':
        return render(request, 'thema_vr/index.html')
    # elif path == '/news/':
    #     return render(request, 'thema_vr/news/index.html')
    elif path == '/aboutleague/':
        return render(request, 'thema_vr/all-matches/index.html')
    # elif path == '/teams/':
    #     return render(request, 'thema_vr/all-teams/index.html')
    elif path == '/aboutus/':
        return render(request, 'thema_vr/about-us-3/index.html')
    # elif path == '/sponsors/':
    #     return render(request, 'thema_vr/sponsor-page/index.html')
    else:
        return render(request, 'thema_vr/index.html')

    #     return render(request, 'thema_vr/sponsor-page/index.html')


from django.views.generic.detail import DetailView


class SeasonDetailView(DetailView):
    model = Week
    # This file should exist somewhere to render your page
    template_name = 'league/weeks.html'
    # Should match the value after ':' from url <slug:the_slug>
    slug_url_kwarg = 'the_slug'
    # Should match the name of the slug field on the model
    slug_field = 'slug'  # DetailView's default value: optional
