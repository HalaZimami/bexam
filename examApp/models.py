from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        emails = User.objects.filter(email=postData['email'])
        if len(emails)>0:
            errors['emailExist']="This Email is already in use!"
            return errors
        if len(postData['fname'])<2:
            errors['fname']='First Name must be at least 2 characters'
        if len(postData['lname'])<2:
            errors['lname']='Last Name must be at least 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password'])<8:
            errors['password']='Password must be at least 8 characters'
        if not postData['password'] == postData['Cpassword']:
            errors['Cpassword']='Password and Confirm Password must be the same!'
        return errors

class WishManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['title'])<3:
            errors['title']='A wish must consist of at least 3 characters'
        if len(postData['desc'])<3:
            errors['desc']='A description must be provided'
        return errors

class User(models.Model):
    fname = models.CharField(max_length=35)
    lname = models.CharField(max_length=35)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    objects = UserManager()

class Wish(models.Model):
    created_by = models.ForeignKey(User, related_name='wishes', on_delete=models.CASCADE)
    title = models.CharField(max_length=24)
    desc = models.TextField(max_length=281)
    liked_by = models.ManyToManyField(User, related_name="likes")
    users_list = models.ManyToManyField(User, related_name="lists")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = WishManager()