from django.apps import AppConfig

from sqli.models import SqliLog
from xss.models import XssLog
from env.environ import CATEGORY, ITEM_CATEGORY_SQLI, ITEM_CATEGORY_XSS


class BaseConfig(AppConfig):
    name = 'base'


def get_latest_attack(team, category):
    if category == ITEM_CATEGORY_SQLI:
        latest = SqliLog.objects.filter(from_team=team).latest()
    elif category == ITEM_CATEGORY_XSS:
        latest = XssLog.objects.filter(from_team=team).latest()
    else:
        return None

    if not latest:
        return None

    return {
        "to_team": latest.to_team,
        "is_success": latest.succeed
    }

