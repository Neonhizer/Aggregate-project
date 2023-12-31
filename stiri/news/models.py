from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(unique=True)
    short_description = models.CharField(max_length=500, default="N/A")

    def __str__(self):
        return self.title
