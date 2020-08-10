from django.apps import AppConfig
from env.sqli.team_db import generate_db
from env.environ import SQLI_DB
from django.contrib.auth import get_user_model
import pymysql

Team = get_user_model()


def create_team(form_username, form_password, form_email):
    team = Team.objects.create_user(
        username=form_username,
        password=form_password,
        email=form_email
    )

    init_sqli_db(team)

    return team


def init_sqli_db(team: Team):
    conn = pymysql.connect(host=SQLI_DB.HOST, port=SQLI_DB.PORT, user=SQLI_DB.USER, password=SQLI_DB.PASSWD, charset=SQLI_DB.CHARSET)
    generate_db(conn, team.username)


class CoreConfig(AppConfig):
    name = 'core'
