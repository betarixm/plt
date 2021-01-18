from django.db import models
from django.contrib.auth.models import AbstractUser


class Team(AbstractUser):
    balance = models.BigIntegerField(default=0)
    score = models.BigIntegerField(default=0)

    actions = ['create_new_database', ]

    def apply_score(self, _score: int):
        self.balance += _score
        self.score += _score
        self.save()

    class Meta:
        verbose_name = '팀'
        verbose_name_plural = '팀들'


from sqli.apps import generate_db

def create_new_database(Team, request, queryset):
    for team in queryset:
        generate_db(team.username)


class Rule(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        abstract = True


class RegexRule(Rule):
    regexp = models.CharField(max_length=255)
    class Meta:
        verbose_name = "정규식 차단 규칙"
        verbose_name_plural = "정규식 차단 규칙들"

class LenRule(Rule):
    value = models.PositiveSmallIntegerField()
    class Meta:
        verbose_name = "길이 제한 엄격화 규칙"
        verbose_name_plural = "길이 제한 엄격화 규칙들"

class CspRule(Rule):
    csp = models.CharField(max_length=255)
    class Meta:
        verbose_name = "CSP"
        verbose_name_plural = "CSP들"



class Filter(models.Model):
    owner = models.ForeignKey(Team, on_delete=models.PROTECT)
    regex_rule_list = models.ManyToManyField(RegexRule, blank=True)
    max_len = models.PositiveSmallIntegerField(default=120)

    class Meta:
        abstract = True


class SqliFilter(Filter):
    class Meta:
        verbose_name = "SQLi 필터"
        verbose_name_plural = "SQLi 필터들"

class XssFilter(Filter):
    csp_rule_list = models.ManyToManyField(CspRule, blank=True)
    class Meta:
        verbose_name = "XSS 필터"
        verbose_name_plural = "XSS 필터들"