from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from account.form import UserForm
import logging
logger = logging.getLogger(__name__)


def user_login(request):
    """Custom user login with custom form."""
    if request.method == 'POST':
        form = UserForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        logger.debug(user)
        if user is not None:
            login(request, user)
            logger.debug(form)
            return HttpResponseRedirect('/')
        else:
            form = UserForm({'username': username, 'password': ''})
            return render(request, 'login.html', {'form': form})
    else:
        form = UserForm()
        logger.debug(form)
    return render(request, 'login.html', {'form': form})
