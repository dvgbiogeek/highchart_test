from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest


class BaseFunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def find_text_in_body(self, find_text):
        """Scans contents of body for text."""
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn(find_text, body_text)

    def click_button(self, button_id):
        button = self.browser.find_element_by_id(button_id)
        button.click()

    def go_to_home_page(self):
        self.browser.get(self.live_server_url)

    def go_to_protein_form(self):
        self.go_to_home_page()
        link = self.browser.find_element_by_link_text(
                "Proteins into Components")
        link.click()

    def go_to_glossary(self):
        self.go_to_home_page()
        link = self.browser.find_element_by_link_text("Protein Glossary")
        link.click()

    def check_at_desired_url(self, url_extension):
        current_url = self.browser.current_url
        self.assertEqual(current_url, self.live_server_url + url_extension)

    def enter_input(self, input_id, text):
        find_element = self.browser.find_element_by_id(input_id)
        find_element.send_keys(text)


class ProteinCompositionTest(BaseFunctionalTest):
    """Functional test for the Composition App."""
    fixtures = ['protein.json']

    def test_can_enter_data_into_form(self):
        """Tests form on protein page."""
        self.go_to_home_page()
        # Does the site "Welcome" you?
        self.find_text_in_body('Welcome!')

        # The page shows a list of links. Well, one...
        self.go_to_protein_form()

        # clicking the link redirects to the protein form
        self.check_at_desired_url('/protein/')
        self.find_text_in_body('Protein Form')

        # After the welcome there is a form to enter content
        name_input = self.browser.find_element_by_id('id_name')
        self.assertEqual(name_input.get_attribute('placeholder'),
                         'Protein Name')
        name_input.send_keys('Cytochrome c')

        sequence_input = self.browser.find_element_by_id('id_sequence')
        self.assertEqual(sequence_input.get_attribute('placeholder'),
                         'Protein Sequence')
        sequence_input.send_keys('MGDVEKGKKIFIMKCSQCHTVEKGGKHKT')
        # submit the form
        self.click_button('id_submit')

        # form redirects to url tied to id
        current_url = self.browser.current_url
        self.assertRegex(current_url, 'composition/.+')

        self.find_text_in_body('Cytochrome c')

    def test_cannot_add_empty_sequence(self):
        """
        Test for basic validation that the form does not submit without a
        sequence.
        """
        # some validation effort to make sure empty entries throw an error
        # go to site (focus on protein route)
        self.go_to_protein_form()

        # Add a name, but no sequence
        self.enter_input('id_name', 'Cytochrome c')
        self.click_button('id_submit')

        # An error message occurs saying a sequence is needed to proceed
        self.find_text_in_body('Please add a sequence.')

        # The page does not redirect to the success page
        self.check_at_desired_url('/protein/')

    def test_cannot_add_empty_name(self):
        """
        Test for basic validation that the form does not submit without a name.
        """
        # some validation effort to make sure empty entries throw an error
        # go to site (focus on protein route)
        self.go_to_protein_form()

        # Add a sequence, but no name
        self.enter_input('id_sequence', 'MGDVEKGKKIFIMKCSQCHTVEKGGKHKT')
        self.click_button('id_submit')

        # An error message occurs saying a sequence is needed to proceed
        self.find_text_in_body('Please add a name.')

        # The page does not redirect to the success page
        self.check_at_desired_url('/protein/')

    def test_can_view_protein_examples(self):
        """
        Test that user can view data from proteins already in the database.
        """
        # Go to site (focus on protein route)
        self.go_to_protein_form()

        # Find and click on link
        link = self.browser.find_element_by_link_text('cytochrome c oxidase subunit 4 isoform 1')
        link.click()

        # The clicking on the link directs to a different url and contains the
        # word 'superoxide'
        current_url = self.browser.current_url
        self.assertRegex(current_url, 'composition/.+')
        self.find_text_in_body('cytochrome c')

        # It displays the amino acid composition graph
        self.click_button('button_comp')
        self.find_text_in_body('Amino Acid Composition')

        # It displays the percent graph
        self.click_button('button_percent')
        self.find_text_in_body('Amino Acid Percent')


class GlossaryTest(BaseFunctionalTest):
    """Functional Tests for the Glossary App."""
    fixtures = ['glossary.json', 'user.json']

    def test_view_glossary_and_add_content(self):
        """Test if user can view glossary objects."""
        # Go to the home page and click on the glossary link
        self.go_to_glossary()

        # check at proper url and text matches an entry in the glossary model
        self.check_at_desired_url('/glossary/')
        self.find_text_in_body('globular string of amino acids')

        # Click on link for adding new content
        new_link = self.browser.find_element_by_link_text('New glossary entry')
        new_link.click()

        # Login is required for adding new entries to the glossary
        self.check_at_desired_url('/login/?next=/glossary/new/')
        self.enter_input('id_username', 'danielle')
        self.enter_input('id_password', 'bunny')
        self.click_button('id_submit')
        self.check_at_desired_url('/glossary/new/')
        self.find_text_in_body('Glossary Form')

        # Check for Markdown Key
        self.find_text_in_body('[More here]')

        # Add glossary content
        self.enter_input('id_term', 'term')
        self.enter_input('id_definition', 'definition')
        self.enter_input('id_reference', 'reference')
        self.click_button('id_submit')

        # Check the page redirects after submitting the form and contains the
        # submitted form's content
        self.check_at_desired_url('/glossary/')
        self.find_text_in_body('term')

    def test_invalid_entry_triggers_error(self):
        """Test that an invalid form entry produces an error."""
        self.go_to_glossary()
        self.browser.find_element_by_link_text('New glossary entry').click()

        # Login is required for adding new entries to the glossary
        self.check_at_desired_url('/login/?next=/glossary/new/')
        self.enter_input('id_username', 'danielle')
        self.enter_input('id_password', 'bunny')
        self.click_button('id_submit')

        # enter term, but no definition or reference
        self.enter_input('id_term', 'term')
        self.click_button('id_submit')

        self.check_at_desired_url('/glossary/new/')
        self.find_text_in_body('Please add a definition to the glossary term')
        self.find_text_in_body('A reference is required')


class LoginTest(BaseFunctionalTest):
    """Functional tests for accounts."""
    fixtures = ['user.json']

    def test_login_and_logout(self):
        """Test that logs in a user then logs out."""
        self.go_to_home_page()
        self.browser.find_element_by_link_text('Sign In').click()

        # Login to site
        self.check_at_desired_url('/login/?next=')
        self.enter_input('id_username', 'danielle')
        self.enter_input('id_password', 'bunny')
        self.click_button('id_submit')

        # Check login was successful.
        self.find_text_in_body('Logout')
        self.check_at_desired_url('/')

        self.browser.find_element_by_link_text('Logout').click()
        self.find_text_in_body('Sign In')

    def test_bad_password_fails_login(self):
        """Test that the proper password is required to log in."""
        self.go_to_home_page()
        self.browser.find_element_by_link_text('Sign In').click()

        # Enter wrong password displays an error and fails to login.
        self.enter_input('id_username', 'danielle')
        self.enter_input('id_password', 'bun')
        self.click_button('id_submit')
        self.find_text_in_body('Sign In')
        self.find_text_in_body('Please enter a correct username and password.')

        # Form maintains username, only add password. Then logs in with correct
        # password.
        pass_input = self.browser.find_element_by_id('id_password')
        self.assertEqual(pass_input.get_attribute('placeholder'),
                         'Enter password')
        self.enter_input('id_password', 'bunny')
        self.click_button('id_submit')
        self.find_text_in_body('Logout')
        self.check_at_desired_url('/')
