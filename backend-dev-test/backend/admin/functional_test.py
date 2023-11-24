from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest
import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        opts = webdriver.FirefoxOptions()
        opts.add_argument('--headless')
        self.browser = webdriver.Firefox(options=opts)
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('Aether Energy Utilities Demo', self.browser.title)
        header_element = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertIn('User Utility Form', header_element.text)

        user_address_box = self.browser.find_element(By.ID, 'new_user_address')
        user_consumption_box = self.browser.find_element(By.ID, 'new_user_consumption')
        user_percentage_box = self.browser.find_element(By.ID, 'new_user_percentage')
        submit_button = self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

        self.assertEqual(
            user_address_box.get_attribute('placeholder'),
            'Enter Address'
        )
        self.assertEqual(
            user_consumption_box.get_attribute('placeholder'),
            'Enter consumption (kWh)'
        )
        self.assertEqual(
            user_percentage_box.get_attribute('placeholder'),
            'Enter percentage scale (%)'
        )
        user_address_box.send_keys('Black Star #45')
        user_consumption_box.send_keys('15')
        user_percentage_box.send_keys('10')
        submit_button.click()
        time.sleep(5)

        rows = self.browser.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('Address: Black Star #45 Consumption: 15 Percentage: 10', [row.text for row in rows])
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
