from studeck.models import Feedbacks
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from staffdeck.models import staff_info
import pandas as pd
from django.http import FileResponse
import os
from django.conf import settings
import json
from .forms import UploadMessMenu
from studeck.models import total_daily,user_total
from datetime import datetime,time,timedelta
import csv

def feedback_view(request):
    data = Feedbacks.objects.all()
    return render(request,'staffpages/feedbackview.html',{'data':data})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        passwrd = request.POST.get("pass")
        user = authenticate(request,username=username,password=passwrd)
        try:
            login(request,user)
            return redirect('staffhome')
        except:
            return render(request,'auth/login.html',{
                "error_message":"Incorrect password or username"
            }) 
    else:
        return render(request,"auth/login.html",{})

def log_out(request):
    logout(request)
    return redirect("home")

def menu_parse(filepath):
    excel_data = pd.read_excel(filepath,skiprows=1)
    menu_dict = {}

    print(excel_data)

    for columns in excel_data.columns:
        for value in excel_data[columns]:
            print(str(value))
            if str(value).upper() in ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]:
                pass
            elif "*" in str(value).upper():
                pass
            elif str(value).lower() == "nan":
                pass
            elif "BREAKFAST" in str(value).upper():
                meal = "breakfast"
                menu_dict.setdefault(columns.strftime("%Y-%m-%d"),{})[meal] = []
            elif "LUNCH" in str(value).upper():
                meal = "lunch"
                menu_dict.setdefault(columns.strftime("%Y-%m-%d"),{})[meal] = []
            elif "DINNER" in str(value).upper():
                meal = "dinner"
                menu_dict.setdefault(columns.strftime("%Y-%m-%d"),{})[meal] = []
            elif "GRUB" in str(value).upper():
                meal = "grub"
                menu_dict.setdefault(columns.strftime("%Y-%m-%d"),{})[meal] = []
            else:
                if meal:
                    menu_dict[columns.strftime("%Y-%m-%d")][meal].append(value)

    menu_json = json.dumps(menu_dict,indent=4)

    with open("menu.json","w") as json_file:
        json_file.write(menu_json)

def staff_home(request):
    if request.method == 'POST':
        form = UploadMessMenu(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()

            if not uploaded_file.file.name.endswith('.xlsx'):
                return HttpResponse("file format not supported")
            else:
                file_path = uploaded_file.file.path
                menu_parse(filepath=file_path)            
    else:
        form = UploadMessMenu()  
    user_username = request.user.username
    user_data = staff_info.objects.filter(user_name = user_username)     

    current_date = datetime.now().date()

    five_day_list = []
    i = 1
    while i < 6:
        dates = current_date - timedelta(days=i)
        five_day_list.append(dates)
        i += 1

    total_present = []

    for i in five_day_list:
        data = total_daily.objects.filter(date = i).first()
        if not data:
            new_date = total_daily(date = i)
            new_date.save()
        else: pass

    for i in five_day_list:
        day_total = total_daily.objects.filter(date = i).first()
        total_stu_list = [day_total.breakfast,day_total.lunch,day_total.dinner]
        total_present.append(total_stu_list)

    attendance_data = {}
    for i in range(0,5):
        attendance_data[five_day_list[i]] = total_present[i]

    staff_members_list = []
    staff_object = staff_info.objects.all()
    for i in staff_object:
        staff_members_list.append(i.user_name)
    
    return render(request,'home/staffhome.html',{'user_data':user_data,'form':form,"attendance_data":attendance_data,"staff_unames":staff_members_list})

def calc_bill(user_n):
    user = user_total.objects.filter(user_name = user_n).first()
    b_total = user.breakfast * 80
    l_total = user.lunch * 180
    d_total = user.dinner * 150
    bill = b_total + l_total + d_total
    return bill
       
def bill(request):
    user_names = []
    users = user_total.objects.all()
    for usernames in users:
        user_names.append(usernames.user_name)
    
    user_bills = []
    for name in user_names:
        bill = calc_bill(name)
        user_bills.append(bill)

    bill_dict = {}
    for i in range(0,len(user_names)):
        bill_dict[user_names[i]] = user_bills[i]
    
    fobj = open('bills.csv','w+')
    wobj = csv.writer(fobj)
    headings = ["username","fees"]
    wobj.writerow(headings)
    for username,fees in bill_dict.items():
        dataset = [username,fees]
        wobj.writerow(dataset)
    fobj.close()

    return render(request,"staffpages/bills.html",{"bill":bill_dict})

def signup_user(request):
    if request.method == "POST":
        mess_name = request.POST.get("mess_name")
        id = request.POST.get("staff_id")
        f_name = request.POST.get("first_name")
        l_name = request.POST.get("last_name")
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        if pass1!=pass2:
                return HttpResponse("Password do not match, Try again")
        else:
            try:
                data = staff_info(user_name = uname,staff_id=id,staff_fname=f_name,staff_lname=l_name,staff_email=email,staff_mess=mess_name)
                data.save()
                try:
                    my_user=User.objects.create_user(uname,email,pass1)
                    my_user.save()
                except:
                    return HttpResponse("Username not unique")
            except:
                return HttpResponse("ID not unique")
        return redirect('login_u')

    else:
        return render(request,'auth/signup.html',{})

def user_bills(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'bills.csv')
    with open(file_path, 'r') as csv_file:
        response = HttpResponse(csv_file.read(), content_type='csv')
        response['Content-Disposition'] = 'attachment; filename="bills.csv"'
    return response