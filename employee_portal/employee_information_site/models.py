from django.db import models


# Create your models here.
class Candidate(models.Model):
    entryDate = models.DateField()
    fullName = models.CharField(max_length=50)
    email = models.EmailField()
    otherContacts = models.CharField(max_length=100)
    position = models.CharField(max_length=30)

    def __str__(self):
        return self.fullName
