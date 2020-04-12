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
        self.database_path = "postgres:///{}".format(self.database_name)
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
        res = self.client().get("/categories")
        
        self.assertEqual(res.status_code, 200)
        
        cat_json = res.get_json()
        self.assertTrue(cat_json.get("success"), "Success should be present in the response")
        
        cat_dict = cat_json.get("categories")
        self.assertEqual(6, len(cat_dict))
        expected = {
            "1":"Science",
            "2":"Art",
            "3":"Geography",
            "4":"History",
            "5":"Entertainment",
            "6":"Sports"}
        self.assertEqual(expected, cat_dict)
        
        
    def test_method_not_allowed_categories(self):
        methods = ["POST", "PATCH", "DELETE", "PUT"]
        url = "/categories"
        for method in methods:
            res = getattr(self.client(), method.lower())(url)            
            self.assertEqual(res.status_code, 405, f"Expecting method not allowed error (405) for method {method}")
            self.assertTrue(res.get_json().get("error"), "Error attribute should be present in response")
            self.assertFalse(res.get_json().get("success"), "Success attribute should be present in response and should be false")
        

    def test_get_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        self.assertEqual(res.status_code, 200)
        myjson = res.get_json()
        self.assertTrue(myjson.get("categories"), "Categories key should exist in the response")
        self.assertTrue(myjson.get("success"))
        self.assertEqual(1, myjson.get("current_category"), "Current category should match the category passed in the url")
        self.assertEqual(3, myjson.get("total_questions"))
        self.assertEqual(3, len(myjson.get("questions")))
        
        
    def test_get_questions_for_nonexistant_category(self):
        res = self.client().get("/categories/999/questions")
        self.assertEqual(res.status_code, 404, "Expecting page not found error (404) for a non-existent category ")
        self.assertTrue(res.get_json().get("error"), "Error attribute should be present in response")
        self.assertFalse(res.get_json().get("success"), "Success attribute should be present in response and should be false")

    
    def test_bad_url(self):
        res = self.client().get("/bad-url")
        self.assertEqual(res.status_code, 404, "Expecting page not found error (404) for a non-existent category ")
        self.assertTrue(res.get_json().get("error"), "Error attribute should be present in response")
        self.assertFalse(res.get_json().get("success"), "Success attribute should be present in response and should be false")

        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()