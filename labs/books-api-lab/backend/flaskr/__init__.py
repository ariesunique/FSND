import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy #, or_
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, default_exceptions
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there. 
#     If you do not update the endpoints, the lab will not work - of no fault of your API code! 
#   - Make sure for each route that you're thinking through when to abort and with which kind of error 
#   - If you change any of the response body keys, make sure you update the frontend to correspond. 

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

        
    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    
    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(error=str(e)), code
    
    
    for ex in default_exceptions:
        app.register_error_handler(ex, handle_error)

    # @TODO: Write a route that retrivies all books, paginated. 
    #         You can use the constant above to paginate by eight books.
    #         If you decide to change the number of books per page,
    #         update the frontend to handle additional books in the styling and pagination
    #         Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars
    @app.route("/books", methods=['GET', 'POST'])
    def get_books():

        result = {}
        
        if request.method == "POST":
            request_json = request.get_json()
            title = request_json.get("title")
            author = request_json.get("author")
            rating = request_json.get("rating")

            book = Book(title, author, rating)
            book.insert()
            
            result["created"] = book.id
        

        book_query_results = Book.query.order_by("author").all()
        books = [book.format() for book in book_query_results]
        num_pages = (len(books) // BOOKS_PER_SHELF) + ( 1 if len(books) % BOOKS_PER_SHELF > 0 else 0)
        
        page = request.args.get("page", 1, type=int)        
        start = (page - 1) * BOOKS_PER_SHELF
        end = start + BOOKS_PER_SHELF
        
        result["success"] = True
        result["books"] = books[start:end]
        result["total_books"] = len(books)
        result["next_page"] = "/books?page={}".format(page+1) if page+1 <= num_pages else ""
        result["prev_page"] = "/books?page={}".format(page-1) if page > 1 else ""
        
        return jsonify(result)
    


    # @TODO: Write a route that will update a single book's rating. 
    #         It should only be able to update the rating, not the entire representation
    #         and should follow API design principles regarding method and route.  
    #         Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh
    @app.route("/books/<int:book_id>", methods=["PATCH", "DELETE"])
    def update_rating(book_id):
        book = Book.query.get(book_id)

        if book:
            if request.method == "PATCH":
                request_json = request.get_json(force=True)  # read json even if header is not set to application/json
                rating = request_json.get("rating")
                book.rating = rating
                book.update()
                return jsonify({
                    "success": True,
                    "book": book.format()
                })
            elif request.method == "DELETE":
                book.delete()
                
                book_query_results = Book.query.order_by("author").all()
                books = [book.format() for book in book_query_results]
                num_pages = (len(books) // BOOKS_PER_SHELF) + ( 1 if len(books) % BOOKS_PER_SHELF > 0 else 0)

                page = request.args.get("page", 1, type=int)        
                start = (page - 1) * BOOKS_PER_SHELF
                end = start + BOOKS_PER_SHELF
        
                return jsonify({
                    "success": True,
                    "deleted": book_id,
                    "books": books[start:end],
                    "total_books": len(books)
                })
        else:
            abort(404)
#             return jsonify({
#                 "success": False,
#                 "error": "Unable to locate book with id={}".format(book_id)
#             })


    # @TODO: Write a route that will delete a single book. 
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'

    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.
    


    # @TODO: Write a route that create a new book. 
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books. 
    #       Your new book should show up immediately after you submit it at the end of the page. 


    return app

    