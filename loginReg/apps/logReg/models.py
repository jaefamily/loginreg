from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def add_user(self, postData):
        errors = []
        if not len(postData['first_name']):
            errors.append('First name is required')
        if len(postData['last_name']) < 2:
            errors.append('Last name must be at least 2 characters long!')
        if not len(postData['email']):
            errors.append('Email is required!')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Please enter a valid email!')
        check_email = self.filter(email = postData['email'])
        if check_email:
            errors.append('Sorry email already exist!')
        if len(postData['password']) < 8:
            errors.append('Password must be at least 8 characters!')
        if not postData['password'] == postData['confirm_password']:
            errors.append('Passwords must match!')

        modelsResponse = {}

        if errors:
            # failed validations
            modelsResponse ['isRegistered'] = False
            modelsResponse['errors'] = errors
        else:
            # passed validations, create a new user
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = self.create(first_name = postData['first_name'] , last_name = postData['last_name'], email=postData['email'], password = hashed_password)
            modelsResponse ['isRegistered']= True
            modelsResponse['user'] = user

        return modelsResponse

    def login_user(self, postData):
        user = self.filter(email = postData['email'])
        errors = []
        modelsResponse = {}
        print user
        if not user:
            #invalid email
            errors.append('Invalid email!')

        else:
            #found a user match, check the password to see if they match
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                #login the user
                modelsResponse['isLoggedIn'] = True
                modelsResponse['user'] = user[0]
            else:
                # invalid email password combination
                errors.append('Invalid email/password combination!')

        if errors:
            modelsResponse['isLoggedIn'] = False
            modelsResponse['errors'] = errors

        return modelsResponse

class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length =100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()