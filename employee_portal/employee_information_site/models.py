from django.db import models


# Create your models here.
class Candidate(models.Model):
    entryDate = models.DateField(verbose_name='Entry Date')
    fullName = models.CharField(max_length=50, verbose_name='Name')
    email = models.EmailField()
    otherContacts = models.CharField(max_length=100)
    position = models.CharField(max_length=30, verbose_name='Position')

    def __str__(self):
        return self.fullName
