from django.contrib import admin

from .models import staff_info,MessUpload

class staff_admin(admin.ModelAdmin):
    fieldsets = [
        (None,{"fields":["staff_id"]}),
        ("username",{"fields":["user_name"]}),
        ("First name",{"fields":["staff_fname"]}),
        ("Last name",{"fields":["staff_lname"]}),
        ("Staff Mess",{"fields": ["staff_mess"]}),
        ("Staff email",{"fields":["staff_email"]}),
        
    ]
    list_display = ["user_name","staff_id","staff_fname","staff_lname","staff_email","staff_mess"]

class UploadedFiles(admin.ModelAdmin):
    fieldsets = [
        (None,{"fields":["file"]}),
    ]
    list_display = ["file"]


    
admin.site.register(staff_info,staff_admin)
admin.site.register(MessUpload,UploadedFiles)