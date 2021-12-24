from django.db import models
from django.contrib.auth import get_user_model  # If used custom user model

UserModel = get_user_model()


class Currency(models.Model):
    '''
    "r030": 36, "txt": "Австралійський долар", "rate": 19.7237, "cc": "AUD", "exchangedate": "24.12.2021"
    '''
    r030 = models.IntegerField()
    txt = models.CharField('Валюта', max_length=40, blank=True, null=True)
    rate = models.DecimalField('rate', max_digits=10, decimal_places=4, blank=True, null=True)
    cc = models.CharField('cc', max_length=5, blank=True, null=True)
    exchangedate = models.DateTimeField("exchangedate", blank=True, null=True)

    class Meta:
        unique_together = ('exchangedate', 'cc',)

