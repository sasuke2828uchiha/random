from django.shortcuts import render,redirect
from staffdeck.models import staff_info


def home_page(request):
    staff_members_list = []
    staff_object = staff_info.objects.all()
    for i in staff_object:
        staff_members_list.append(i.user_name)
    return render(request,'home/home.html',{"staff_names":staff_members_list})


