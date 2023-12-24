from django.contrib import admin
from .models import Feedbacks,user_total,total_daily,rating_model,food_items,student_info,checkpresence

class Feedback_admin(admin.ModelAdmin):
    fieldsets = [
        (None,{"fields":["user_name"]}),
        ("Feedback",{"fields":["feed_back"]}),
        ("picture",{"fields":["picture"]})
    ]
    list_display = ["user_name","feed_back","picture"]

class fooditems(admin.ModelAdmin):
    fieldsets = [
        (None,{'fields':["food_item"]}),
        ("rating",{'fields':["rating"]}),
    ]
    list_display = ["food_item","rating"]

class usertotal(admin.StackedInline):
    model = user_total

class presence(admin.StackedInline):
    model = checkpresence

class total_daily_admin(admin.ModelAdmin):
    fieldsets = [
        ("date",{"fields":["date"]}),
        ("breakfast",{"fields":["breakfast"]}),
        ("lunch",{"fields":["lunch"]}),
        ("dinner",{"fields":["dinner"]}),    
    ]
    list_display = ["date","breakfast","lunch","dinner"]

class ratin_admin(admin.ModelAdmin):
    fieldsets = [
        ("username",{"fields":["user_name"]}),
        ("food item",{"fields":["food_item"]}),
        ("Rating",{'fields':["rating"]}),

    ]
    list_display = ["user_name","food_item","rating"]

class student_admin(admin.ModelAdmin):
    fieldsets =[
        ("username",{"fields":["user_name"]}),
        ("bhawan",{"fields":["student_bhawan"]}),
        ("id",{"fields":["student_id"]}),
        ("email",{"fields":["email"]})
    ]
    inlines = [usertotal,presence]
    list_display = ["user_name","student_bhawan","student_id","email"]

admin.site.register(Feedbacks,Feedback_admin)
admin.site.register(total_daily,total_daily_admin)
admin.site.register(rating_model,ratin_admin)
admin.site.register(food_items,fooditems)
admin.site.register(student_info,student_admin)





