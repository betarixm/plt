from django.apps import AppConfig
from env.sqli.team_db import generate_db
from django.contrib.auth import get_user_model
from utils.mysql import sqli_db

Team = get_user_model()


def create_team(form_username, form_password, form_email):
    team = Team.objects.create_user(
        username=form_username,
        password=form_password,
        email=form_email
    )

    generate_db(sqli_db(), team.username)

    return team


class CoreConfig(AppConfig):
    name = 'core'
