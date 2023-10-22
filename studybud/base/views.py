from django.shortcuts import render,redirect
from .models import Room,Topic,Message
from .forms import RoomForm,UserForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"user does not exist")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"invalid credentials")
            
            
    context = {'page':page}
    return render(request,'base/login_register.html',context)


def RegisterUser(request):   
    form = UserCreationForm()
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)   #able to get the user object
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"internal server error , try later")
    return render(request,'base/login_register.html',{'form':form})
    


def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    room_list = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)  
        )
    room_count = room_list.count()
    topics = Topic.objects.all()[:5]
    room_messages = Message.objects.all().filter(Q(room__topic__name__icontains=q))
    context = {'rooms':room_list,'topics':topics,'room_count':room_count,"room_messages":room_messages}
    return render(request,'base/home.html',context)


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

def rooms(request,pk):
    room_list = Room.objects.get(id=pk)
    room_messages = room_list.message_set.all().order_by('updated')
    participants = room_list.participants.all()
    
    if request.method=='POST':
        message = Message.objects.create(
            user = request.user,
            room = room_list,
            body = request.POST.get('body')
        )
        room_list.participants.add(request.user)
        return redirect('room',pk=room_list.id)
    context = {"room":room_list,'room_messages':room_messages,'participants':participants}
    return render(request,"base/room.html",context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic,create = Topic.objects.get_or_create(name= topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name = request.POST.get("name"),
            description = request.POST.get("description"),
            
        )
        return redirect('home')
        
        
    context = {'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance= room)
    
    if request.user !=room.host:
        return HttpResponse("action not allowed")
        
    
    if request.method=='POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user !=room.host:
        return HttpResponse("action not allowed")
        
    if request.method=="POST":
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})
    
    
def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user !=message.user:
        return HttpResponse("action not allowed")
        
    if request.method=="POST":
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})



@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile',pk=user.id)
        
    return render(request,'base/update-user.html',{'form':form})


def topicsPage(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)
    return render(request,'base/topics.html',{"topics":topics})


def activitiyPage(request):
    room_messages = Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})
    
    
    
        