import application
import os
from redis import Redis, StrictRedis
import unittest

from application.database import Database
from application.application import average_score


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        application.app.testing = True
        self.app = application.app.test_client()
        self.students_score_cache = Database(index=1, redis_host='localhost')
        self.exams_cache = Database(index=2, redis_host='localhost')

        self.students_score_cache.save_entry('test_student_id', 'exam_01', '9.0')
        self.students_score_cache.save_entry('test_student_id', 'exam_02', '7.0')
        self.exams_cache.save_entry('exam_01', 'test_student_id', '9.0')
        self.exams_cache.save_entry('exam_01', 'test_student_id_2', '7.0')
        self.exams_cache.save_entry('exam_02', 'test_student_id', '7.0')

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

    def test_student_profile_with_param_filter(self):
        res = self.app.get('students/test_student_id?exam_id=exam_01')
        assert "exam_01" in res.data
        assert "9.0" in res.data
        assert "8.0" in res.data # average_score
        assert "exam_02" not in res.data

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
        assert "test_student_id_2" in res.data
        assert "7.0" in res.data
        assert "9.0" in res.data
        assert "8.0" in res.data

    def test_exams_id_with_param(self):
        res = self.app.get('exams/exam_01?student_name=test_student_id')
        assert "test_student_id" in res.data
        assert "9.0" in res.data
        assert "test_student_id_2" not in res.data


class UnitTest(unittest.TestCase):
    def test_average_score(self):
        entries = {
            'exam_01': 9.0,
            'exam_02': 7.0,
            'exam_03': 8.0
        }
        self.assertEqual(average_score(entries), 8.0)

if __name__ == '__main__':
    unittest.main()
