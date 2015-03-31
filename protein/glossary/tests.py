from django.test import TestCase
from glossary.models import Glossary


class GlossaryViewTest(TestCase):

    def test_glossary_view_renders_template(self):
        """Test that '/glossary/' renders 'glossary.html'."""
        response = self.client.get('/glossary/')
        self.assertTemplateUsed(response, 'glossary.html')


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
