import unittest

from main import find_in_text, get_url_soup, KEYWORDS, URL
from bs4 import BeautifulSoup
from fake_headers import Headers

class TestMain(unittest.TestCase):
    
    def setUp(self):
        headers = Headers(browser="chrome", os="win", headers=True)
        self.header = headers.generate()
    
    def tearDown(self):
        del self.header
    
    def test_find_in_text_true(self):
        text = "Это текст о дизайне и фото"
        res = find_in_text(KEYWORDS, text)
        self.assertTrue(res)
        
    def test_find_in_text_false(self):
        text = "Это простой текст о чем то ..."
        res = find_in_text(KEYWORDS, text)
        self.assertFalse(res)
        
    def test_find_in_empty_text_false(self):
        text = ""
        res = find_in_text(KEYWORDS, text)
        self.assertFalse(res)
        
    def test_url_connection_true(self):
        soup = get_url_soup(URL, self.header)
        self.assertIsInstance(soup, BeautifulSoup)
        
    def test_url_connection_false(self):
        soup = get_url_soup('https://httpbin.org/ererw', self.header)
        self.assertIsNone(soup)