from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    sqli_filter = models.OneToOneField('core.SqliFilter', related_name="SQLi_Filter", on_delete=models.CASCADE)
    ssti_filter = models.OneToOneField('core.SstiFilter', related_name="SSTI_Filter", on_delete=models.CASCADE)
    xss_filter = models.OneToOneField('core.XssFilter', related_name="XSS_Filter", on_delete=models.CASCADE)

    balance = models.BigIntegerField()
    score = models.BigIntegerField()

    class Meta:
        verbose_name = '팀'
        verbose_name_plural = '팀들'

    def __str__(self):
        return self.name

    def add_score(self, d_score: int):
        self.score += d_score


class Rule(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        verbose_name = "차단 규칙"
        verbose_name_plural = "차단 규칙들"

    def __str__(self):
        return self.name


class RegexRule(Rule):
    Rule.name = "Reg Exp Rule"
    regexp = models.TextField()

    class Meta:
        verbose_name = "정규식 차단 규칙"
        verbose_name_plural = "정규식 차단 규칙들"


class LenRule(Rule):
    Rule.name = "Max Length Rule"
    value = models.BigIntegerField()

    class Meta:
        verbose_name = "길이 제한 엄격화 규칙"
        verbose_name_plural = "길이 제한 엄격화 규칙들"


class CspRule(Rule):
    Rule.name = "CSP Rule"
    csp = models.TextField()

    class Meta:
        verbose_name = "CSP"
        verbose_name_plural = "CSP들"


class Filter(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    regex_rule_list = models.ManyToManyField(RegexRule, blank=True)
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
        verbose_name = "SSTI 필터"
        verbose_name_plural = "SSTI 필터들"


class XssFilter(Filter):
    Filter.name = "XSS Filter"
    csp_rule_list = models.ManyToManyField(CspRule, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "XSS 필터"
        verbose_name_plural = "XSS 필터들"
