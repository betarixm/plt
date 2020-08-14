from django.db import models
from django.contrib.auth import get_user_model
from env.environ import CATEGORY_CHOICES

Team = get_user_model()


class Flag(models.Model):
    flag = models.TextField(unique=True)
    score = models.BigIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    teams = models.ManyToManyField(Team, blank=True)

    class Meta:
        verbose_name = "Flag"
        verbose_name_plural = "Flag들"

    def __str__(self):
        return self.flag
