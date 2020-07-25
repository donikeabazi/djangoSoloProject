from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register_validator(self, postData):
		errors = {}
		check = User.objects.filter(email=postData['email'])
		if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
			errors['first_name'] = "Please enter a valid first name and with only letters"
		if len(postData['last_name']) < 2 or not postData['last_name'].isalpha():
			errors['last_name'] = "Please enter a valid last name and with only letters"
		if len(postData['password']) < 8:
			errors['password'] = "Password cannot be less than 8 characters."
		elif postData['password'] != postData['confirm_password']:
			errors['password'] = "Passwords do not match."
		if len(postData['email']) < 1:
			errors['email'] = "Email addres cannot be blank."
		elif not EMAIL_REGEX.match(postData['email']):
			errors['email'] = "Please enter a valid email address."
		elif check:
			errors['email'] = "Email address is already registered."
		return errors

class PostManager(models.Manager):
    def validator(self, postData):
        errors = {}
        
        if(len(postData['title'])) < 4:
            errors['title'] = "Title of the post should contain at least 5 characters."
        if(len(postData['description'])) < 10:
            errors['description'] = "Description of the post should contain at least 10 characters"
        if(len(postData['content'])) < 50:
            errors['content'] = "Content must contain at least 50 characters."
        return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

class Post(models.Model):
    title = models.CharField(max_length=15)
    description = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, related_name="has_posts", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="has_likes")
    collection = models.ForeignKey(User, related_name="has_collected", on_delete=models.CASCADE, null=True)

    objects = PostManager()