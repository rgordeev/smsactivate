#!/usr/bin/env python
import unittest
import sys
from os.path import abspath, join, dirname
try:
    from StringIO import StringIO
except:
    from io import StringIO
import smsactivate
import logging
from datetime import date

# Configure logging here
full_path = lambda filename: abspath(join(dirname(__file__), filename))
# logging config
# == start
logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s',
    filename=full_path('%s.log' % str(date.today())),
    level=logging.INFO)


class SmsActivateTest(unittest.TestCase):

    def test_trivial(self):
        self.assertTrue(True)

    def test_send_request(self):
        self.assertEqual(smsactivate.get_number('bad_api_key'), 'BAD_KEY')


if __name__ == '__main__':
    unittest.main()
