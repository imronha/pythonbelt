from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip
import re
import bcrypt

#----------------- Login/Reg +Validation -------------#
def index(request):
    return render(request, "travel/index.html")

def register(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors):
        #print error message if fails validation
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        #Search the db to see if the user already exists
        found_user = User.objects.filter(username=request.POST['username'])
        if found_user.count() > 0:
            messages.error(request, "Username already taken.", extra_tags="username")
            return redirect('/')
        else:
            #If the found user doesnt exist, hash their pw and create user object
            hashed_pw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed_pw)
            messages.success(request, 'Successfully registered, you may now log in.')
            return redirect('/')

def login(request):
    #Check to see if we find any users with the email provided
    found_users = User.objects.filter(username=request.POST['username'])
    if len(found_users) >0:
        #If found, check if their pw matches the hashed pw stored in db
        found_user= found_users.first()
        if bcrypt.checkpw(request.POST['pw'].encode(), found_user.password.encode()) == True:
            #Successfully logged in
            request.session['user_id'] = found_user.id
            request.session['name'] = found_user.name
            print found_user
            return redirect('/travels')
        else:
            messages.error(request, "Login failed", extra_tags="email")
            return redirect('/')
    else:
        messages.error(request, "Login failed", extra_tags="email")
        return redirect('/')

def logout(request):
    del request.session['user_id']
    del request.session['name']
    return redirect('/')
#----------------- End Login/Reg +Validation --------------#

#----------------- Home Page/ all trip info ---------------#
def travels(request):
    context = {
        "all_trips": Trip.objects.exclude(joined__id=request.session['user_id']),
        "all_users_trips": Trip.objects.filter(joined__id=request.session['user_id'])

    }
    return render(request, "travel/travels.html", context)
#--------------- END Home Page/ all trip info -------------#

#------------------  Trip Page/ add trip ------------------#
def destination(request, trip_id):
    # Pass info needed for trip/ joining users display page
    context = {
        "trip_info": Trip.objects.get(id=trip_id),
        "planner":Trip.objects.get(id=trip_id).user,
        "users": User.objects.filter(joining__id=trip_id),
        "joined": Trip.objects.filter(joined__id= trip_id)
    }
    return render(request, "travel/destination.html", context)

def add_trip_page(request):
    # Renders add trip page
    return render(request, "travel/add_trip.html")

def add_trip(request):
    # Validates trip info
    errors = Trip.objects.trip_validator(request.POST)
    if request.method == "POST":
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/add_trip_page')
        # Create trip if valid
        Trip.objects.create(plan=request.POST['plan'], destination=request.POST['destination'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], user=User.objects.get(id=request.session['user_id']))
        return redirect('/travels')
    context = {
        "current_user": User.objects.get(id=request.session['user_id'])
    }
    return redirect('/travels')

#----------------  END Trip Page/ add trip ---------------#
#-----------------  Add Trip/ Remove trip ----------------#

def joined(request):
    # Joins user to a trip
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=request.POST['hidden'])
    print trip
    user.joining.add(trip)
    return redirect('/travels')

def remove(request):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=request.POST['hidden'])
    user.joining.remove(trip)
    return redirect('/travels')
