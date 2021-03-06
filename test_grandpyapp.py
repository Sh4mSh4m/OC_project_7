import os
import unittest
import json
import requests

from unittest.mock import patch, Mock
from requests.models import Response
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import grandpyapp.views as vw
import grandpyapp.myparser as ps
import grandpyapp.myrequestapi as rq


class webClientTestCase(unittest.TestCase):
    """
    Test suite for the flask server, verifying it builds up the 
    index.html page on get requests and that the input container 
    is present
    """
    @classmethod
    def setUp(cls):
        vw.app.testing = True
        cls.driver = webdriver.Firefox()

    def test_webpage_loads(self):
        """
        Client opens up a firefox, types in the URL and checks that
        this is the right website
        """
        driver = self.driver
        self.driver.get('http://localhost:5000')
        test = driver.find_element_by_id("global")
        # test = driver.find_element_by_xpath("//p[@id='global']")
        self.assertIn("Welcome", test.text)
        # self.assertIn("Rick'n'Morty's multiverse locator", driver.title)#

    def test_webpage_input(self):
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
        self.assertIn("some text", chat_area.text)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()


class ParserTestCase(unittest.TestCase):
    """
    Test suite focusing on the various functions contributing to parsing
    user inputs and building up the server response to the POST request.
    """
    def test_msgParser(self):
        """
        Flask engine receives JSON and treats it as JSON to identify sentences
        and questions
        """
        msg = "Salut. Qui es-tu ? moi ca va"
        retour = ps.msgParser(msg)
        self.assertTrue(retour['sentences'][0] == "salut" and
                        retour['questions'][0] == " qui es-tu " and
                        retour['sentences'][1] == " moi ca va")

    def test_msgProcessor(self):
        """
        Parsing script buidls up the JSON reponse depending on:
        - assertions
        - questions
        """
        parsedBatch = {'sentences': ['salut mec',
                                     ' le tocard',
                                     '',
                                     ' une phrase3 and more'],
                       'questions': [' où est paris ']}
        result = ps.msgProcessor(parsedBatch)
        expectedMsgResponse = {'interaction': "Salut mec. S'toi le tocard. ",
                       'complement': "",
                       'keyWord': "paris ",
                       'response': ""}
        self.assertEqual(result, expectedMsgResponse)

    def test_questionsProc(self):
        # eliminates stop words and empty strings
        # builds response based on questions
        lstquestions = ['où est paris', 'tu connais paris ', '']
        msgResponse = {'interaction': "",
                       'complement': "",
                       'keyWord': "",
                       'response': ""}
        result = ps.questionsProc(lstquestions, msgResponse)
        expectedResponse = "paris paris "
        self.assertEqual(result['keyWord'], expectedResponse)

    def test_sentencesProc(self):
        # eliminates stop words and empty strings
        # builds response based on assertions
        lstsentences = ['salut ', 'le tocard', '']
        msgResponse = {'interaction': "",
                       'complement': "",
                       'response': ""}
        result = ps.sentencesProc(lstsentences, msgResponse)
        expectedResponse = "Salut mec. S'toi le tocard. "
        self.assertEqual(result['interaction'], expectedResponse)

    def test_stripStopWords(self):
        # eliminates stop words and empty strings
        phrases = ['la phrase1 avec stuff', 'une phrase2 du stuff', '']
        result = ps.stripStopWords(phrases)
        expectedResponse = [['phrase1', 'stuff'], ['phrase2', 'stuff']]
        self.assertEqual(result, expectedResponse)


class apiRequester(unittest.TestCase):
    """
    Test suite on the API request script
    """
    def test_apiWikiPedia(self):
        # mocks the requests.get call
        with patch('grandpyapp.myrequestapi.requests.get') as mocked_get:
            # mocks the response of the mocked call
            the_response = Mock(spec=Response)
            reponse = [
                        "Paris",
                        [
                          "Paris",
                          "Paris Saint-Germain Football Club",
                        ],
                        [
                          "Paris prononce..."
                        ],
                        ["links", "other link"]
                    ]
            the_response.json.return_value = reponse
            mocked_get.return_value = the_response
            self.assertEqual(rq.getJsonApiWiki("Paris"), "Paris prononce...")


if __name__ == '__main__':
    unittest.main()
