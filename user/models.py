from django.db import models
import datetime


class User(models.Model):
    username = models.CharField(max_length=100,default='',verbose_name="Username",unique=True)
    email=models.EmailField(max_length=100,verbose_name="EMail Id")
    password = models.TextField(max_length='100',verbose_name='Password')
    firstname = models.CharField(max_length=100,default='',verbose_name='FirstName')
    lastname = models.CharField(max_length=100,default='',verbose_name='LastName')
    authToken = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateTimeField(default=datetime.datetime.now())
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for User
        """
        verbose_name_plural = "User"

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        return super(User, self).save(*args, **kwargs)

