from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model

from base.models import RegexRule, LenRule, CspRule
from env.environ import CATEGORY, ITEM_CATEGORY_SQLI, ITEM_CATEGORY_XSS
Team = get_user_model()



class Item(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    teams = models.ManyToManyField(Team, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY)
    price = models.IntegerField()

    def already_bought(self, request):
        try:
            self.teams.get(username=request.user.username)
            return True
        except Team.DoesNotExist:
            return False

    def get_filter(self, team: Team):
        if self.category == ITEM_CATEGORY_SQLI:
            return team.sqli_filter
        elif self.category == ITEM_CATEGORY_XSS:
            return team.xss_filter

    def check_balance(self, team: Team):
        return team.balance >= self.price

    def buy(self, team: Team):
        if self.check_balance(team):
            team.balance = F('balance') - self.price
            team.save()
            self.teams.add(team)
            self.action(team)
            return True
        else:
            return False
    
    def cast(self):
        check_item_type = [
            RegexItem.objects.filter(id=self.id), 
            LenItem.objects.filter(id=self.id), 
            CspItem.objects.filter(id=self.id)
        ]
        for t in check_item_type:
            if t.count() == 1:
                return t[0]
        return self

    def action(self, team):
        self.cast().action(team)
        return
    
    def __str__(self):
        return '%s' % self.title



class RegexItem(Item):
    regex_rule = models.ManyToManyField('base.RegexRule')

    def action(self, team: Team):
        f = self.get_filter(team)
        rules = self.regex_rule.all()

        for rule in rules:
            f.regex_rule_list.add(rule)
            f.save()

    class Meta:
        verbose_name = "차단 규칙 아이템"
        verbose_name_plural = "차단 규칙 아이템들"


class LenItem(Item):
    len_rule = models.OneToOneField(LenRule, on_delete=models.CASCADE)

    def action(self, team: Team):
        f = self.get_filter(team)
        current_len = f.max_len
        f.max_len = max(0, current_len - self.len_rule.value)
        f.save()

    class Meta:
        verbose_name = "길이 제한 아이템"
        verbose_name_plural = "길이 제한 아이템들"


class CspItem(Item):
    csp_rule = models.ManyToManyField('base.CspRule')

    def action(self, team: Team):
        f = self.get_filter(team)
        rules = self.csp_rule.all()
        for rule in rules:
            f.csp_rule_list.add(rule)
            f.save()

    class Meta:
        verbose_name = "CSP 아이템"
        verbose_name_plural = "CSP 아이템들"
