from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest


class SetUpTest(StaticLiveServerTestCase):

    fixtures = ['protein.json']

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
        link = self.browser.find_element_by_link_text(
                "Proteins into Components")
        link.click()

    def test_can_enter_data_into_form(self):
        """Tests form on home page."""
        self.go_to_home_page()
        # Does the site "Welcome" you?
        self.find_text_in_body('Welcome!')

        # The page shows a list of links. Well, one...
        self.go_to_protein_form()

        # clicking the link redirects to the protein form
        current_url = self.browser.current_url
        self.assertEqual(current_url, self.live_server_url + '/protein/')
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
        # self.fail('Finish the test!')

    def test_cannot_add_empty_sequence(self):
        # some validation effort to make sure empty entries throw an error
        # go to site (focus on protein route)
        self.go_to_home_page()
        self.go_to_protein_form()

        # Add a name, but no sequence
        name_input = self.browser.find_element_by_id('id_name')
        name_input.send_keys('Cytochrome c')
        self.click_button('id_submit')

        # An error message occurs saying a sequence is needed to proceed
        self.find_text_in_body('Please add a sequence.')

        # The page does not redirect to the success page
        current_url = self.browser.current_url
        self.assertEqual(current_url, self.live_server_url + '/protein/')

        # self.fail('More test!')

    def test_cannot_add_empty_name(self):
        # some validation effort to make sure empty entries throw an error
        # go to site (focus on protein route)
        self.go_to_home_page()
        self.go_to_protein_form()

        # Add a sequence, but no name
        sequence_input = self.browser.find_element_by_id('id_sequence')
        sequence_input.send_keys('MGDVEKGKKIFIMKCSQCHTVEKGGKHKT')
        self.click_button('id_submit')

        # An error message occurs saying a sequence is needed to proceed
        self.find_text_in_body('Please add a name.')

        # The page does not redirect to the success page
        current_url = self.browser.current_url
        self.assertEqual(current_url, self.live_server_url + '/protein/')

    def test_can_view_protein_examples(self):
        # Go to site (focus on protein route)
        self.go_to_home_page()
        self.go_to_protein_form()

        # Find and click on link
        link = self.browser.find_element_by_link_text('cytochrome c')
        link.click()

        # The clicking on the link directs to a different url and contains the
        # word 'superoxide'
        current_url = self.browser.current_url
        self.assertRegex(current_url, 'composition/.+')
        self.find_text_in_body('cytochrome c')
