from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    # print('-----------------------------')
    # print(User.objects.values('username'))
    # print(User.objects.values('username')[0])
    # print(User.objects.values('username')[0]['username'])
    # print('-----------------------------')
    # for i in User.objects.values('username'):
    #     print(i['username'])
    # print('-----------------------------')
    # print(User.objects.filter(id__in=uid_list)[0], type(str(User.objects.filter(id__in=uid_list)[0])))
    # return User.objects.filter(id__in=uid_list)

    return User.objects.filter(id__in=uid_list)