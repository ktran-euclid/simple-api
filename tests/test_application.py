import flaskr
import os
import unittest

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.app = FlaskAPI(__name__)

    def test_students(self):
        res = self.app.get('/students')
        import pdb; pdb.set_trace()
        

if __name__ == '__main__':
    unittest.main()
