import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import grandpyapp.views
import grandpyapp.myparser as ps
import grandpyapp.myrequestApi as rq

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
#        assert b"Welcome to Rick'n'Morty's multiverse locator" in rv.data#

    def teXt_webpage_loads(self):
        """
        Client opens up a firefox, types in the URL and checks that
        this is the right website
        """
        driver = self.driver
        self.driver.get('http://localhost:5000')
        test = driver.find_element_by_id("global")
#        test = driver.find_element_by_xpath("//p[@id='caca']")
        self.assertIn("Welcome", test.text)
#        self.assertIn("Rick'n'Morty's multiverse locator", driver.title)#

    def teXt_webpage_input(self):
        """
        Client opens up a firefox, locates the input field, enter text.
        text appears in the display area
        """
        driver = self.driver
        self.driver.get('http://localhost:5000')
        chat_input = driver.find_element_by_xpath("//textarea[@id='dialogInput']")
        chat_input.clear()
        chat_input.send_keys('some text')
        chat_input.send_keys(Keys.RETURN)
        chat_area = driver.find_element_by_id("dialogDisplay")
        self.assertIn("some text", chat_area.text)#

# Data input control, maek sure we only have text input#
    def tearDown(self):
        self.driver.quit()


class ParserTestCase(unittest.TestCase):

    def test_msgParser(self):
        """
        Flask engine receives JSON and treats it as JSON to identify sentences
        and questions
        """
        msg = "Salut. Qui es-tu ? moi ca va"
        retour = ps.msgParser(msg)
        print(retour)
        self.assertTrue(retour['sentences'][0] == "salut" and
                        retour['questions'][0] == " qui es-tu " and
                        retour['sentences'][1] == " moi ca va")

    def test_msgProcessor(self):
        pass


class apiRequester(unittest.TestCase):

    def test_apiWikiPedia(self):
        result = [
                    "Paris",
                    [
                      "Paris",
                      "Paris Saint-Germain Football Club",
                      "Paris Hilton",
                      "Paris-Gare-de-Lyon",
                      "Paris Football Club",
                      "Paris Match",
                      "Paris Saint-Germain Handball",
                      "Paris Saint-Germain Football Club (féminines)",
                      "Paris-Saclay",
                      "Paris sous l'occupation allemande"
                    ],
                    [
                      "Paris (prononcé [pa.ʁi] ) est la capitale de la France. Elle se situe au cœur d'un vaste bassin sédimentaire aux sols fertiles et au climat tempéré, le bassin parisien, sur une boucle de la Seine, entre les confluents de celle-ci avec la Marne et l'Oise."
                    ]
                ]
        pass


if __name__ == '__main__':
    unittest.main()
