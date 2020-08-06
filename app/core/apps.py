from django.apps import AppConfig
from env.sqli.team_db import generate_db
from env.environ import SQLI_DB
from django.contrib.auth import get_user_model
import pymysql

Team = get_user_model()


def init_sqli_db(team: Team):
    conn = pymysql.connect(host=SQLI_DB.HOST, port=SQLI_DB.PORT, user=SQLI_DB.USER, password=SQLI_DB.PASSWD, charset=SQLI_DB.CHARSET)
    generate_db(conn, team.username)


class CoreConfig(AppConfig):
    name = 'core'
