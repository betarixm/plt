from django.apps import AppConfig
from flag.models import Flag
from django.contrib.auth import get_user_model

Team = get_user_model()


def check_flag(team: Team, flag_str: str):
    flag = Flag.objects.filter(flag=flag_str).exclude(teams__username=team.username)[0]
    if not flag:
        return False, None

    team.add_score(flag.score)
    flag.teams.add(team)

    return True, flag


class FlagConfig(AppConfig):
    name = 'flag'
