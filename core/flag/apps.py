from django.apps import AppConfig
from django.contrib.auth import get_user_model

from .models import Flag
from base.models import Team


class FlagConfig(AppConfig):
    name = 'flag'


Team = get_user_model()


def check_flag(team: Team, flag_str: str):
    try:
        flag = Flag.objects.get(flag=flag_str)
        team = flag.teams.get(username=team.username)
    except Flag.DoesNotExist:
        return False, None
    except Team.DoesNotExist:
        pass
    else:
        return False, None
    
    team.apply_score(flag.score)
    flag.teams.add(team)
    return True, flag
