from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class DataInput(models.Model):
    start_day = models.DateTimeField('start_day')
    finish_day = models.DateTimeField('finish_day')
    campaign_id = models.CharField('campaign_id', max_length=3)
    buyer_id    = models.CharField('buyer_id', max_length=10)
    def __str__(self):
        return self.campaign_id