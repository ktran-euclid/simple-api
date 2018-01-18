import application
import os
from redis import Redis, StrictRedis
import unittest

class TestApplication(unittest.TestCase):
    def setUp(self):
        application.app.testing = True
        self.app = application.app.test_client()

    def test_ping(self):
        res = self.app.get('/ping')
        self.assertEqual(res.data, '{"hello": "world"}')

    def test_student_profile(self):
        students_score_cache = StrictRedis(host='localhost', port=6379, db=1)
        students_score_cache.hset('test_student_id', 'exam_01', '9.0')
        res = self.app.get('students/test_student_id')
        self.assertEqual(res.data, '{"exam_01": "9.0"}')

if __name__ == '__main__':
    unittest.main()
