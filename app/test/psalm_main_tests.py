import os
#import psalm_main
import unittest
from app.models.user import customer
# import psalm_main
import unittest

import os

from app.models.user import customer


class PsalmMainTestCase(unittest.TestCase):

    def setUp(self):
        customer.app.config['TESTING'] = True
        self.app = customer.app.test_client()
        customer.reg_customer_info()

    def tearDown(self):
        os.unlink(customer.app)

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

if __name__ == '__main__':
    unittest.main()
