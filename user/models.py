# user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserModel(AbstractUser):
    class Meta: # 데이터베이스에 정보를 넣어 주는 역할(장고 기초 2-3) 
        db_table = "my_user"

    bio = models.CharField(max_length=256, default='')
