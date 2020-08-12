from django.db import models

# Create your models here.

class XssTrial(models.Model):
    from_team = models.CharField(max_length=20)
    to_team = models.CharField(max_length=20)
    csp = models.CharField(max_length=10000)
    query = models.CharField(max_length=10000)
    hash = models.CharField(max_length=32)
    checked = models.BooleanField(default=False)
    succeed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"query from {from_team} to {to_team}"

    class Meta:
        verbose_name = "XSS 공격 시도"
        verbose_name_plural = "XSS 공격 시도들"
