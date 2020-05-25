from django.db.models import Q
from rest_framework.utils import json

from League.models import *


# def get_users(*,fetched_by:User)-> Iterable[User]:
#     query =Q()
#     return models.Score.objects.filter(query)


def get_scores():
    return Score.objects.all()


def get_games():
    return Game.objects.all()


def get_leagues():
    return Season.objects.all()


def get_active_leagues():
    return Season.objects.all()


def get_current_part(season: Season) -> Week:
    week_id = (season.starting_at - timezone.now().date()) % (
        dt.timedelta(weeks=1) if not season.type.is_daily else dt.timedelta(days=1))
    week_date = season.starting_at + dt.timedelta(weeks=week_id)
    query = Q(season=season, starting_at=week_date)
    data = Week.objects.filter(query)
    return data


def get_week_id(week: Week) -> int:
    week_id = abs(week.season.starting_at - week.starting_at) / (
        dt.timedelta(weeks=1) if not week.season.type.is_daily else dt.timedelta(days=1))

    return int(week_id) + 1


def create_season_(season):
    create_season(typ=season.type,
                  name=season.name,
                  game=season.game,
                  description=season.description,
                  starting_at=season.starting_at,
                  sponsor_name=season.sponsor_name,
                  difficulty=season.difficulty
                  )


def create_season(*,
                  typ: Type,
                  name: str,
                  game: Game,
                  description:str,
                  starting_at: dt.date,
                  sponsor_name: str,
                  difficulty
                  ) -> Season:
    season, created = Season.objects.get_or_create(name=name,
                                                   type=typ,
                                                   game=game,
                                                   description=description,
                                                   starting_at=starting_at,
                                                   sponsor_name=sponsor_name,
                                                   difficulty=difficulty
                                                   )
    if created:
        season.save()
        Week.objects.bulk_create(create_week(season))

    return season


def create_week(season: Season) -> [Week]:
    weeks = []
    index = 0
    for i in range(season.type.count):
        delta_time = timezone.timedelta(days=i) if season.type.is_daily else timezone.timedelta(weeks=i)
        week = Week(
            starting_at=season.starting_at + delta_time,
            finishing_at=season.starting_at + delta_time * 2,
            season=season
        )
        week.set_name(index)
        index += 1
        weeks.append(week)
    return weeks


def clean_weeks(season: Season):
    Week.objects.filter(season=season).delete()


def create_song(*,
                name: str,
                game__id: int,
                key: int,
                hash_data: str,
                sub_name: str,
                level_author_name: str,
                song_author_name: str,
                easy,
                normal,
                hard,
                expert,
                expert_plus,
                downloads: int,
                plays: int,
                download_url: str,
                direct_download: str,
                cover_url: str,
                description: str,
                bpm: float,
                up_votes: int,
                down_votes: int,
                heat: float,
                rating: float
                ):
    song = Song(name=name,
                game_id=game__id,
                key=key,
                hash=hash_data,
                sub_name=sub_name,
                level_author_name=level_author_name,
                song_author_name=song_author_name,
                bpm=bpm,
                heat=heat,
                rating=rating,
                easy=easy,
                normal=normal,
                hard=hard,
                expert=expert,
                expert_plus=expert_plus,
                up_votes=up_votes,
                down_votes=down_votes,
                cover_url=cover_url,
                direct_download=direct_download,
                download_url=download_url,
                description=description,
                downloads=downloads,
                plays=plays
                )

    # song.easy = get_diffs_json(diffs_data, 0)
    # song.normal = get_diffs_json(diffs_data, 1)
    # song.hard = get_diffs_json(diffs_data, 2)
    # song.expert = get_diffs_json(diffs_data, 3)
    # song.expert_plus = get_diffs_json(diffs_data, 3)

    # song.up_votes = up_votes
    # song.down_votes = down_votes

    try:
        update_song = Song.objects.get(key=song.key)
    except Song.DoesNotExist:
        update_song = None
    if update_song is not None:
        update_song = song
        update_song.save()
    else:
        song.save()
    print(song)


def create_songs_from_json(json_data: list):
    for data in json_data:
        try:
            create_song(
                game__id=Game.objects.first().id,
                key=data['Key'],
                hash_data=data['Hash'],
                name=data['SongName'],
                sub_name=data['SongSubName'],
                level_author_name=data['LevelAuthorName'],
                song_author_name=data['SongAuthorName'],
                # diffs_data=data['Diffs'],
                bpm=data['Bpm'],
                # played_count=data['PlayedCount'],
                up_votes=data['Upvotes'],
                down_votes=data['Downvotes'],
                heat=data['Heat'],
                rating=data['Rating']

            )
        except Exception as ex:
            print('zaten var')

        # for dt in data['Diffs']:
        #     dt['Diff'],
        #     dt['Scores'],
        #     dt['Stars'],
        #     dt['Ranked'],


def create_songs_from_url(json_data: dict):
    for data in json_data['docs']:
        diffs = data['metadata']['characteristics'][0]['difficulties']
        create_song(
            game__id=Game.objects.first().id,
            key=data['key'],
            hash_data=data['hash'],
            name=data['metadata']['songName'],
            sub_name=data['metadata']['songSubName'],
            level_author_name=data['metadata']['levelAuthorName'],
            song_author_name=data['metadata']['songAuthorName'],
            # diffs_data=data['characteristics']['difficulties'],
            bpm=data['metadata']['bpm'],
            heat=data['stats']['heat'],
            rating=data['stats']['rating'],
            easy=get_diffs_json(diffs, 0),
            normal=get_diffs_json(diffs, 1),
            hard=get_diffs_json(diffs, 2),
            expert=get_diffs_json(diffs, 3),
            expert_plus=get_diffs_json(diffs, 4),
            description=data['description'],
            up_votes=data['stats']['upVotes'],
            down_votes=data['stats']['downVotes'],
            downloads=data['stats']['downloads'],
            plays=data['stats']['plays'],
            direct_download=data['directDownload'],
            download_url=data['downloadURL'],
            cover_url=data['coverURL']
        )


def read_json(path: str):
    with open(path, 'r') as file:
        data = json.load(file)
        file.close()
    return data


def get_diffs_json(json_data, diff_level):
    diff = [
        'easy',
        'normal',
        'hard',
        'expert',
        'expertPlus'
    ]
    if json_data[diff[diff_level]] is not None:
        diff = Difficulty(

            duration=json_data[diff[diff_level]]['duration'],
            length=json_data[diff[diff_level]]['length'],
            bombs=json_data[diff[diff_level]]['bombs'],
            notes=json_data[diff[diff_level]]['notes'],
            obstacles=json_data[diff[diff_level]]['obstacles'],
            njs=json_data[diff[diff_level]]['njs'],
            njs_offset=json_data[diff[diff_level]]['njsOffset']
        )
        diff.save()
        return diff


def get_songs():
    # .filter(hard__isnull=False)
    return Song.objects.filter(hard__isnull=False).order_by('-rating')


def get_posts():
    posts = Post.objects.all().order_by('-created_at')
    scores = get_scores().order_by('-created_at')
    scores_post = []
    for post in posts:
        post = Post(user=post.user,
                    detail=post.detail,
                    created_at=post.created_at)
        scores_post.append(post)

    for score in scores:
        score_post = Post(user=score.user,
                          game_detail=score.game.name,
                          detail='Scored on {} : {}'.format(score.song.name, score.score),
                          created_at=score.created_at)
        scores_post.append(score_post)

    all_posts = sorted(scores_post, key=lambda x: x.created_at)[::-1]

    return all_posts


def apply_for_season(season: Season,
                     user: User
                     ):
    if not season.is_season_started:
        season.user_list.add(user)
        return True
    else:
        return False


def update_seasons():
    for obj in Season.objects.all():
        clean_weeks(obj)
        Week.objects.bulk_create(create_week(obj))
