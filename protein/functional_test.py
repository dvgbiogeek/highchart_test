from selenium import webdriver
import unittest


class SetUpTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def find_text_in_body(self, find_text):
        """Scans contents of body for text."""
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn(find_text, body_text)

    def test_home_page_renders(self):
        # Check out web page
        self.browser.get('http://localhost:8000')
        # You notice that the title says "Welcome"
        self.assertIn('Welcome', self.browser.title)

        # Can expand further
        # self.fail('Finish the test!')

    def test_can_enter_data_into_form(self):
        """Tests form on home page."""
        self.browser.get('http://localhost:8000')
        # Does the site "Welcome" you?
        self.find_text_in_body('Welcome!')

        # After the welcome there is a form to enter content
        name_input = self.browser.find_element_by_id('id_name_input')
        self.assertEqual(name_input.get_attribute('placeholder'),
                         'Protein Name')
        name_input.send_keys('Cytochrome c')

        sequence_input = self.browser.find_element_by_id('id_sequence')
        self.assertEqual(sequence_input.get_attribute('placeholder'),
                         'Protein Sequence')
        sequence_input.send_keys('MGDVEKGKKIFIMKCSQCHTVEKGGKHKT')
        # submit the form
        submit_button = self.browser.find_element_by_id('id_submit')
        submit_button.click()

        # Need to add more in terms of resolving submission of the form
        # self.fail('Finish the test!')

    def test_can_enter_data_into_django_form(self):
        """Tests form on home page."""
        self.browser.get('http://localhost:8000/protein')
        # Does the site "Welcome" you?
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
        submit_button = self.browser.find_element_by_id('id_submit')
        submit_button.click()

        # form redirects to url tied to id
        current_url = self.browser.current_url
        self.assertRegex(current_url, 'protein/.+')

        self.find_text_in_body('name')

        # self.fail('Finish the test!')

    def test_cannot_add_empty_entries(self):
        # some validation effort to make sure empty entries throw an error
        # go to site (focus on protein route)
        self.browser.get('http://localhost:8000/protein')

        # Add a name, but no sequence
        name_input = self.browser.find_element_by_id('id_name')
        name_input.send_keys('Cytochrome c')
        submit_button = self.browser.find_element_by_id('id_submit')
        submit_button.click()

        # An error message occurs saying a sequence is needed to proceed
        self.find_text_in_body('Please add a name and sequence.')

        # The page does not redirect to the success page
        current_url = self.browser.current_url
        self.assertEqual(current_url, 'http://localhost:8000/protein/')

        # self.fail('More test!')


if __name__ == '__main__':
    unittest.main()
