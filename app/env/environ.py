from dataclasses import dataclass
from env.credential import SQLI_CREDENTIAL_USER, SQLI_CREDENTIAL_PASSWD
from env.credential import FILTER_CREDENTIAL_USER, FILTER_CREDENTIAL_PASSWD
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


SQLI_DB = MySQLConnectionInfo("", 0000, SQLI_CREDENTIAL_USER, SQLI_CREDENTIAL_PASSWD, "sqli", "utf8")
FILTER_DB = MySQLConnectionInfo("", 0000, FILTER_CREDENTIAL_USER, FILTER_CREDENTIAL_PASSWD, "filter", "utf8")

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
