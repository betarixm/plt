from django.db import models
from django.contrib.auth import get_user_model

from core.models import Rule

Team = get_user_model()


class Item(models.Model):
    title = models.CharField()
    description = models.TextField()
    teams = models.ManyToManyField(Team)

    class Meta:
        verbose_name = '아이템'
        verbose_name_plural = '아이템들'

    def __str__(self):
        return self.title


class RuleItem(Item):

    class Meta:
        verbose_name = "차단 규칙 아이템"
        verbose_name_plural = "차단 규칙 아이템들"


class LengthItem(Item):
    max_len = models.BigIntegerField()

    class Meta:
        verbose_name = "길이 제한 아이템"
        verbose_name_plural = "길이 제한 아이템들"