from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from account.form import UserForm
from account.views import user_login
User = get_user_model()


class LoginViewTest(TestCase):

    def test_login_view_renders_template(self):
        """Test that '/login/' renders 'login.html'."""
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'login.html')


class LoginFormTest(TestCase):

    fixtures = ['user.json']

    def test_login_form_has_placeholders(self):
        """Tests if the form has the correct placeholder."""
        form = UserForm()
        self.assertIn('placeholder="Enter username"', form.as_p())
        self.assertIn('placeholder="Enter password"', form.as_p())

    def test_successful_login_results_in_redirect(self):
        """
        Tests that a successful post request for login results in a redirect.
        """
        c = Client()
        data = {'username': 'danielle', 'password': 'bunny'}
        response = c.post('/login/', data)
        print(response.content.decode())
        self.assertRedirects(response, '/')

    def test_login_failure_redisplays_the_form(self):
        """
        Tests that wrong login does not redirect and displays an error message.
        """
        c = Client()
        data = {'username': 'danielle', 'password': 'bun'}
        response = c.post('/login/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please enter a correct username and password.',
            response.content.decode())
