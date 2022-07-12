import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.user_name = 'postgres'
        self.password = 'postp'
        self.host = 'localhost:5432'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.user_name, self.password, self.host, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        """Test get categories """
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'],True)
        self.assertEqual(res.json['categories']['1'],"Science")

    def test_get_questions(self):
        """Test get questions 200 response"""
        res = self.client().get('/questions?page=1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'],True)

    def test_get_questions_wrong_page(self):
        """Test get questions 404 response"""
        res = self.client().get('/questions?page=99999')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json['success'],False)

    def test_get_questions_text_page(self):
        """Test get questions 400 response"""
        res = self.client().get('/questions?page=lol')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['success'],False)

    def test_delete_question(self):
        """Test delete questions 200 response"""
        question = Question.query.order_by(Question.id.desc()).first()
        res = self.client().delete('/questions/'+str(question.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'],True)


    def test_delete_nonexistent_question(self):
        """Test delete questions 400 response"""
        res = self.client().delete('/questions/0')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['success'],False)

    def test_post_question(self):
        """Test post questions 200 response"""
        res = self.client().post('/questions', 
            json={
                "question":"What is the name of the Galaxy we live in?",
                "answer":"The Milky Way galaxy",
                "difficulty":2,
                "category": 1
            })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'],True)
    
    def test_post_question_alphanumeric_difficulty(self):
        """Test post questions 400 response (incorrect difficulty)"""
        res = self.client().post('/questions', 
            json={
                "question":"Is Darth Vader related to Anakin Skywalker?",
                "answer":"Yes",
                "difficulty":"lol",
                "category":5
            })
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['success'],False)

    def test_post_question_nonexistent_category(self):
        """Test post questions 400 response (incorrect difficulty)"""
        res = self.client().post('/questions', 
            json={
                "question":"Is Darth Vader related to Anakin Skywalker?",
                "answer":"Yes",
                "difficulty":3,
                "category":0
            })
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['success'],False)

    def test_post_question_search(self):
        """Test post questions 200 response"""
        res = self.client().post('/questions/search', 
            json={
                "searchTerm": "HeMaToLoGy"
            })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'],True)

    def test_post_question_search_no_result(self):
        """Test post questions 404 response"""
        res = self.client().post('/questions/search', 
            json={
                "searchTerm": "HeMaToLoGy24567"
            })
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json['success'],False)

    def test_post_quizzes_with_only_1_question_left(self):
        """Test post quizzes which can return only 1 question with 200 response"""
        res = self.client().post('/quizzes', 
            json={
                "previous_questions":[14, 15],
                "quiz_category": {"type": "Geography", "id": "3"}
            })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'],True)
        print("LOLOLOL",res.json)
        self.assertEqual(res.json['question']['id'],13)

    def test_post_quizzes_with_no_question_left(self):
        """Test post quizzes which can return no new question with 200 response"""
        res = self.client().post('/quizzes', 
            json={
                "previous_questions":[14, 13, 15],
                "quiz_category": {"type": "Geography", "id": "3"}
            })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'],True)
        self.assertEqual(res.json['question'],False)
    
    def test_post_quizzes_with_incorrect_category_id(self):
        """Test post quizzes which can return 400 response"""
        res = self.client().post('/quizzes', 
            json={
                "previous_questions":[14, 13, 15],
                "quiz_category": {"type": "Geography", "id": "lol"}
            })
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['success'],False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()