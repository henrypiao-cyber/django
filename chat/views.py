from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from registerApp.getUsers import get_all_logged_in_users


# user_list=['admin', 'austin', 'aladin']
@login_required
def home(request):
    user = request.user

    # NON-ADMIN → auto enter own room
    if not user.is_superuser:
        room_name = user.username

        # create room if it does not exist
        Room.objects.get_or_create(name=room_name)

        return redirect(f'/chat/{room_name}/?username={user.username}')

    # ADMIN → can choose room
    return render(request, 'home.html', {'user': user})


@login_required
def room(request, room):
    user = request.user

    # NON-ADMIN cannot open other rooms
    if not user.is_superuser and room != user.username:
        return HttpResponse("Unauthorized", status=403)

    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)

    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


@login_required
def checkview(request):
    user = request.user

    # NON-ADMIN → force room = username
    if not user.is_superuser:
        room = user.username
        username = user.username
    else:
        room = request.POST.get('room_name')
        username = request.POST.get('username')

    Room.objects.get_or_create(name=room)

    return redirect(f'/chat/{room}/?username={username}')


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

    # Fetch last 50 messages (newest first)
    messages = list(
        Message.objects
        .filter(room=room_details.id)
        .order_by('-id')
        .values()[:50]
    )

    # Reverse to show oldest → newest
    messages.reverse()

    user = request.user
    user_list = get_all_logged_in_users()
    users = [str(i) for i in user_list]

    if "admin" in users and str(user) in users:
        online = users if str(user) == "admin" else "Online"
    else:
        online = "Offline"

    return JsonResponse({
        "messages": messages,   # ✅ NO .values() HERE
        "online": online
    })


