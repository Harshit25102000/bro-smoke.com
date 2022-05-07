from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.db.models import Min, Max , Sum
from datetime import date
def index(request):

    return render(request,'brosmokingapp/index.html')

import math

def myaccount(request):

    if request.user.is_authenticated:
        queryset = Profile.objects.get(user=request.user)

        aggregate = data.objects.filter(user=request.user).aggregate(Min('date'), Max('date'), Sum('qty'), Sum('cost'))
        min_date = aggregate.get('date__min')

        if min_date is not None:
            curr_date = date(datetime.today().year, datetime.today().month, datetime.today().day)
            # print(curr_date)
            max_date = aggregate.get('date__max')
            total_cig = aggregate.get('qty__sum')
            total_cost = aggregate.get('cost__sum')
            days = (curr_date - min_date).days + 1


        context = {'queryset': queryset,'cig': total_cig, 'min': min_date, 'max': max_date, 'days': days, 'cost': total_cost}



        return render(request,'brosmokingapp/myaccount.html',context)
    else:
        messages.error(request, 'Please login to continue')
        return render(request,'brosmokingapp/login.html')

def make_entry(request):

    from datetime import timedelta
    if request.user.is_authenticated:

        if request.method == 'POST':
            name= request.POST['name']
            quantity = request.POST['quantity']
            price = request.POST['price']
            dates = request.POST['date']
            time = request.POST['time']

            print(name,quantity,price,dates,time)

            if name=='':
                name="Not given"



            if dates=='':
                now = datetime.now()
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                print("date  =", dt_string[:10])
                print("time =", dt_string[11:])
                dates = dt_string[:10]
                time = dt_string[11:]

            data.objects.create(user = request.user,cig=name, qty=quantity, cost=price, date=dates, time=time)

        aggregate = data.objects.filter(user=request.user).aggregate(Min('date'), Max('date'), Sum('qty'), Sum('cost'))
        min_date = aggregate.get('date__min')

        if min_date is not None:
            curr_date = date(datetime.today().year,  datetime.today().month,  datetime.today().day)
            #print(curr_date)
            max_date = aggregate.get('date__max')
            total_cig = aggregate.get('qty__sum')
            total_cost = aggregate.get('cost__sum')
            days = (curr_date - min_date).days + 1
            datas = {'cig': total_cig, 'min': min_date, 'max': max_date, 'days': days, 'cost': total_cost}
            print(datas)
            weeks = days / 7
            months = weeks / 4
            years = months / 12
            print(days, weeks, months, years)
            context = {'cigday': math.floor(total_cig / days), 'cigmonth': math.floor(total_cig / months),
                       'cigweek': math.floor(total_cig / weeks),
                       'cigyear': math.floor(total_cig / years), 'expday': math.floor(total_cost / days),
                       'expmonth': math.floor(total_cost / months),
                       'expyear': math.floor(total_cost / years), 'expweek': math.floor(total_cost / weeks),
                       'first_date': min_date,
                       'last_date': max_date,
                       'total_cig': total_cig, 'days': days, 'cost': total_cost}
            print(context)

            check = Profile.objects.filter(user=request.user).first()
            if check is not None:
                Profile.objects.update(
                                                 cigday=context['cigday'],
                                                 cigweek=context['cigweek'],
                                                 cigmonth=context['cigmonth'],
                                                 cigyear=context['cigyear'],
                                                 expday=context['expday'],
                                                 expweek=context['expweek'],
                                                 expmonth=context['expmonth'],
                                                 expyear=context['expyear'],

                                                 )
            else:
                Profile.objects.create(user=request.user,
                                       cigday=context['cigday'],
                                       cigweek=context['cigweek'],
                                       cigmonth=context['cigmonth'],
                                       cigyear=context['cigyear'],
                                       expday=context['expday'],
                                       expweek=context['expweek'],
                                       expmonth=context['expmonth'],
                                       expyear=context['expyear'],

                                       )




        messages.success(request, 'Entry created')
        return redirect('Home')

    else:
        messages.error(request, 'Please login to continue')
        return render(request,'brosmokingapp/login.html')

def searchresult(request):
    if request.method == "GET":
        ls=[]
        query = request.GET.get('query', "")
        bros=User.objects.filter(username__icontains=query)
        for bro in bros:
            profiles=Profile.objects.get(user=bro)
            ls.append(profiles)
        data=zip(bros,ls)
        context = {'bros': bros,'query': query,'ls':ls,'data':data}

        return render(request,'brosmokingapp/searchresults.html',context)

    else:
        return HttpResponse("Access Denied")

def signup(request):
    return render(request,'brosmokingapp/signup.html')

def loginpage(request):
    return render(request,'brosmokingapp/login.html')

def handle_signup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']

        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        print(username, pass1, pass2)
        # check for errorneous input
        if len(username) < 5:
            messages.error(request, " Your user name must be greater than 5 characters")
            return redirect('signup')

        if len(username) >= 50:
            messages.error(request, " Your user name must be shorter than 50 characters")
            return redirect('signup')

        user = User.objects.filter(username=username).first()

        if user:
            messages.error(request, 'Account already exists with this Email ')
            return redirect('signup')

        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('signup')

        # Create the user
        myuser = User.objects.create_user(username, pass1)

        myuser.save()
        messages.success(request, " Your account has been successfully created")
        return redirect('Home')

    else:
        return HttpResponse("404 - Not found")


def handle_login(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['username']
        loginpassword = request.POST['pass']
        print(loginusername, loginpassword)
        user = authenticate(request,username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("Home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("login")

    return HttpResponse("404- Not found")

def handlecontactus(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST['name']
            surname = request.POST['surname']
            email=request.POST['email']
            message = request.POST['message']
            if name=='':
                name='blank'
            if email=='':
                email='blank'
            if surname=='':
                surname='blank'

            contactus.objects.create(firstname=name, email=email, lastname=surname,message=message,user=request.user)
        return HttpResponse('Done')

    else:

        messages.error(request, 'Please login to continue')
        return render(request, 'brosmokingapp/login.html')

def forgotpassword(request):
    return render(request, 'brosmokingapp/forgotpassword.html')

def handle_username(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            if user is not None:
                return redirect('reset_password')
        except:
            messages.error(request, 'No account exists with this username')
            return redirect('forgotpassword')


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('Home')

def allbros(request):

    bros=Profile.objects.all().order_by('cigday')
    context={'bros':bros}
    return render(request,'brosmokingapp/allbros.html',context)

def about(request):
    return render(request,'brosmokingapp/about.html')

def contact(request):
    return render(request,'brosmokingapp/contact.html')

def history(request):

    if request.user.is_authenticated:
        entries = data.objects.filter(user=request.user)
        context = {'entries': entries}
        return render (request,'brosmokingapp/history.html',context)
    else:
        return HttpResponse("Bad request")

def change_password(request):
    return render(request,'brosmokingapp/changepassword.html')

def handle_changepassword(request):
    if request.method == 'POST':
        username = request.user
        current_password = request.POST['curr-pw']
        user = authenticate(username=username,password=current_password)
        password1 = request.POST['new-pw1']
        password2 = request.POST['new-pw2']

        if user is not None:
            if password1 != password2:
                messages.error(request, 'passwords do not match')
                return redirect('change_password')
            u = User.objects.get(username=username)
            u.set_password(password1)
            u.save()
            messages.success(request, 'password changed successfully')

            return redirect('login')
        else:
            messages.error(request, 'Invalid password')
            return redirect('change_password')
    else:
        return HttpResponse('404 Not Allowed')