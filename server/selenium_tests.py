import os
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class WebTransportSeleniumTestCase(unittest.TestCase):
    """A sample test class to show how page object works"""

    def setUp(self):
        options = Options()
        options.add_argument('--origin-to-force-quic-on=localhost:4433')
        options.add_argument('--ignore-certificate-errors-spki-list=dRdC5nAgSeEPsnMF9SvWeoPshvK0SHUp52dnbJlPmxM=')

        self.driver = webdriver.Chrome(options=options)
        html_file = os.getcwd().replace('server', '') + 'client/index.html'
        self.driver.get("file://" + html_file)

    def test_server_response(self):
        self.assertFalse('pong' in self.driver.page_source)
        connect_button = self.driver.find_element(By.ID, "connect")
        connect_button.click()
        send_button = self.driver.find_element(By.ID, "send")
        send_button.click()
        self.assertTrue('pong' in self.driver.page_source)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
