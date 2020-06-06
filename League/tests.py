# TODO: Insert clever settings mechanism
# from __future__ import unicode_literals
import os
import sys

import django

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


def get_songs_bulk_saber(start_val=1, end_val=sys.maxsize, shortby: int = 1):
    for i in range(start_val, end_val):
        get_songs_from_saber(shortby, i)
        print('Page:{}'.format(i).center(80, '-'))


# get_songs_bulk_saber(236, 237, 1)
print("Example usage :\n0:hot\n1:rating\n2:latest\n3:downloads\n4:plays\nget_songs_bulk_saber(1, 5000,shortby = 1)\n")

# services.create_season(name='Alpha Season', game=models.Game.objects.first(),
#                        starting_at=timezone.now() + dt.timedelta(weeks=1), typ=models.Type.objects.first(),sponsor_name='Vr Gaming Room')
