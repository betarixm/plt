from django.apps import AppConfig
from django.contrib.auth import get_user_model

from .models import Flag


class FlagConfig(AppConfig):
    name = 'flag'


Team = get_user_model()


def check_flag(team: Team, flag_str: str):
    flag = Flag.objects.filter(flag=flag_str).exclude(teams__username=team.username)
    if not flag:
        return False, None
    flag = flag[0]
    
    team.add_score(flag.score)
    team.save()
    flag.teams.add(team)

    return True, flag