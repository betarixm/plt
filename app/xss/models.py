from django.db import models

from core.models import CspRule

# Create your models here.

class XssLog(models.Model):
    from_team = models.CharField(max_length=20)
    to_team = models.CharField(max_length=20)
    csp = models.ManyToManyField(CspRule, blank=True)
    query = models.CharField(max_length=1000)
    hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False)
    succeed = models.BooleanField(default=False)

    def __str__(self):
        return f"XSS query from {self.from_team} to {self.to_team} /{self.hash}"

    class Meta:
        verbose_name = "XSS 로그"
        verbose_name_plural = "XSS 로그들"
        get_latest_by = "created_at"
