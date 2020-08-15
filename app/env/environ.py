from dataclasses import dataclass
from django.contrib.auth import get_user_model

Team = get_user_model()

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
