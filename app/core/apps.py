from django.apps import AppConfig
from env.sqli.team_db import generate_db
from django.contrib.auth import get_user_model
from utils.mysql import sqli_db
from xss.models import XssLog
from ssti.models import SstiLog
from sqli.models import SqliLog
from env.environ import ITEM_CATEGORY_XSS, ITEM_CATEGORY_SSTI, ITEM_CATEGORY_SQLI
Team = get_user_model()


def create_team(form_username, form_password, form_email):
    team = Team.objects.create_user(
        username=form_username,
        password=form_password,
        email=form_email
    )

    generate_db(sqli_db(), team.username)

    return team


def get_latest_attack(team, category):
    if category == ITEM_CATEGORY_SQLI:
        latest = SqliLog.objects.filter(from_team=team).order_by('-id')
    elif category == ITEM_CATEGORY_SSTI:
        latest = SstiLog.objects.filter(from_team=team).order_by('-id')
    elif category == ITEM_CATEGORY_XSS:
        latest = XssLog.objects.filter(from_team=team).order_by('-id')
    else:
        return None

    if latest.count() == 0:
        return None

    latest = latest[0]
    return {
        "category": category,
        "to_team": latest.to_team,
        "is_success": latest.succeed
    }


class CoreConfig(AppConfig):
    name = 'core'
