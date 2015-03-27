from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)


def terms(request):
    logger.debug('Glossary terms called')
    return render(request, 'glossary.html')
