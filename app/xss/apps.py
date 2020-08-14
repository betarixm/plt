import os
import binascii
import re
from datetime import datetime

from django.apps import AppConfig
from django.contrib.auth import get_user_model

from .models import XssTrial

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

    return True, target_team.xss_filter.csp_rule_list



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


def get_time_passed_after_last_attack(attack_team, target_team):
    last_attack_time = 0
    try:
        last_attack = XssTrial.objects.filter(from_team=attack_team,
                                            to_team=target_team,
                                            succeed=True).latest()
        last_attack_time = int(last_attack.created_at.strftime("%Y%m%d%H%M%S"))
    except XssTrial.DoesNotExist:
        pass
    
    return int(datetime.now().strftime("%Y%m%d%H%M%S")) - last_attack_time


def attack_xss(attack_team, target_team, query, csp):
    res, csp = prepare_xss(target_team, query)
    if not res:
        return "", False, False

    hash = str(binascii.hexlify(os.urandom(32)),'utf8')
    xss_trial = XssTrial.objects.create(hash=hash)
    xss_trial.from_team = attack_team
    xss_trial.to_team = target_team
    xss_trial.csp.add(*csp.all())
    xss_trial.query = query
    xss_trial.save()

    return xss_trial
    