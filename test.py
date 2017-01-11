import unittest
import txodds

class TestInput(unittest.TestCase):
    def setUp(self):
        self.filename_in = 'url_list_test.txt'
        self.link_fixture = [('http//wikipedia.org',
                             '//wikimediafoundation.org/wiki/Privacy_policy',
                             'http://wikimediafoundation.org/wiki/Privacy_policy',),
                            ('https://moz.com/',
                             '/products',
                             'https://moz.com/products',),

                            ('https://moz.com/',
                             'https://google.com/',
                             'https://google.com/',),

                            ('https://moz.com/',
                             'google.com/',
                             'google.com/',),

                            ]
    def test_input(self):
        urls = txodds.file_input(self.filename_in)
        self.assertEqual(len(urls), 38)

    def test_absolute_url_creation(self):
        for fixture in self.link_fixture:
            url, link, result = fixture
            self.assertEqual(txodds.make_absolute_url(url, link), result)
