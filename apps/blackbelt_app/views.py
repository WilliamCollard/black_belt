from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt


# Create your views here.


def index(request):


    return render(request, 'blackbelt_app/index.html')

def new_user(request):
    print("PRINTING POST DATA: ", request.POST)

    #<<--------VALIDATIONS-------->>
    errors = User.objects.basic_validator(request.POST)


    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)

        print(errors)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        hash_brown = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name= request.POST['name'], username = request.POST['username'], password = hash_brown.decode('utf-8'))

        #store user id in session
        request.session['id'] = user.id
        request.session['username']=user.username

        return redirect('/user_dash')


def user_dash(request):
    if len(request.session.keys()) > 0:
        all_trips=Trip.objects.all()
        user_joined=Join.objects.filter(user_id=request.session['id'])

        for i in user_joined:
            all_trips=all_trips.exclude(id=i.trip_id)

        context={
            'all_trips':all_trips,
            'user_joined': user_joined
        }
        return render(request, 'blackbelt_app/user_dash.html', context)
    else: 
        return redirect('/')

def login(request):
    print("LOGIN REQUEST EXECUTED")
    print(request.POST)

    errors = User.objects.login_validator(request.POST)
    print(errors)


    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)

        print(errors)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        user = User.objects.get(username=request.POST['username'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print("password match")
            request.session['id'] = user.id
            request.session['username']=user.username
            return redirect('/user_dash')
        else:

            print("failed password")
            messages.error(request, "Wrong password")



            return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def add_trip(request):
    return render(request, "blackbelt_app/addmovie.html")

def create_trip(request):
    print(request.POST)

    errors = Trip.objects.trip_validator(request.POST)
    print(errors)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)


        print(errors)
        return redirect('/add_trip')
    else:
        Trip.objects.create(destination=request.POST['destination'], plan=request.POST['plan'], start_date=request.POST['start_date'], end_date= request.POST['end_date'], added_by_id= request.session['id'])
        return redirect('/user_dash')

def joined(request, trip_id):
    Join.objects.create(trip_id=trip_id, user_id=request.session['id'])
    return redirect('/user_dash')

def show(request, trip_id):
    
    trip = Trip.objects.get(id=trip_id)
    user_joined=Join.objects.filter(trip_id=trip_id)
    context = {
        'trip': trip,
        'user_joined': user_joined
    }
    print(trip.id)
    return render(request, 'blackbelt_app/show.html', context)

def delete(request, trip_id):
    b = Trip.objects.get(id=trip_id)
    b.delete()
    return redirect( "/user_dash")

