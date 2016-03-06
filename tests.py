import unittest
import json
# import urllib

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    from urllib.parse import quote
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib import urlopen
    from urllib import quote

from flask.ext.testing import LiveServerTestCase
import pyRestDb

class testServerTestCase(LiveServerTestCase):

    def create_app(self):
        app = pyRestDb.app
        app.config['TESTING'] = True
        return app

    def urlTest(self, url, response, encodeURL=False, toJSON = True):
        if encodeURL:
            url = quote(url)
        res = urlopen(self.get_server_url()+url)
        self.assertEqual(res.code, 200)
        data = res.read().decode('utf-8')
        if toJSON:
            j = json.loads(data)
            if isinstance(j, dict):
                keys = j.keys()
                if keys == None:
                    self.assertEqual(j, response)
                else:
                    for k in keys:
                        self.assertEqual(j[k], response[k])
            else:
                self.assertEqual(j, response)
        else:
            self.assertEqual(data, response)

    def generateSecret(self):
        url = quote('/generate/secret')
        res = urlopen(self.get_server_url()+url)
        self.assertEqual(res.code, 200)
        data = res.read().decode('utf-8')
        j = json.loads(data)
        return j['secret']

    def test_server_is_up_and_running(self):
        res = urlopen(self.get_server_url())
        self.assertEqual(res.code, 200)

    def test_numbers_value(self):
        self.urlTest('/set/testInt/13', {"response": "OK"})
        self.urlTest('/get/testInt', "13")
        self.urlTest('/set/testInt/-113', {"response": "OK"})
        self.urlTest('/get/testInt', '-113')
        self.urlTest('/set/testInt/-3.14', {"response": "OK"})
        self.urlTest('/get/testInt', '-3.14')

    def test_strings_value(self):
        self.urlTest('/set/testString/stringWithNoQuotes', {"response": "OK"})
        self.urlTest('/get/testString', "stringWithNoQuotes")
        self.urlTest('/set/testString/"stringWithQuotes"', {"response": "OK"})
        self.urlTest('/get/testString', "stringWithQuotes")

    def test_JSON_value(self):
        self.urlTest('/set/testJSON/{"jsonNum":3.14,"jsonStr":"pi"}', {"response": "OK"})
        self.urlTest('/get/testJSON', {"jsonNum": 3.14, "jsonStr": "pi"})
        self.urlTest('/get/testJSON/', {"jsonNum": 3.14, "jsonStr": "pi"})
        self.urlTest('/get/testJSON/jsonNum', 3.14)
        self.urlTest('/get/testJSON/jsonNum/', 3.14)
        self.urlTest('/get/testJSON/jsonStr', "pi")
        self.urlTest('/get/testJSON/jsonStr/', "pi")
        self.urlTest('/get/testJSON?pjson', '{\n    "jsonNum": 3.14,\n    "jsonStr": "pi"\n}', False, False)
        self.urlTest('/get/testJSON/?pjson', '{\n    "jsonNum": 3.14,\n    "jsonStr": "pi"\n}', False, False)

    def test_numbers_value_with_secret(self):
        secret = self.generateSecret()
        print("Secret: " + secret)
        self.urlTest('/set/testInt/13?secret='+secret, {"response": "OK"})
        self.urlTest('/get/testInt?secret='+secret, "13")
        self.urlTest('/set/testInt/-113?secret='+secret, {"response": "OK"})
        self.urlTest('/get/testInt?secret='+secret, '-113')
        self.urlTest('/set/testInt/-3.14?secret='+secret, {"response": "OK"})
        self.urlTest('/get/testInt?secret='+secret, '-3.14')

if __name__ == '__main__':
    unittest.main()