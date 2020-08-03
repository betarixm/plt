from django.db import models
from django.contrib.auth.models import AbstractUser


class Team(AbstractUser):
    id = models.CharField(max_length=20)

    class Meta:
        verbose_name = '팀'
        verbose_name_plural = '팀들'

    def __str__(self):
        return self.id
