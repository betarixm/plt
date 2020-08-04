from django.db import models
from django.contrib.auth.models import AbstractUser


class Team(AbstractUser):
    id = models.CharField(max_length=20)

    sqli_filter = models.OneToOneField('core.SqliFilter', on_delete=models.CASCADE)
    ssti_filter = models.OneToOneField('core.SstiFilter', on_delete=models.CASCADE)
    xss_filter = models.OneToOneField('core.XssFilter', on_delete=models.CASCADE)

    balance = models.BigIntegerField()

    class Meta:
        verbose_name = '팀'
        verbose_name_plural = '팀들'

    def __str__(self):
        return self.id


class Rule(models.Model):
    name = models.CharField()
    description = models.TextField()

    class Meta:
        verbose_name = "차단 규칙"
        verbose_name_plural = "차단 규칙들"

    def __str__(self):
        return self.name


class RegexRule(Rule):
    regexp = models.CharField()

    class Meta:
        verbose_name = "정규식 차단 규칙"
        verbose_name_plural = "정규식 차단 규칙들"


class MaxLenRule(Rule):
    max_len = models.BigIntegerField()

    class Meta:
        verbose_name = "길이 제한 규칙"
        verbose_name_plural = "길이 제한 규칙들"


class Filter(models.Model):
    name = models.CharField()
    description = models.TextField()
    block_rule_list = models.ManyToManyField(RegexRule, blank=True)
    max_len = models.BigIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "필터"
        verbose_name_plural = "필터들"


class SqliFilter(Filter):
    Filter.name = "SQLi Filter"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "SQLi 필터"
        verbose_name_plural = "SQLi 필터들"


class SstiFilter(Filter):
    Filter.name = "SSTI Filter"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "SQLi 필터"
        verbose_name_plural = "SQLi 필터들"


class XssFilter(Filter):
    Filter.name = "XSS Filter"
    csp_rule_list = models.ManyToManyField(RegexRule, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "XSS 필터"
        verbose_name_plural = "XSS 필터들"
