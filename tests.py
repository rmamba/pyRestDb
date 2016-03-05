import unittest
import urllib

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

from flask.ext.testing import LiveServerTestCase
import pyRestDb

class testServerTestCase(LiveServerTestCase):

    def create_app(self):
        app = pyRestDb.app
        app.config['TESTING'] = True
        return app

    def urlTest(self, url, response, encode=True):
        if encode:
            url = urllib.quote(url)
        res = urlopen(self.get_server_url()+url)
        self.assertEqual(res.read(), response)
        self.assertEqual(res.code, 200)

    def test_server_is_up_and_running(self):
        res = urlopen(self.get_server_url())
        self.assertEqual(res.code, 200)

    def test_numbers_value(self):
        self.urlTest('/set/testInt/13', '{"response": "OK"}')
        self.urlTest('/get/testInt', '"13"')
        self.urlTest('/set/testInt/-113', '{"response": "OK"}')
        self.urlTest('/get/testInt', '"-113"')
        self.urlTest('/set/testInt/-3.14', '{"response": "OK"}')
        self.urlTest('/get/testInt', '"-3.14"')

    def test_strings_value(self):
        self.urlTest('/set/testString/stringWithNoQuotes', '{"response": "OK"}')
        self.urlTest('/get/testString', '"stringWithNoQuotes"')
        self.urlTest('/set/testString/"stringWithQuotes"', '{"response": "OK"}')
        self.urlTest('/get/testString', '"stringWithQuotes"')

    def test_JSON_value(self):
        self.urlTest('/set/testJSON/{"jsonNum":3.14,"jsonStr":"pi"}', '{"response": "OK"}')
        self.urlTest('/get/testJSON', '{"jsonNum": 3.14, "jsonStr": "pi"}')
        self.urlTest('/get/testJSON?pjson', '{"jsonNum": 3.14, "jsonStr": "pi"}')
        self.urlTest('/get/testJSON/?pjson', '{"jsonNum": 3.14, "jsonStr": "pi"}')

if __name__ == '__main__':
    unittest.main()