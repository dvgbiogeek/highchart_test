from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)


def home(request):
    logger.debug('Render home page')
    return render(request, 'home.html')
