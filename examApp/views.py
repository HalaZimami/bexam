from contextlib import redirect_stderr
from turtle import clear
import bcrypt, datetime
from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponse
from .models import *

def index(request):
    return render(request, "index.html")

def signin(request):
    return render(request, "signin.html")

def register(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            pwHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            newUser = User.objects.create(fname=fname,lname=lname,email=email,password=pwHash)
            newUser.save()
            request.session['loggedInUser'] = newUser.id
            return redirect('/home')

def login(request):
    if request.method=='POST':
        users = User.objects.filter(email=request.POST['email'])
        if len(users)==1:
            if not bcrypt.checkpw(request.POST['password'].encode(),users[0].password.encode()):
                messages.error(request, "Email or Password is incorrect!")
                return redirect('/signin')
            else:
                request.session['loggedInUser'] = users[0].id
                return redirect('/home')
        else:
            messages.error(request, "Email does not exist!")
            return redirect('/')

def home(request):
    if not 'loggedInUser' in request.session:
        return redirect('/')
    else:
        context = {
            'logedin':User.objects.get(id=request.session['loggedInUser']),
            'user':User.objects.all(),
            'wishes':Wish.objects.all(),
        }
        return render(request,'homePage.html',context)

def logout(request):
    request.session.clear()
    return redirect('/signin')

def wish(request):
    if not 'loggedInUser' in request.session:
        return redirect('/')
    else:
        context = {
            'user':User.objects.get(id=request.session['loggedInUser']),
        }
    return render(request, 'makewish.html', context)


def makewish(request):
    if request.method == 'POST':
        errors = Wish.objects.validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/makewish')
        else:
            title = request.POST['title']
            desc = request.POST['desc']
            created_by = User.objects.get(id=request.session['loggedInUser'])
            newWish = Wish.objects.create(title=title,desc=desc,created_by=created_by)
            newWish.save()
            return redirect('/home')

def delete(request, _id):
    wish=Wish.objects.get(id=_id)
    wish.delete()
    return redirect('/home')

def edit(request, _id):
    wish=Wish.objects.get(id=_id)
    context={
        'wish':wish,
        'logedin':User.objects.get(id=request.session['loggedInUser']),
    }
    return render(request, 'edit.html', context)

def update(request, _id):
    errors = Wish.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit/{_id}')

    else:
        wish=Wish.objects.get(id=_id)
        wish.title=request.POST['title'] 
        wish.desc=request.POST['desc']
        wish.save()
    return redirect('/home')

def like(request,_id):
    wish = Wish.objects.get(id=_id)
    user = User.objects.get(id=request.session['loggedInUser'])
    user.likes.add(wish)
    return redirect(f'/home')

def grant(request, _id):
    wish = Wish.objects.get(id=_id)
    user = User.objects.get(id=request.session['loggedInUser'])
    user.lists.add(wish)
    return redirect(f'/home')

def stats(request):
    if not 'loggedInUser' in request.session:
        return redirect('/')
    else:
        context = {
            'logedin':User.objects.get(id=request.session['loggedInUser']),
            'user':User.objects.all(),
            'wishes':Wish.objects.all().order_by('-createdAt'),
        }
    return render(request, 'stats.html', context)