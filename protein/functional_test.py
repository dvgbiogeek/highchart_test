from selenium import webdriver
import unittest


class SetUpTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_home_page_renders(self):
        # Check out web page
        self.browser.get('http://localhost:8000')
        # You notice that the title says "Welcome"
        self.assertIn('Welcome', self.browser.title)

        # Can expand further
        # self.fail('Finish the test!')

    def test_can_enter_data_into_form(self):
        self.browser.get('http://localhost:8000')
        # Does the site "Welcome" you?
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Welcome!', body_text)

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

        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()
