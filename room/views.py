from django.shortcuts import render
from .models import Room,Message
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required    #to make sure that a login authentication is required to access this view
def rooms(request):
    rooms=Room.objects.all()
    return render(request,'room/room.html',{'rooms':rooms})

@login_required
def room(request,slug):
    room=Room.objects.get(slug=slug)
    messages=Message.objects.filter(room=room)[0:25]
    return render(request,'room/roomview.html',{'room':room,'messages':messages})