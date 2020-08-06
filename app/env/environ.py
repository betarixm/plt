from dataclasses import dataclass
from env.credential import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS
from django.contrib.auth import get_user_model

Team = get_user_model()

@dataclass
class MySQLConnectionInfo:
    "Connection information to MySQL"
    HOST: str
    PORT: int
    USER: str
    PASSWD: str
    DB: str
    CHARSET: str


SQLI_DB = MySQLConnectionInfo(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, "sqli", "utf8")
FILTER_DB = MySQLConnectionInfo(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, "filter", "utf8")

ITEM_CATEGORY_SQLI = 'sqli'
ITEM_CATEGORY_SSTI = 'ssti'
ITEM_CATEGORY_XSS = 'xss'

CATEGORY_CHOICES = (
    (ITEM_CATEGORY_SQLI, 'SQLi'),
    (ITEM_CATEGORY_XSS, 'XSS'),
    (ITEM_CATEGORY_SSTI, 'SSTI')
)


def team_list():
    return Team.objects.values_list('username', flat=True)


def team_choices():
    beta = team_list()
    beka = []
    for i in beta:
        beka.append((i, i))

    return tuple(beka)
