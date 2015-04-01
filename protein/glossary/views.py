from django.shortcuts import render
from django.http import HttpResponseRedirect
from glossary.form import GlossaryForm
import logging
logger = logging.getLogger(__name__)


def terms(request):
    logger.debug('Glossary terms called')
    return render(request, 'glossary.html')


def new(request):
    """Form for adding a new glossary term to the app."""
    if request.method == 'POST':
        form = GlossaryForm(request.POST)
        logger.debug(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/glossary/')
        else:
            # Shows previously inputs in the form with errors specific to
            # invalid inputs
            return render(request, 'glossary_form.html', {'form': form})
    else:
        form = GlossaryForm()
    return render(request, 'glossary_form.html', {'form': form})
