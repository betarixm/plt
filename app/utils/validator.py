from django.core.exceptions import ValidationError
from django.utils.translation import gettext
from django.contrib.auth.mixins import UserPassesTestMixin
from core.models import Team


class LoginCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_annoymous

    login_url = '/login'


def unique_team_id(target):
    if Team.objects.filter(username__iexact=target).count() > 0:
        raise ValidationError(
            gettext('Team ID already exist')
        )

