from django.test import TestCase
from django.http import HttpRequest
from composition.form import ProteinForm
from composition.models import Protein
from composition.views import protein


class HomePageTest(TestCase):
    """Tests for the home page."""

    def test_home_page_renders_home_template(self):
        """Test that home page renders the 'home.html' template."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ProteinFormTest(TestCase):

    def test_protein_form_renders(self):
        """Test that '/protein/' renders the 'protein_form.html' template."""
        response = self.client.get('/protein/')
        self.assertTemplateUsed(response, 'protein_form.html')

    def test_protein_form_has_placeholder(self):
        """Tests if the form has the correct placeholder."""
        form = ProteinForm()
        self.assertIn('placeholder="Protein Name"', form.as_p())
        self.assertIn('placeholder="Protein Sequence"', form.as_p())

    def test_form_saves_only_when_necessary(self):
        """Tests the form to make sure it does not submit without an input."""
        request = HttpRequest()
        protein(request)
        self.assertEqual(Protein.objects.count(), 0)

    def test_form_can_submit_and_save_a_POST_request(self):
        """
        Tests that the form saves inputs to the database and that the entry is
        retrievible.
        """
        request = HttpRequest()
        data = {'name': 'test', 'sequence': 'MGDVEKGKKIFIMK'}
        form = ProteinForm(data)
        form.save()

        response = protein(request)

        self.assertEqual(Protein.objects.count(), 1)
        new_protein = Protein.objects.first()
        self.assertEqual(new_protein.name, 'test')
        self.assertEqual(new_protein.sequence, 'MGDVEKGKKIFIMK')

    def test_form_validation_for_blank_sequence(self):
        """
        Tests that the form is not saved if a sequence is omitted, and that the
        form throws an error telling the user to add a sequence.
        """
        data = {'name': 'test', 'sequence': ''}
        form = ProteinForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Please add a sequence.", form.errors.as_ul())

    def test_form_validation_for_blank_name(self):
        """
        Tests that the form is not saved if a name is omitted, and that the
        form throws an error telling the user to add a name.
        """
        data = {'name': '', 'sequence': 'MGDVEKGKKIFIMK'}
        form = ProteinForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Please add a name.", form.errors.as_ul())


class ProteinModelTest(TestCase):

    def test_saving_and_retrieving_proteins(self):
        """Test that the model can save and retrieve proteins."""
        first_protein = Protein()
        first_protein.name = 'test'
        first_protein.sequence = 'MGDVEKGKKIFIMK'
        first_protein.save()

        second_protein = Protein()
        second_protein.name = 'test2'
        second_protein.sequence = 'NPKKYIPGTKMIFV'
        second_protein.save()

        saved_proteins = Protein.objects.all()
        self.assertEqual(saved_proteins.count(), 2)

        first_saved_protein = Protein.objects.all()[0]
        second_saved_protein = Protein.objects.all()[1]
        self.assertEqual(first_saved_protein.name, 'test')
        self.assertEqual(second_saved_protein.name, 'test2')
