
from django.db import models

class staff_info(models.Model):
    user_name = models.CharField(max_length=200,default="")
    staff_id = models.CharField(max_length=20,default="",unique=True)
    staff_fname = models.CharField(max_length = 30,default="")
    staff_lname = models.CharField(max_length = 30,default="")
    staff_email = models.CharField(max_length = 100,default="")
    staff_mess = models.CharField(max_length= 10,default="")

class MessUpload(models.Model):
    file = models.FileField(upload_to='file_uploads/')
