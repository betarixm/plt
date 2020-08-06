from django.core.exceptions import ValidationError
from django.utils.translation import gettext
from django.contrib.auth.mixins import UserPassesTestMixin
from core.models import Team
import re


class LoginCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_annoymous

    login_url = '/login'


def unique_team_id(target):
    if Team.objects.filter(username__iexact=target).count() > 0:
        raise ValidationError(
            gettext('Team ID already exist')
        )


def flag_format(target):
    p = re.compile(r"^(PLUS)\{.*\}")
    if not p.match(target):
        print("not valid format!")
        raise ValidationError(
            gettext('Flag Format not Valid!')
        )

