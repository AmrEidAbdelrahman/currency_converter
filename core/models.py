from django.contrib.auth.models import User
from django.db import models

# Create your models here.

CURRENCY_CHOICES = (
    ('usd', 'USD'),
    ('eur', 'EUR'),
    ('egp', 'EGP'),   
)


class CurrencyChangeRequest(models.Model):
    source_currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES)
    target_currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES)
    number_of_requests = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'From {self.source_currency} To {self.target_currency} #{self.number_of_requests}'

