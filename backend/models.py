from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(null=True)
    birthday = models.CharField(max_length=15, null=True)
    sex = models.CharField(max_length=1, null=True, default='1')
    country = models.CharField(max_length=30, null=True)
    first_name = models.CharField(max_length=10, null=True)
    last_name = models.CharField(max_length=10, null=True)
    wechat = models.CharField(max_length=50, null=True)


class Picture(models.Model):
    pid = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to="pics")
    imgname = models.CharField(max_length=100, null=True)
    size = models.IntegerField()
    uploader = models.ForeignKey('User', on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    num_like = models.IntegerField()
    num_star = models.IntegerField()
    num_view = models.IntegerField()


class Favorite(models.Model):
    pid = models.ForeignKey('Picture', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            # complex primary key: promise combination is only one
            models.UniqueConstraint(fields=['pid', 'user'], name='favor_pic'),
        ]


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tname = models.CharField(max_length=20)

    class Meta:
        constraints = [
            # complex primary key: promise combination is only one
            models.UniqueConstraint(fields=['tag_id', 'tname'], name='tag_id'),
        ]


class PictoTag(models.Model):
    pid = models.ForeignKey('Picture', on_delete=models.CASCADE)
    tag_id = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            # complex primary key: promise combination is only one
            models.UniqueConstraint(fields=['pid', 'tag_id'], name='tag_pic'),
        ]