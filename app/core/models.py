from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class Rule(models.Model):
    description = models.TextField()

    class Meta:
        verbose_name = "차단 규칙"
        verbose_name_plural = "차단 규칙들"

    def __str__(self):
        try:
            return self.name
        except:
            return "No name"


class RegexRule(Rule):
    name = models.CharField(max_length=20, default="regexrule")
    regexp = models.TextField()

    class Meta:
        verbose_name = "정규식 차단 규칙"
        verbose_name_plural = "정규식 차단 규칙들"


class LenRule(Rule):
    name = models.CharField(max_length=20, default="lenrule")
    value = models.BigIntegerField()

    class Meta:
        verbose_name = "길이 제한 엄격화 규칙"
        verbose_name_plural = "길이 제한 엄격화 규칙들"


class CspRule(Rule):
    name = models.CharField(max_length=20, default="csprule")
    csp = models.TextField()

    class Meta:
        verbose_name = "CSP"
        verbose_name_plural = "CSP들"


class Filter(models.Model):
    teamname = models.CharField(max_length=20, default="NONAME")
    description = models.TextField()
    regex_rule_list = models.ManyToManyField(RegexRule, blank=True)
    max_len = models.BigIntegerField(default=120)

    def __str__(self):
        try:
            return f"{self.name} of Team {self.teamname}"
        except:
            return f"Some Filter of Team {self.teamname}"

    class Meta:
        verbose_name = "필터"
        verbose_name_plural = "필터들"


class SqliFilter(Filter):
    name = models.CharField(max_length=20, default="SQLi_filter")

    class Meta:
        verbose_name = "SQLi 필터"
        verbose_name_plural = "SQLi 필터들"


class SstiFilter(Filter):
    name = models.CharField(max_length=20, default="SSTI_filter")

    class Meta:
        verbose_name = "SSTI 필터"
        verbose_name_plural = "SSTI 필터들"


class XssFilter(Filter):
    name = models.CharField(max_length=20, default="XSS_filter")
    csp_rule_list = models.ManyToManyField(CspRule, blank=True)

    class Meta:
        verbose_name = "XSS 필터"
        verbose_name_plural = "XSS 필터들"


class TeamManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None):
        if not username:
            raise ValueError('no username')

        filters = (SqliFilter(), SstiFilter(), XssFilter())
        for f in filters:
            f.teamname = username
            f.save()

        team = self.model(username = username)
        team.sqli_filter = filters[0]
        team.ssti_filter = filters[1]
        team.xss_filter = filters[2]
        
        team.email = self.normalize_email(email)
        team.set_password(password)
        team.save(using=self._db)
        return team

    def create_superuser(self, username, password, email=None):
        if not password:
            raise ValueError('no password')

        team = self.create_user(
            username=username,
            password=password
        )
        team.is_admin = True
        team.is_superuser = True
        team.is_staff = True
        team.save(using=self._db)
        return team


class Team(AbstractUser, PermissionsMixin):
    objects = TeamManager()

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=20, unique=True)
    balance = models.BigIntegerField(default=0)
    score = models.BigIntegerField(default=0)

    sqli_filter = models.OneToOneField('core.SqliFilter', related_name="SQLi_Filter", on_delete=models.CASCADE)
    ssti_filter = models.OneToOneField('core.SstiFilter', related_name="SSTI_Filter", on_delete=models.CASCADE)
    xss_filter = models.OneToOneField('core.XssFilter', related_name="XSS_Filter", on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = '팀'
        verbose_name_plural = '팀들'

    def __str__(self):
        return self.username

    def add_score(self, d_score: int):
        self.balance += d_score
        self.score += d_score
