import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book

class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgres:///{}".format( self.database_name)
        setup_db(self.app, self.database_path)

        self.new_book_dict = {
            'title': 'Anansi Boys',
            'author': 'Neil Gaiman',
            'rating': 5
        }
        
        self.new_book = None

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.new_book = Book(**self.new_book_dict)
            self.new_book.insert()
    
    def tearDown(self):
        """Executed after reach test"""
        books = Book.query.all()
        for book in books:
            book.delete()
        

# @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
#        You can feel free to write additional tests for nuanced functionality,
#        Such as adding a book without a rating, etc. 
#        Since there are four routes currently, you should have at least eight tests. 
# Optional: Update the book information in setUp to make the test database your own! 
    def test_get_books(self):
        res = self.client().get('/books')

        self.assertEqual(res.status_code, 200)
        book_json = res.get_json()
        self.assertEqual(book_json.get("total_books"), 1)
        self.assertEqual(book_json.get("books")[0].get("title"), "Anansi Boys")
        

    def test_add_book(self):
        new_book_dict = {
                    'title': 'The Stand',
                    'author': 'Stephen King',
                    'rating': 5
                }
        
        res = self.client().post('/books', json=new_book_dict)
        self.assertEqual(res.status_code, 200)
        
        book_json = res.get_json()
        self.assertEqual(book_json.get("total_books"), 2)      


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()