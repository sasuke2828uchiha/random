from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from datetime import datetime,time,timedelta
from .models import Feedbacks,user_total,total_daily,rating_model,student_info,checkpresence,food_items
from .forms import Feedback_form
import pandas as pd
import json
from staffdeck.models import staff_info

def stulogin(request):
    staff_members_list = []
    staff_object = staff_info.objects.all()
    for i in staff_object:
        staff_members_list.append(i.user_name)
    return render(request,'auth/stulogin.html',{"staff_names":staff_members_list})

def log_out(request):
    logout(request)
    return redirect("home")

def stuhome(request):
    user = request.user
    try:
        info = student_info.objects.get(user_name = request.user.username)
    except:
        info = student_info(user_name = request.user.username)
        info.save()
    try:
        google_account = user.socialaccount_set.get(provider='google')
        profile_picture_url = google_account.extra_data['picture']
    except user.socialaccount_set.model.DoesNotExist:
        profile_picture_url = None
    
    try:
        fobj = open('menu.json','r')
        global menu_data
        menu_data = json.load(fobj)
        next_data = {}
        if( time(9,0) < datetime.now().time() < time(14,0)):
          for date,data in menu_data.items():
            if(datetime.now().date().strftime("%Y-%m-%d") == date):
                meal = list(data.items())[1]
                next_data = {meal[0]:meal[1]}
        elif( time(14,0) < datetime.now().time() < time(21,0) ):
          for date,data in menu_data.items():
            if(datetime.now().date().strftime("%Y-%m-%d") == date):
                meal = list(data.items())[2]
                next_data = {meal[0]:meal[1]}
        elif(time(21,0) < datetime.now().time() < time(0,0)):
          for date,data in menu_data.items():
            next_date = datetime.now().date() + timedelta(days=1)
            if(next_date.strftime("%Y-%m-%d") == date):
                meal = list(data.items())[0]
                next_data = {meal[0]:meal[1]}
        else:
            for date,data in menu_data.items():
                if(datetime.now().date().strftime("%Y-%m-%d") == date):
                    meal = list(data.items())[0]
                    next_data = {meal[0]:meal[1]}
    except:
        menu_data = {}
        next_data = {}
         
    try:
        studentdata = student_info.objects.filter(user_name = request.user.username).first()
        stubhawan = studentdata.student_bhawan
        stuid = studentdata.student_id
    except:
        stubhawan = ""
        stuid = ""
    
    context = {"bhawan":stubhawan,"ID":stuid,'user': user, 'profile_picture_url': profile_picture_url,'menu_data':menu_data,"next_menu":next_data}
    return render(request, 'home/stuhome.html',context )
    
def inc_attendance(request):
    date_data = total_daily.objects.filter(date = datetime.now().date()).first()
    if not date_data:  
        new_date = total_daily(date = datetime.now().date())
        new_date.save()
        date_data = total_daily.objects.filter(date = datetime.now().date()).first()

   
    student = student_info.objects.get(user_name = request.user.username)
    if not student:
        new_stu = student_info(user_name = request.user.username)
        new_stu.save()
        student = student_info.objects.get(user_name = request.user.username)

    
    user = user_total.objects.filter(user_name = student).first()
    if not user:
        new_user = user_total(user_name = student)
        new_user.save()
        user = user_total.objects.filter(user_name = student).first()

    pres_data = checkpresence.objects.filter(user_name = student).first()
    if not pres_data:
        new_pres = checkpresence(user_name = student)
        new_pres.save()
        pres_data = checkpresence.objects.filter(user_name = student).first()

    if(pres_data.date != datetime.now().date()):
        pres_data.date = datetime.now().date()
        pres_data.breakfast = 0
        pres_data.lunch = 0
        pres_data.dinner = 0
        pres_data.save()
    
    if time(7,0) <= datetime.now().time() <= time(9,0):
        if pres_data.breakfast == 1:
            messages.error(request,"cannot mark attendance more than once a day for breakfast")
        else: 
            user.breakfast += 1
            date_data.breakfast += 1
            pres_data.breakfast += 1
            pres_data.save()
            date_data.save()
            user.save()
            messages.success(request,"attendance marked for breakfast")
    elif time(12,0) <= datetime.now().time() <= time(14,0):
        if pres_data.lunch == 1:
            messages.error(request,"cannot mark attendance more than once a day for lunch")
        else:
            user.lunch += 1
            date_data.lunch += 1
            pres_data.lunch += 1
            pres_data.save()
            date_data.save()
            user.save()
            messages.success(request,"attendance marked for lunch")
    elif time(19,0) <= datetime.now().time() <= time(21,0):
        if pres_data.dinner == 1:
            messages.error(request,"cannot mark attendance more than once a day for dinner")
        else:
            user.dinner += 1
            date_data.dinner += 1
            pres_data.dinner += 1
            pres_data.save()
            date_data.save()
            user.save()
            messages.success(request,"attendance marked for dinner")
    else:
        messages.success(request,"cannot mark your attendance right now")
    return redirect("stuhome")
    
def monthmenu(request):
    return render(request,"stupages/monthlymenu.html",{"menu_data":menu_data})

def unique_menu_items():
    try:
        fobj = open('menu.json','r')
        menu_data = json.load(fobj)
        item_list = []
        for date,time in menu_data.items():
            for key,value in time.items():
                for i in value:
                    if i not in item_list:
                        item_list.append(i)
                    else:
                        pass
        return item_list
    except:
        menu_data = {}

def menu_rating(request):
    item_list = unique_menu_items()
    if request.method == "POST":
        food = request.POST.get('selected_item')
        rating_int = request.POST.get("rating")

        try:
            studentuser = student_info.objects.get(user_name = request.user.username)
        except:
            new_info = student_info(user_name = request.user.username)
            new_info.save()
            studentuser = student_info(user_name = request.user.username)

        try:
            fooditem = food_items.objects.get(food_item = food)
        except:
            newfood = food_items(food_item = food)
            newfood.save()
            fooditem = food_items.objects.get(food_item = food)

        rating_data = rating_model.objects.filter(user_name = studentuser, food_item = fooditem).first()
        if not rating_data:
            rating_data = None
        try:
            rating_data.rating = rating_int
            rating_data.save()
            messages.success(request,"Rating updated")
        except:
            data = rating_model(user_name = studentuser, food_item = fooditem, rating = rating_int)
            data.save()
            messages.success(request,"Rating submited")
        food_total = food_items.objects.filter(food_item = food).first()



    food_list = food_items.objects.all()

    for i in food_list:
        food_total = food_items.objects.filter(food_item = i).first()
        if not food_total:
            new_item = food_items(food_item = i)
            new_item.save()
            food_total = food_items.objects.filter(food_item = i).first()
        total_rating = 0
        items = rating_model.objects.filter(food_item = i)
        for j in items:
            total_rating += j.rating
        item_count = rating_model.objects.filter(food_item = i).count()
        if(int(item_count) == 0):
            food_total.rating = 0
        else:
            food_total.rating = total_rating/int(item_count)
        food_total.save()

    item_Rating_dict = {}
    food_Rating_list = food_items.objects.all().order_by("-rating")
    for i in food_Rating_list:
        item_Rating_dict[i.food_item] = i.rating 

    return render(request,"stupages/rating.html",{'itemlist':item_list,'avg_rating':item_Rating_dict})

def feedback(request):
    if request.method == 'POST':
        form = Feedback_form(request.POST, request.FILES)
        try:
            studentinfo = student_info.objects.get(user_name = request.user.username)
        except:
            new_user = student_info(user_name = request.user.username)
            new_user.save()
            studentinfo = student_info.objects.get(user_name = request.user.username)

        if form.is_valid():
            fback = form.cleaned_data['feed_back']
            pic = form.cleaned_data['picture']
            data = Feedbacks(user_name = studentinfo,feed_back = fback,picture = pic)
            data.save()
            return HttpResponse('You feedback have been submited')
    else:
            form = Feedback_form()  

    return render(request,"stupages/feedback.html",{'form':form})

def student_data(request):
    bhawan_list = ["Bhagirath","Budh","C.V. Raman","Gandhi","Krishna","Malaviya","Meera","Meera","Ram","Shankar","Srinivas Ramanujan","Vishwakarma","Vyas"]

    if request.method == "POST":
        stu_bhawan = request.POST.get("bhawan")
        id = request.POST.get("stu_id")
        try:
            studentdata = student_info.objects.filter(user_name = request.user.username).first()
            studentdata.student_bhawan = stu_bhawan
            studentdata.student_id = id
            studentdata.save()
            return redirect("stuhome")

        except: 
            data = student_info(user_name = request.user.username, student_bhawan = stu_bhawan,student_id = id, email=request.user.email)
            data.save()
            return redirect("stuhome")

        


    return render(request,"stupages/student_info.html",{"bhawans":bhawan_list})

