from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from social_core.exceptions import AuthForbidden
from social_core.pipeline.social_auth import social_uid
from social_core.pipeline.user import create_user
from social_django.middleware import SocialAuthExceptionMiddleware

from League.models import Player

#
#
# def save_profile(backend, user, response, *args, **kwargs):
#     if backend.name == 'steam':
#         profile = Player.objects.get(user=user)
#         if profile is None:
#             profile = Player(user_id=user.id)
#         # # profile.gender = response.get('gender')
#         # profile.link = response.get('link')
#         # profile.timezone = response.get('timezone')
#         # profile.save()
STEAM_DEF_RESPONSE_EX = {'steamid': '76561198103998111',
                         'communityvisibilitystate': 3,
                         'profilestate': 1,
                         'personaname': 'Bacı Zıbartan',
                         'commentpermission': 1,
                         'profileurl': 'https://steamcommunity.com/id/furkankykc/',
                         'avatar': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/93/93402f86ef78acbe444f7fabf3f0f7ef88304ac9.jpg',
                         'avatarmedium': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/93/93402f86ef78acbe444f7fabf3f0f7ef88304ac9_medium.jpg',
                         'avatarfull': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/93/93402f86ef78acbe444f7fabf3f0f7ef88304ac9_full.jpg',
                         'lastlogoff': 1582827518,
                         'personastate': 0,
                         'realname': 'Furkan kıyıkçı',
                         'primaryclanid': '103582791435246968',
                         'timecreated': 1377171040,
                         'personastateflags': 0,
                         'loccountrycode': 'TR',
                         'locstatecode': '68'}


def save_profile(strategy, details, backend, user=None, *args, **kwargs):
    if backend.name == 'steam':
        profile, created = Player.objects.get_or_create(user=user)
        # if not created:
        #     profile = Player(user_id=user.id)
        # profile.gender = response.get('gender')

        player = details.get('player')
        profile.steam_link = player['profileurl']
        profile.steam_uid = player['steamid']
        profile.profile_pic = player['avatarfull']
        profile.country = player['loccountrycode']
        profile.real_name = player['realname']
        profile.timezone = details.get('timezone')
        profile.save()


def create_just_activated_users(strategy, details, backend, user=None, *args, **kwargs):
    if backend.name == 'steam':
        if details.get('commentpermission') == 1:
            create_user(strategy, details, backend, user=None, *args, **kwargs)


def accept_only_auth(backend, details, response, *args, **kwargs):
    uid = social_uid(backend, details, response, *args, **kwargs)

    if not uid != 76561198019013458:
        raise AuthForbidden(backend)


def auth_allowed(backend, details, response, *args, **kwargs):
    uid = backend.get_user_id(details, response)
    if not fdauth_allowed(uid):
        # raise AuthForbidden(backend)
        return redirect(reverse('forbidden'))#<-here goes your url as defined on your urls.py


def fdauth_allowed(details):
    """Return True if the user should be allowed to authenticate, by
    default check if email is whitelisted (if there's a whitelist)"""
    uids = settings.WHITELISTED_UIDS
    # domains = self.setting('WHITELISTED_DOMAINS', [])
    uid = details
    allowed = False
    if uid and uids:
        # domain = email.split('@', 1)[1]
        allowed = uid in uids
    return allowed



