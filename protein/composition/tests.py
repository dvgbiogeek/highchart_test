from django.test import TestCase


class HomePageTest(TestCase):
    """Tests for the home page."""

    def test_home_page_renders_home_template(self):
        """Test that home page renders the 'home.html' template."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


# class ProteinFormTest(TestCase):
