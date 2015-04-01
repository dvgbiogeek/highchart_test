from django.test import TestCase
from django.http import HttpRequest
from glossary.models import Glossary
from glossary.views import new
from glossary.form import GlossaryForm


class GlossaryViewTest(TestCase):

    def test_glossary_view_renders_template(self):
        """Test that '/glossary/' renders 'glossary.html'."""
        response = self.client.get('/glossary/')
        self.assertTemplateUsed(response, 'glossary.html')


class GlossaryFormTest(TestCase):

    def test_glossary_form_renders(self):
        """Test that '/glossary/new/' renders the 'glossary_form.html' template."""
        response = self.client.get('/glossary/new/')
        self.assertTemplateUsed(response, 'glossary_form.html')

    def test_protein_form_has_placeholder(self):
        """Tests if the form has the correct placeholder."""
        form = GlossaryForm()
        self.assertIn('placeholder="New term"', form.as_p())
        self.assertIn('placeholder="Term definition"', form.as_p())
        self.assertIn('placeholder="Reference"', form.as_p())

    def test_form_saves_only_when_necessary(self):
        """Tests the form to make sure it does not submit without an input."""
        request = HttpRequest()
        new(request)
        self.assertEqual(Glossary.objects.count(), 0)

    def test_form_can_submit_and_save_a_POST_request(self):
        """
        Tests that the form saves inputs to the database and that the entry is
        retrievible.
        """
        request = HttpRequest()
        data = {'term': 'test', 'definition': 'definition', 'reference': 'yep'}
        form = GlossaryForm(data)
        form.save()

        response = new(request)

        self.assertEqual(Glossary.objects.count(), 1)
        new_term = Glossary.objects.first()
        self.assertEqual(new_term.term, 'test')
        self.assertEqual(new_term.definition, 'definition')
        self.assertEqual(new_term.reference, 'yep')

    def test_form_validation_for_blank_reference(self):
        """
        Tests that the form is not saved if a reference is omitted, and that
        the form throws an error telling the user to add a sequence.
        """
        data = {'term': 'test', 'definition': 'definition', 'reference': ''}
        form = GlossaryForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "A reference is required.", form.errors.as_ul())

    def test_form_validation_for_blank_definition(self):
        """
        Tests that the form is not saved if a reference is omitted, and that
        the form throws an error telling the user to add a sequence.
        """
        data = {'term': 'test', 'definition': '', 'reference': 'yep'}
        form = GlossaryForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Please add a definition to the glossary term.", form.errors.as_ul())

    def test_form_validation_for_blank_term(self):
        """
        Tests that the form is not saved if a reference is omitted, and that
        the form throws an error telling the user to add a sequence.
        """
        data = {'term': '', 'definition': 'definition', 'reference': 'yep'}
        form = GlossaryForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Please add a glossary term.", form.errors.as_ul())


class GlossaryModelTest(TestCase):

    def test_saving_and_retrieving_glossary_entries(self):
        """Test that the model can save and retrieve proteins."""
        first_entry = Glossary()
        first_entry.term = 'test'
        first_entry.definition = 'definition'
        first_entry.reference = 'ref'
        first_entry.save()

        second_entry = Glossary()
        second_entry.term = 'test2'
        second_entry.definition = 'definition2'
        second_entry.reference = 'ref2'
        second_entry.save()

        saved_terms = Glossary.objects.all()
        self.assertEqual(saved_terms.count(), 2)

        first_saved_term = Glossary.objects.all()[0]
        second_saved_term = Glossary.objects.all()[1]
        self.assertEqual(first_saved_term.term, 'test')
        self.assertEqual(second_saved_term.term, 'test2')
