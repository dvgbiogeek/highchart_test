from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)


def terms(request):
    logger.debug('Glossary terms called')
    return render(request, 'glossary.html')


def new(request):
    logger.debug('new glossary called')
    return render(request, 'thanks.html')
