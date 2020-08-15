from django.apps import AppConfig
from django.contrib.auth import get_user_model

import pymysql
import re

from utils.mysql import sqli_db
from utils.mysql import raw_query

Team = get_user_model()


def get_sql_query(target_team_name: str, query: str):
    target_team_list = Team.objects.filter(username=target_team_name)

    if len(target_team_list) != 1:
        return False, None

    target_team = target_team_list[0]

    if not is_valid_query(target_team, query):
        return False, None

    return raw_query(sqli_db(), query)



def is_valid_query(target_team: Team, query: str):

    if len(Team.objects.filter(username=target_team.username)) == 0:
        return False

    teams_in_query = [t for t in Team.objects.all() if t.username in query]

    if len(teams_in_query) > 0:
        return False

    max_len = target_team.sqli_filter.max_len

    if max_len < len(query):
        return False

    regex_filter_list = target_team.sqli_filter.regex_rule_list.all()

    for r in regex_filter_list.regexp:
        p = re.compile(r.regexp)
        if p.match(query):
            return False

    return True


class SqliConfig(AppConfig):
    name = 'sqli'
