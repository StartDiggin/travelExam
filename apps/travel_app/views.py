# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login_app.models import User
from models import Travel
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime

# Create your views here.
def index(request):
    if not 'id' in request.session:
        messages.error(request,'Please log in again!')
        return redirect('/')

    cur_user = User.objects.get(id=request.session['id'])
    context={
        'cur_user': User.objects.get(id=request.session['id']),
        'other_users': User.objects.exclude(id=request.session['id']),
        'mytrips': cur_user.trips.all(),
        'alltrips': Travel.objects.all(),
    }
    return render(request,'travel_app/index.html', context)

def new(request):
    if not 'id' in request.session:
        messages.error(request,'Please log in again!')
        return redirect('/')
    return render(request,'travel_app/add.html')

def create(request):
    if not 'id' in request.session:
        messages.error(request,'Please log in again!')
        return redirect('/')
    if len(request.POST['destination'].strip()) < 1:
        messages.error(request, 'Destination not valid')
        return redirect('/travel/')
    if len(request.POST['description'].strip()) < 1:
        messages.error(request, 'Description needed')
        return redirect('/travel/')
    if request.POST['from_date'] <= str(datetime.date.today()):
        messages.error(request,'Travel Date not valid!')
        return redirect('/travel/')
    else:
        user = User.objects.get(id=request.session['id'])
        trip = Travel.objects.create(destination=request.POST['destination'], description=request.POST['description'], from_date=request.POST['from_date'], to_date=request.POST['to_date'])
        user.trips.add(trip)
        return redirect('/travel/')

def show(request, id):
    if not 'id' in request.session:
        messages.error(request,'Please log in again!')
        return redirect('/')
    name = User.objects.filter(trips__id=id)[0].first_name
    context={
        'trip': Travel.objects.get(id=id),
        'travelers': User.objects.filter(trips__id=id).exclude(first_name=User.objects.filter(trips__id=id)[0].first_name),
    }
    return render(request,'travel_app/destination.html',context)

def update(request, id):
    cur_user =  User.objects.get(id=request.session['id'])
    trip = Travel.objects.get(id=id)
    cur_user.trips.add(trip)
    return redirect('/travel/')
