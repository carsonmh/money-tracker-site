from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MoneyLog(models.Model):
    """A class for logging money that the user has made"""
    money_made = models.FloatField(help_text="")
    date_added = models.DateTimeField(auto_now_add=True)
    money_info = models.TextField(default="", blank=True)
    anonymous = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """return a string rep of the model"""
        return str(self.money_made)