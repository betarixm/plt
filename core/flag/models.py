from django.db import models
from django.contrib.auth import get_user_model
from env.environ import CATEGORY

Team = get_user_model()


class Flag(models.Model):
    flag = models.TextField(unique=True)
    score = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY)
    teams = models.ManyToManyField(Team, blank=True)

    class Meta:
        verbose_name = "Flag"
        verbose_name_plural = "Flag들"

    def __str__(self):
        return '%s' % self.flag