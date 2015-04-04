from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from account.form import UserForm, CreateNewForm
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


class LoginViewTest(TestCase):

    def test_new_user_view_renders_template(self):
        """Test that '/new_user/' renders 'new_user.html'."""
        response = self.client.get('/new_user/')
        self.assertTemplateUsed(response, 'new_user.html')


class NewUserFormTest(TestCase):
    fixtures = ['user.json']

    def test_new_user_form_has_placeholders(self):
        """Tests if the form has the correct placeholder."""
        form = CreateNewForm()
        self.assertIn('placeholder="Create a username"', form.as_p())
        self.assertIn('placeholder="Enter password"', form.as_p())
        self.assertIn('placeholder="Enter email address"', form.as_p())
        self.assertIn('placeholder="Confirm password"', form.as_p())

    def test_successful_login_results_in_redirect(self):
        """
        Tests that a successful post request for login results in a redirect.
        """
        c = Client()
        data = {'username': 'dan', 'email': 'd@g.com',
                'password1': 'bunny', 'password2': 'bunny'}
        response = c.post('/new_user/', data)
        print(response.content.decode())
        self.assertRedirects(response, '/login/')

    def test_login_failure_redisplays_the_form(self):
        """
        Tests that wrong login does not redirect and displays an error message.
        """
        c = Client()
        data = {'username': 'dan', 'email': 'd@g.com',
                'password1': 'bunny', 'password2': 'bun'}
        response = c.post('/new_user/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('The two password fields did not match.',
                response.content.decode())

    def test_login_failure_redisplays_the_form_and_displays_error(self):
        """
        Tests that wrong login does not redirect and displays an error message.
        """
        c = Client()
        data = {'username': 'danielle', 'email': 'd@g.com',
                'password1': 'bunny', 'password2': 'bunny'}
        response = c.post('/new_user/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('A user with this username already exists.',
                response.content.decode())
