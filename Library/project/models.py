from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    enrollment=models.CharField(max_length=40)
    branch=models.CharField(max_length=40)
    def __str__(self):
        return self.user.first_name+'['+str(self.enrollment)+']'

    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id

class Book(models.Model):
    catchoice=[
        {'','--SELECT--'},
        {'education', 'EDUCATION'},
        {'entertainment', 'ENTERTAINMENT'},
        {'comics', 'COMICS'},
        {'biography', 'BIOGRAPHY'},
        {'history', 'HISTORY'},
    ]
    name=models.CharField(max_length=100)
    isbn=models.PositiveIntegerField()
    author=models.CharField(max_length=100)
    category=models.CharField(max_length=100,choices=catchoice,default='--SELECT--')
    def __str__(self):
        return str(self.name)+" ["+str(self.isbn)+"]"


def get_expiry():
    return datetime.today()+timedelta(days=15)
class IssuedBook(models.Model):
    enrollment=models.CharField(max_length=30)
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    def __str__(self):
        return self.enrollment