import os
import binascii
import re
from django.utils import timezone

from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from flag.models import Flag
from utils.generator import random_flag
from env.environ import ITEM_CATEGORY_XSS, XSS_SCORE
import base.models
from .models import XssLog
from .checkbot import check_alert

Team = get_user_model()

class XssConfig(AppConfig):
    name = 'xss'


def create_flag():
    flag = random_flag()
    Flag.objects.create(flag=flag, score=XSS_SCORE, category=ITEM_CATEGORY_XSS)
    return flag


def get_time_passed_after_last_attack(attack_team, target_team):
    now_time = int(timezone.localtime().strftime("%Y%m%d%H%M%S"))
    last_attack_time = 0
    try:
        attacks = XssLog.objects.filter(from_team=attack_team,
                                            to_team=target_team,
                                            succeed=True)
        if len(attacks) == 0:
            return now_time
        last_attack = attacks.last()
        last_attack_time = int(last_attack.created_at_korean_time.strftime("%Y%m%d%H%M%S"))
    except XssLog.DoesNotExist:
        pass
    print(now_time - last_attack_time)
    return now_time - last_attack_time


def query_xss(attack_team_name: str, target_team_name: str, query: str):
    if attack_team_name == target_team_name:
        return False, "자기자신은 공격할 수 없습니다.", 400

    try:
        target_team = Team.objects.get(username=target_team_name)
    except Team.DoesNotExist:
        return False, "그런 이름의 지구는 존재하지 않습니다.", 404

    ok, message, status_code, csp = is_valid_query(target_team, query)
    if not ok:
        return False, message, status_code

    hash = str(binascii.hexlify(os.urandom(32)),'utf8')

    xss_log = XssLog.objects.create(hash=hash)
    xss_log.from_team = attack_team_name
    xss_log.to_team = target_team_name
    xss_log.csp.add(*csp.all())
    xss_log.query = query
    xss_log.save()

    checked, succeed = check_alert(f'http://plus.or.kr:17354/xss/{xss_log.hash}/')
    xss_log.checked = checked
    xss_log.succeed = succeed
    xss_log.save()

    if not succeed:
        return False, "상대 지구가 CSP를 통해 해당 쿼리를 발견, 제거하였습니다.", 400
    return True, "", 200



def is_valid_query(target_team: Team, query: str):
    try:
        xssfilter = base.models.XssFilter.objects.get(owner=target_team)
    except Team.DoesNotExist:
        return False, "그런 이름의 지구는 존재하지 않습니다.", 404, None

    max_len = xssfilter.max_len
    if max_len < len(query):
        return False, "쿼리가 너무 깁니다. 발각될 위험이 있습니다.", 400, None

    regex_filter_list = xssfilter.regex_rule_list.all()
    for r in regex_filter_list:
        p = re.compile(r.regexp, re.I)
        if p.match(query):
            return False, "해당 지구가 차단한 문자열이 포함되어있습니다.", 400, None

    return True, "", 200, xssfilter.csp_rule_list