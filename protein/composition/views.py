from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from composition.form import ProteinForm
from composition.models import Protein
import json
import logging
logger = logging.getLogger(__name__)


def home(request):
    logger.debug('Render home page')
    return render(request, 'home.html')


def protein(request):
    """Form for inputting a protein name and sequence."""
    # logger.debug(request)
    if request.method == 'POST':
        # After submission of the form the data is cleaned and if valid, the
        # data is added to the database.
        form = ProteinForm(request.POST)
        logger.debug(form)
        if form.is_valid():
            form = ProteinForm(request.POST)
            # instance is the data object
            instance = form.save()
            logger.debug(instance)
            return HttpResponseRedirect('/composition/' + str(instance.pk))
    else:
        # If not a POST request, generate a new instance of the form.
        form = ProteinForm()
        logger.debug(form)
    return render(request, 'protein_form.html', {'form': form})


def protein_detail(request, protein_id):
    """
    At '/protein/id' the data is shown as a json object including the protein
    name, sequence, amino acid numbers, and length.
    """
    protein_dict = build_protein_dict(protein_id)
    logger.debug(protein_dict)
    return HttpResponse(protein_dict)


def composition_detail(request, protein_id):
    """
    The url where highcharts will be used to show the data based on the protein
    data submitted through the form.
    """
    return render(request, 'composition.html')


def build_aa_dict(protein_id):
    """Generates a dictionary with the numbers of each amino acid."""
    aa = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P',
          'R', 'S', 'T', 'W', 'Y']
    aa_content = {}
    sequence = Protein.objects.get(pk=protein_id).sequence
    for a in aa:
        aa_content[a] = sequence.count(a)
    return aa_content


def convert_dict_to_array(protein_id):
    dict_list = []
    prot_dict = build_aa_dict(protein_id)
    for key, value in prot_dict.items():
        temp = [key, value]
        dict_list.append(temp)
    return dict_list


def build_protein_dict(protein_id):
    """
    Creates a json dictionary with the protein data for the name, sequence,
    length, and amino acid breakdown.
    """
    protein = Protein.objects.get(pk=protein_id)
    protein_dict = {
        'name': protein.name,
        'sequence': protein.sequence,
        'length': len(protein.sequence),
        'amino acids': build_aa_dict(protein_id),
        'amino': convert_dict_to_array(protein_id),
    }
    protein_json = json.dumps(protein_dict)
    return protein_json
