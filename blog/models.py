from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse
from django.conf import settings
from PIL import Image
from django.db.models.deletion import CASCADE
from PIL import Image
from django.core.validators import MinValueValidator, RegexValidator



class Profile(models.Model):
    name = models.CharField(max_length = 100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default = 18, validators=[MinValueValidator(18)])
    address = models.TextField(null = True, blank = True)
    status = models.CharField(max_length=20,
    default="single", choices=(("single", "single"), ("married", "married"), ("widow", "widow"), ("separated", "separated"), ("commited", "commited")))
    gender = models.CharField(max_length=20, default="female", choices=(("male", "male"), ("female", "female")))
    phone_no = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=15, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.image.path)


        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    image = models.ImageField(blank=True, null = True, upload_to='images/')
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=Profile, on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ManyToManyField('Category')


    def __str__(self):
        return self.title 

    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.image.path)


        if img.height > 300 or img.width > 500:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=CASCADE)
    msg = models.TextField()
    commented_by = models.ForeignKey(to=Profile, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    flag = models.CharField(max_length=20, null=True, blank=True, choices=(("racist", "racist"), ("abusing", "abusing")))
    def __str__(self):
        return self.msg


class Like(models.Model):
    post = models.ForeignKey(to=Post, on_delete=CASCADE)
    liked_by = models.ForeignKey(to=Profile, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.liked_by

class Unlike(models.Model):
    post = models.ForeignKey(to=Post, on_delete=CASCADE)
    Unliked_by = models.ForeignKey(to=Profile, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Unliked_by

class FollowUser(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete=CASCADE, related_name="profile")
    followed_by = models.ForeignKey(to=Profile, on_delete=CASCADE, related_name="followed_by")
    def __str__(self):
        return f'{self.profile} is followed by {self.followed_by}'