from django.apps import AppConfig
from django.contrib.auth import get_user_model
import re

Team = get_user_model()

class XssConfig(AppConfig):
    name = 'xss'


def attack_xss(target_team_name: str, query: str):
    target_team_list = Team.objects.filter(name=target_team_name)

    if len(target_team_list) != 1:
        return False
    
    target_team = target_team_list[0]

    if not is_valid_query(target_team, query):
        return False

    return try_xss(target_team, query)



def is_valid_query(target_team: Team, query: str):

    if len(Team.objects.filter(name=target_team.username)) == 0:
        return False
    
    max_len = target_team.xss_filter.max_len

    if max_len < len(query):
        return False

    regex_filter_list = target_team.xss_filter.regex_rule_list

    for r in regex_filter_list.objects.all():
        p = re.compile(r.regexp)
        if p.match(query):
            return False

    return True


def try_xss(target_team: Team, query: str):
    pass
