from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from Bio.SeqUtils import ProtParam
from composition.form import ProteinForm
from composition.models import Protein
import json
import re
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
        'localization': localization(protein_id),
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


def localization(protein_id):
    protein = Protein.objects.get(pk=protein_id)
    seq = protein.sequence
    data_dict = [
        {'name': 'Nucleus', 'value': nucleus(seq)},
        {'name': 'Secretory Pathway', 'value': er_localization(seq)},
        {'name': 'Cytoplasm', 'value': cytoplasm(seq)},
    ]
    return data_dict


def cytoplasm(seq):
    if secretory_pathway(seq):
        return "Since this protein is synthesized in the ER, it is unlikely to be found in the cytoplasm"
    elif nls(seq):
        return "Many nuclear proteins shuttle between the cytoplasm and nucleus"
    else:
        return "This protein is likely found in the cytoplasm, but could also be localized to mitochondria"


def secretory_pathway(seq):
    n_term = seq[:45]
    pattern = re.compile(r'[AFILPV]{5,}')
    other = re.compile(r'[AFILPV]{4}.{,2}[AFILPV]{3,}')
    match = pattern.search(n_term)
    alt_match = other.search(n_term)
    if match or alt_match:
        # return the matching sequence and index
        return True
    else:
        return False


def er_localization(seq):
    if secretory_pathway(seq):
        if er_only(seq):
            return "Endoplasmic reticulum localization only"
        elif transmembrane_only(seq):
            return "Protein is likely within the membrane of the ER"
        else:
            return "Protein is part of the secretory pathway"
    else:
        return "Not a secretory pathway protein"


def er_only(seq):
    """Returns True if 'KDEL' is in the sequence."""
    if 'KDEL' in seq[-10:] or 'HDEL' in seq[-10:]:
        return True
    else:
        return False


def transmembrane_only(seq):
    c_term = seq[-10:]
    pattern = re.compile(r'[K]{2}.{2}')
    match = pattern.search(c_term)
    if match:
        return True
    else:
        return False


def nls(seq):
    monopartite = re.compile(r'[K][KR].{1}[KR]')
    bipartite = re.compile(r'[KR]{2}.{8,10}[KR]{3,5}')
    match1 = monopartite.search(seq)
    match2 = bipartite.search(seq)
    if match1 or match2:
        return True
    else:
        return False


def nucleus(seq):
    if secretory_pathway(seq) and nls(seq):
        return "Synthesized in the ER, unlikely to be in the nucleus."
    elif nls(seq) is True:
        return "Found in the nucleus"
    else:
        return "Does not contain the standard nuclear localization signal"


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
