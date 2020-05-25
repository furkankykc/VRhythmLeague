# TODO: Insert clever settings mechanism
import django
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "leagueSystem.settings")
django.setup()
from League import services


#
# send_mail('mail subject', 'body content',settings.EMAIL_HOST_USER,['furkanfbr@gmail.com'], fail_silently=False)
# def test():
#     print(services.create_songs_from_json(services.read_json(os.path.join(settings.BASE_DIR, 'static/combinedScrapped.json'))))

def get_songs_from_saber(list=4, page=1):
    import requests
    lists = [
        'hot',
        'rating',
        'latest',
        'latest',
        'downloads',
        'plays',
    ]
    session = requests.Session()
    session.headers.update({'User-Agent': 'Furkankykc(SongSaver v0.1)  ({0})'.format(os.uname())})
    url = 'https://beatsaver.com/api/maps/{}/{}'.format(lists[list], page)
    resp = session.get(url)
    if resp.status_code != 200:
        # This means something went wrong.
        raise ValueError('GET /tasks/ {}'.format(resp.status_code))
    data = resp.json()
    services.create_songs_from_url(data)


def get_songs_bulk_saber(start_val=1, end_val=sys.maxsize):
    for i in range(start_val, end_val):
        get_songs_from_saber(4, i)
        print('Page:{}'.format(i).center(80, '-'))


# get_songs_bulk_saber(1400, 5000)

# services.create_season(name='Alpha Season', game=models.Game.objects.first(),
#                        starting_at=timezone.now() + dt.timedelta(weeks=1), typ=models.Type.objects.first(),sponsor_name='Vr Gaming Room')
