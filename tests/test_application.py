import application
import os
from redis import Redis, StrictRedis
import unittest

class TestApplication(unittest.TestCase):
    def setUp(self):
        application.app.testing = True
        self.app = application.app.test_client()
        self.students_score_cache = StrictRedis(host='localhost', port=6379, db=1)
        self.students_score_cache.hset('test_student_id', 'exam_01', '9.0')
        self.students_score_cache.hset('test_student_id', 'exam_02', '7.0')

    def tearDown(self):
        self.students_score_cache.delete('test_student_id')

    def test_ping(self):
        res = self.app.get('/ping')
        self.assertEqual(res.data, '{"hello": "world"}')

    def test_student_profile(self):
        res = self.app.get('students/test_student_id')
        assert "exam_02" in res.data
        assert "7.0" in res.data

if __name__ == '__main__':
    unittest.main()
