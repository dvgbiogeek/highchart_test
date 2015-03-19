from django.shortcuts import render
from django.http import HttpResponseRedirect
from composition.form import ProteinForm
from composition.models import Protein
import logging
logger = logging.getLogger(__name__)


def home(request):
    logger.debug('Render home page')
    return render(request, 'home.html')


def protein(request):
    if request.method == 'POST':
        form = ProteinForm(request.POST)
        if form.is_valid():
            # protein = Protein.objects.get(pk=protein_id)
            # populates the form with previous data
            form = ProteinForm(request.POST)
            form.save()
            logger.debug(form)
            # p = Protein.objects.get(pk=)
            return HttpResponseRedirect('thanks/')
    else:
        form = ProteinForm()
    return render(request, 'protein_form.html', {'form': form})


def thanks(request):
    return render(request, 'thanks.html')
