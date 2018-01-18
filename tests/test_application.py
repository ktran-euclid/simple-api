import application
import os
import unittest

class TestApplication(unittest.TestCase):
    def setUp(self):
        application.app.testing = True
        self.app = application.app.test_client()

    def test_students(self):
        res = self.app.get('/students')
        self.assertEqual(res.data, '{"hello": "world"}')


if __name__ == '__main__':
    unittest.main()
