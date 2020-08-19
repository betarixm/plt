from django.apps import AppConfig
from django.contrib.auth import get_user_model

import pymysql
import re

from .models import SqliLog
from env.credential import MYSQL_PASS
from utils.mysql import sqli_db
from utils.mysql import raw_query

Team = get_user_model()


def get_sql_query(attack_team_name: str, target_team_name: str, query: str):
    target_team_list = Team.objects.filter(username=target_team_name)

    if len(target_team_list) != 1:
        return False, None

    target_team = target_team_list[0]

    if not is_valid_query(target_team, query):
        return False, None

    succeed, res = raw_query(sqli_db(target_team_name, MYSQL_PASS), query)

    sqli_log = SqliLog.objects.create()
    sqli_log.from_team = attack_team_name
    sqli_log.to_team = target_team_name
    sqli_log.query = query
    sqli_log.succeed = succeed
    sqli_log.return_value = res
    sqli_log.save()

    return succeed, res



def is_valid_query(target_team: Team, query: str):

    if len(Team.objects.filter(username=target_team.username)) == 0:
        return False

    max_len = target_team.sqli_filter.max_len

    if max_len < len(query):
        return False

    regex_filter_list = target_team.sqli_filter.regex_rule_list.all()

    for r in regex_filter_list:
        p = re.compile(r.regexp)
        if p.match(query):
            return False

    return True


class SqliConfig(AppConfig):
    name = 'sqli'
