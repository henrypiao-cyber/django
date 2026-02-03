from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignUpForm
from .getUsers import get_all_logged_in_users
from django import template
from .telSend import chat_request

def frontpage(request):
    return render(request, 'frontpage.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

register = template.Library()

@register.inclusion_tag('templates/logged_in_user_list.html')
def render_logged_in_user_list(request):
    print(list(get_all_logged_in_users()), len(list(get_all_logged_in_users())))
    return render(request, 'logged_in_user_list.html', { 'users': get_all_logged_in_users() })

def contact(request):
    user = str(request.user)
    chat_request(user)
    return redirect(request.META.get('HTTP_REFERER')) # redirect to previous page