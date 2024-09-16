from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=212)
    content = models.TextField(max_length=500)
    author = models.CharField(max_length=212)

    def __str__(self):
        return self.title