import requests

from django.apps import AppConfig
from django.contrib.auth import get_user_model

from .models import SstiLog
from env.ssti import ssti_flag_pusher

Team = get_user_model()

class SstiConfig(AppConfig):
    name = 'ssti'


def check_ssti(target_team_name: str, query: str):
    target_team_list = Team.objects.filter(username=target_team_name)

    if len(target_team_list) != 1:
        return False, None
    
    target_team = target_team_list[0]

    ok, msg = is_valid_query(target_team, query)
    if not ok:
        return False, msg

    requests.get("http://plus.or.kr:37511", params={'query':form.query})
    return True, ""


def is_valid_query(target_team: Team, query: str):

    if len(Team.objects.filter(username=target_team.username)) == 0:
        return False, "으흠, 그런 이름을 가진 팀은 이 마을에 없는 것으로 압니다!"
    
    max_len = target_team.ssti_filter.max_len

    if max_len < len(query):
        return False, "조금 짧게 말씀해주실 수 있으실까요?"

    regex_filter_list = target_team.ssti_filter.regex_rule_list.all()

    for r in regex_filter_list:
        p = re.compile(r.regexp)
        if p.match(query):
            return False, "앗..! 그런 말씀은 박물관에서는 금지입니다만...."

    return True, ""