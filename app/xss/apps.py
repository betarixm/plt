from django.apps import AppConfig
from django.contrib.auth import get_user_model
import re

from .checkbot import check_alert

Team = get_user_model()

class XssConfig(AppConfig):
    name = 'xss'


def prepare_xss(target_team_name: str, query: str):
    target_team_list = Team.objects.filter(username=target_team_name)

    if len(target_team_list) != 1:
        return False, False
    
    target_team = target_team_list[0]

    if not is_valid_query(target_team, query):
        return False, False

    return True, target_team.xss_filter.csp_rule_list.all()



    location = prepare_xss(target_team, query)

    return True, check_alert(base_uri + location)



def is_valid_query(target_team: Team, query: str):

    if len(Team.objects.filter(username=target_team.username)) == 0:
        return False
    
    max_len = target_team.xss_filter.max_len

    if max_len < len(query):
        return False

    regex_filter_list = target_team.xss_filter.regex_rule_list.all()

    for r in regex_filter_list:
        p = re.compile(r.regexp)
        if p.match(query):
            return False

    return True
