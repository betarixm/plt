from django.apps import AppConfig
from flag.models import Flag
from django.contrib.auth import get_user_model

Team = get_user_model()


def check_flag(team: Team, flag_str: str):
    f = Flag.objects.filter(flag=flag_str)
    if len(f) == 0:
        return False, None

    f = f[0]

    team.add_score(f.score)
    f.teams.add(team)

    return True, f


class FlagConfig(AppConfig):
    name = 'flag'
