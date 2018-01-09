import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import views


class GrandPyTestCase(unittest.TestCase):

    def setUp(self):
        views.app.testing = True
        #self.app = views.app.test_client()
        self.driver = webdriver.Firefox()

#    def test_webpage_content(self):
#        """
#        Test that the flask app launches and that the client can access
#        it and view the content of the header
#        """
#        rv = self.app.get('/')
#        assert b"Welcome to Rick'n'Morty's multiverse locator" in rv.data

    def test_webpage_loads(self):
        """
        Client opens up a firefox, types in the URL and checks that
        this is the right website
        """
        driver = self.driver
        self.driver.get('http://localhost:5000')
        test = driver.find_element_by_id("caca")
#        test = driver.find_element_by_xpath("//p[@id='caca']")
        self.assertIn("pipicaca", test.text)
#        self.assertIn("Rick'n'Morty's multiverse locator", driver.title)

    def test_webpage_input(self):
        """
        Client opens up a firefox, locates the input field, enter text.
        text appears in the display area
        """
        driver = self.driver
        chat_input = driver.find_element_by_xpath("//input[1]")
        chat_input.clear()
        chat_input.send_keys('some text')
        chat_area = driver.find_element_by_id("chat_area")
        self.assertIn("some text", chat_area.text)


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
