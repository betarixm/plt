from django.db import models
from django.contrib.auth import get_user_model

from core.models import RegexRule
from env.environ import ITEM_CATEGORY_SQLI, ITEM_CATEGORY_SSTI, ITEM_CATEGORY_XSS
Team = get_user_model()


class Item(models.Model):
    CATEGORY_CHOICES = (
        (ITEM_CATEGORY_SQLI, 'SQLi'),
        (ITEM_CATEGORY_XSS, 'XSS'),
        (ITEM_CATEGORY_SSTI, 'SSTI')
    )

    title = models.CharField()
    description = models.TextField()
    teams = models.ManyToManyField(Team)
    category = models.CharField(choices=CATEGORY_CHOICES)
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
        return self.title


class RegexItem(Item):
    regex_rule = models.ManyToManyField('core.RegexRule', blank=True)

    def action(self, team: Team):
        self.get_filter(team).block_rule_list.add(self.regex_rule)

    class Meta:
        verbose_name = "차단 규칙 아이템"
        verbose_name_plural = "차단 규칙 아이템들"


class MaxLenItem(Item):
    max_len_rule = models.ManyToManyField('core.MaxLenRule', blank=True, unique=True)

    def action(self, team: Team):
        self.get_filter(team).max_len_rule = self.max_len_rule.max_len

    class Meta:
        verbose_name = "길이 제한 아이템"
        verbose_name_plural = "길이 제한 아이템들"