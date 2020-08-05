from django.db import models
from django.contrib.auth import get_user_model

from core.models import RegexRule, LenRule, CspRule
from env.environ import ITEM_CATEGORY_SQLI, ITEM_CATEGORY_SSTI, ITEM_CATEGORY_XSS, CATEGORY_CHOICES
Team = get_user_model()


class Item(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    teams = models.ManyToManyField(Team)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.BigIntegerField()

    def get_filter(self, team: Team):
        if self.category is ITEM_CATEGORY_XSS:
            return team.xss_filter
        elif self.category is ITEM_CATEGORY_SSTI:
            return team.ssti_filter
        elif self.category is ITEM_CATEGORY_SQLI:
            return team.sqli_filter

    def check_balance(self, team: Team):
        return team.balance >= self.price

    def buy(self, team: Team):
        if self.check_balance(team):
            self.action(team)
            return True
        else:
            return False

    def action(self, team):
        return

    class Meta:
        verbose_name = '아이템'
        verbose_name_plural = '아이템들'

    def __str__(self):
        return self.name


class RegexItem(Item):
    regex_rule = models.ManyToManyField('core.RegexRule')

    def action(self, team: Team):
        self.get_filter(team).regex_rule_list.add(self.regex_rule)

    class Meta:
        verbose_name = "차단 규칙 아이템"
        verbose_name_plural = "차단 규칙 아이템들"


class LenItem(Item):
    len_rule = models.OneToOneField('core.LenRule', on_delete=models.CASCADE)

    def action(self, team: Team):
        self.get_filter(team).max_len -= self.len_rule.value

    class Meta:
        verbose_name = "길이 제한 아이템"
        verbose_name_plural = "길이 제한 아이템들"


class CspItem(Item):
    csp_rule = models.ManyToManyField('core.CspRule')

    def action(self, team: Team):
        self.get_filter(team).csp_rule_list.add(self.csp_rule)

    class Meta:
        verbose_name = "CSP 아이템"
        verbose_name_plural = "CSP 아이템들"