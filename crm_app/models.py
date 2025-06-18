from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=20, blank=False)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
