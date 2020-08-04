from django.core.exceptions import ValidationError
from django.utils.translation import gettext
from core.models import Team


def unique_team_id(target):
    if Team.objects.filter(username__iexact=target).count() > 0:
        raise ValidationError(
            gettext('Team ID already exist')
        )

