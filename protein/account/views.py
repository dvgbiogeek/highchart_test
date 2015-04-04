from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.forms import ValidationError
from account.form import UserForm, CreateNewForm
import logging
logger = logging.getLogger(__name__)


def user_login(request):
    """Custom user login with custom form."""
    if request.method == 'POST':
        form = UserForm(request.POST)
        # Obtain username and password from the form for authenitcation
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # user = Userform.clean()
        logger.debug(user)
        # if user is known
        if user is not None:
            login(request, user)
            logger.debug(form)
            try:
                # Get next url for redirect
                current_url = request.META['HTTP_REFERER']
                redirect_url = current_url.split('=')[1]
                # if no next parameter is in the url, redirect to the home page
                if redirect_url == '':
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect(redirect_url)
            except:
                logger.debug('No redirect url')
                return HttpResponseRedirect('/')
        else:
            form = UserForm({'username': username, 'password': ''})
            return render(request, 'login.html', {'form': form})
    else:
        form = UserForm()
    return render(request, 'login.html', {'form': form})


def new_user(request):
    if request.method == 'POST':
        form = CreateNewForm(request.POST)
        print(form.as_p())
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/login/')
        else:
            return render(request, 'new_user.html', {'form': form})
    else:
        form = CreateNewForm()
    return render(request, 'new_user.html', {'form': form})
