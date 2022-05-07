from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class data(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)

    cig = models.CharField(max_length=50,blank=True, null=True)
    cost= models.IntegerField(default=0)
    qty = models.IntegerField(default=0)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return str(self.id)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cigday = models.IntegerField(default=0)
    cigweek = models.IntegerField(default=0)
    cigmonth = models.IntegerField(default=0)
    cigyear = models.IntegerField(default=0)
    expday = models.IntegerField(default=0)
    expweek = models.IntegerField(default=0)
    expmonth = models.IntegerField(default=0)
    expyear = models.IntegerField(default=0)

    def __str__(self):
        return "Profile of {}".format(self.user.username)

class contactus(models.Model):

    user = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50,null=True,blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    message = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.user)