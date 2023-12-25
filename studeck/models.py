from django.db import models
from django.contrib.auth.models import User  


class student_info(models.Model):
    user_name = models.ForeignKey(User, on_delete = models.CASCADE)
    student_bhawan = models.CharField(max_length=20)
    student_id = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

    
class Feedbacks(models.Model):
    user_name = models.ForeignKey(student_info,on_delete = models.CASCADE)
    feed_back = models.CharField(max_length=1000)
    picture = models.ImageField(upload_to="feedback_pics/",blank=True) 

class total_daily(models.Model):
    date = models.DateField()
    breakfast = models.IntegerField(default=0)
    lunch = models.IntegerField(default=0)
    dinner = models.IntegerField(default=0)

class user_total(models.Model):
    user_name = models.OneToOneField(student_info,on_delete=models.CASCADE)
    breakfast = models.IntegerField(default=0)
    lunch = models.IntegerField(default=0)
    dinner = models.IntegerField(default=0)

class food_items(models.Model):
    food_item = models.CharField(max_length=100)
    rating = models.FloatField(default=0)
    def __str__(self):
        return self.food_item

class rating_model(models.Model):
    food_item = models.ForeignKey(food_items, on_delete = models.CASCADE)
    user_name = models.ForeignKey(student_info, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class checkpresence(models.Model):
    user_name = models.OneToOneField(student_info,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    breakfast = models.IntegerField(default=0)
    lunch = models.IntegerField(default=0)
    dinner = models.IntegerField(default=0)

