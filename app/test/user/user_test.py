import unittest
import os


def test_user_con(self):

    rv = self.app.get('/')
    assert 'No entries here so far' in rv.data

if __name__ == '__main__':
    unittest.main()