from django.db import models


# Create your models here.
class Item(models.Model):
    title = models.CharField()
    description = models.TextField()
    api_url = models.CharField()
    users = models.CharField()

    data = models.TextField()

    def __str__(self):
        return self.title
