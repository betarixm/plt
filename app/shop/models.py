from django.db import models
from django.contrib.auth import get_user_model

Team = get_user_model()


class Item(models.Model):
    title = models.CharField()
    description = models.TextField()
    teams = models.ManyToManyField(Team)
    query = models.CharField()

    class Meta:
        verbose_name = '아이템'
        verbose_name_plural = '아이템들'

    def __str__(self):
        return self.title


class SqliItem(Item):
    def add_sqli_filter(self, team: Team):
        # Todo: add MySql Link
        self.teams.add(team)

    class Meta:
        verbose_name = 'SQLi 아이템'
        verbose_name_plural = 'SQLi 아이템들'


class SSTIItem(Item):
    def add_sqli_filter(self, team: Team):
        self.teams.add(team)

    class Meta:
        verbose_name = 'SSTI 아이템'
        verbose_name_plural = 'SSTI 아이템'


class XSSItem(Item):
    def add_xss_filter(self, team: Team):
        self.teams.add(team)

    class Meta:
        verbose_name = 'XSS 아이템'
        verbose_name_plural = 'SSTI 아이템'
