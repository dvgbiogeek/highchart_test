from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from Bio.SeqUtils import ProtParam
from composition.form import ProteinForm
from composition.models import Protein
import json
import logging
logger = logging.getLogger(__name__)


def home(request):
    """Renders the home page."""
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
            return HttpResponseRedirect('/protein/composition/' + str(instance.pk))
        else:
            # Renders the errors if the form is not valid
            return render(request, 'protein_form.html', {'form': form})
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
    The url where highcharts and ng-Table are used to show the data based on
    the sequence data submitted through the form.
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


def build_aa_percent(protein_id):
    """Generates a dictionary with the percent of each amino acid."""
    aa = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P',
          'R', 'S', 'T', 'W', 'Y']
    aa_content = {}
    sequence = Protein.objects.get(pk=protein_id).sequence
    seq_length = len(sequence)
    for a in aa:
        aa_content[a] = round(sequence.count(a)/seq_length*100, 1)
    return aa_content


def build_protein_dict(protein_id):
    """
    Creates a json dictionary with the protein data for the name, sequence,
    data (length, molecular weight ...), and amino acid breakdown.
    """
    protein = Protein.objects.get(pk=protein_id)
    protein_dict = {
        'name': protein.name,
        'sequence': protein.sequence,
        'protein': protein_data(protein_id),
        'amino': convert_dict_to_array(protein_id),
        'aminoPercent': percent_array(protein_id),
        'secondary': dict_to_array(protein_id),
    }
    protein_json = json.dumps(protein_dict)
    return protein_json


def protein_data(protein_id):
    """
    Uses the Biopython package to get the molecular weight, length, and
    isoelectric point of a protein and returns a dictionary of the data. This
    dictionary is used by ng-Table.
    """
    protein = Protein.objects.get(pk=protein_id)
    seq = protein.sequence
    # Initialize the Protein Analysis class using the sequence of the protein
    # as a string
    prot = ProtParam.ProteinAnalysis(seq)
    data_dict = [
        {'name': 'Length', 'value': prot.length},
        {'name': 'Molecular Weight', 'value': prot.molecular_weight()},
        {'name': 'Isoelectric Point', 'value': prot.isoelectric_point()},
        {'name': 'Instability Index', 'value': prot.instability_index()},
        {'name': 'Aromaticity', 'value': prot.aromaticity() * 100},
        {'name': 'Hydrophobicity', 'value': prot.gravy()},
    ]
    return data_dict


def secondary_structure_dict(protein_id):
    protein = Protein.objects.get(pk=protein_id)
    seq = protein.sequence
    prot = ProtParam.ProteinAnalysis(seq)
    structure = list(prot.secondary_structure_fraction())
    rounded_structure = []
    for e in structure:
        rounded_structure.append(round(e, 2))
    # return structure
    secondary = ['Helix', 'Turn', 'Sheet']
    # for sec in secondary:
    comp = dict(zip(secondary, rounded_structure))
    return comp


def convert_dict_to_array(protein_id):
    """
    Converts amino acid data to an array as the series format for highcharts.
    """
    dict_list = []
    prot_dict = build_aa_dict(protein_id)
    for key, value in prot_dict.items():
        temp = [key, value]
        dict_list.append(temp)
    return dict_list


def dict_to_array(protein_id):
    array_list = []
    secondary = secondary_structure_dict(protein_id)
    for key, value in secondary.items():
        temp = [key, value]
        array_list.append(temp)
    return array_list


def percent_array(protein_id):
    p_array = []
    percents = build_aa_percent(protein_id)
    for key, value in percents.items():
        temp = [key, value]
        p_array.append(temp)
    return p_array


def thanks(request):
    return render(request, 'thanks.html')
