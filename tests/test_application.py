import application
import os
from redis import Redis, StrictRedis
import unittest

class TestApplication(unittest.TestCase):
    def setUp(self):
        application.app.testing = True
        self.app = application.app.test_client()
        self.students_score_cache = StrictRedis(host='localhost', port=6379, db=1)
        self.exams_cache = StrictRedis(host='localhost', port=6379, db=2)
        self.students_score_cache.hset('test_student_id', 'exam_01', '9.0')
        self.students_score_cache.hset('test_student_id', 'exam_02', '7.0')
        self.exams_cache.hset('exam_01', 'test_student_id', '9.0')
        self.exams_cache.hset('exam_01', 'test_student_id_2', '7.0')
        self.exams_cache.hset('exam_02', 'test_student_id', '7.0')

    def tearDown(self):
        self.students_score_cache.delete('test_student_id')
        self.exams_cache.delete('exam_01')
        self.exams_cache.delete('exam_02')

    def test_ping(self):
        res = self.app.get('/ping')
        self.assertEqual(res.data, '{"hello": "world"}')

    def test_student_profile(self):
        res = self.app.get('students/test_student_id')
        assert "exam_02" in res.data
        assert "7.0" in res.data
        assert "exam_01" in res.data
        assert "9.0" in res.data
        assert "8.0" in res.data

    def test_student(self):
        res = self.app.get('students')
        assert "test_student_id" in res.data

    def test_exams(self):
        res = self.app.get('exams')
        assert "exam_01" in res.data
        assert "exam_02" in res.data

    def test_exams_id(self):
        res = self.app.get('exams/exam_01')
        assert "test_student_id" in res.data
        assert "7.0" in res.data
        assert "9.0" in res.data
        assert "8.0" in res.data

if __name__ == '__main__':
    unittest.main()
