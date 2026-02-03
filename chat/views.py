from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from registerApp.getUsers import get_all_logged_in_users

# user_list=['admin', 'austin', 'aladin']
@login_required
def home(request):
    # if request.user.is_authenticated():
    #     username = request.user.username
    user = request.user 
    print(user)
    return render(request, 'home.html', {'user':user})

@login_required
def room(request, room):
    
    username = request.GET.get('username')
    
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

@login_required
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    print(room, username)
    if Room.objects.filter(name=room).exists(): 
        return redirect('/chat/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/chat/'+room+'/?username='+username)

@login_required
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

@login_required
def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    user = request.user
    
    user_list=get_all_logged_in_users()
    print(user_list)
    users=[]
    for i in user_list:
        users.append(str(i))
    print(users)
    print(str(user))
    if "admin" in users and str(user) in users: 
        online='Online'
        if str(user)=='admin':
            online=users
    else:
        online='Offline'

        
    return JsonResponse({"messages":list(messages.values()), 'online':online})

