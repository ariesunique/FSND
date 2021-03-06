import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, default_exceptions


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return jsonify({
            "message": "Hello World!"
        }) 

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    # CORS Headers 
#     @app.after_request
#     def after_request(response):
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
#         response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#         return response
    
    '''
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route("/categories")
    def get_categories():
        categories = { category.id : category.type for category in Category.query.all() }
        return jsonify({
            "categories": categories,
            "success" : True
        })


    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route("/questions")
    def get_questions():
        questions = [ question.format() for question in Question.query.order_by("id").all() ]
        categories = { category.id : category.type for category in Category.query.all() }
        current_category = request.args.get("current_category")
        
        ITEMS_PER_PAGE = 10
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        
        return jsonify({
            "questions" : questions[start:end],
            "total_questions": len(questions),
            "categories": categories,
            "current_category": current_category,
            "success": True
        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route("/categories/<int:cat_id>/questions")
    def get_questions_for_category(cat_id):
        
        current_category = Category.query.get(cat_id)
        if not current_category:
            abort(404)
        
        questions = Question.query.filter_by(category=cat_id).all()
        
        questions = [ question.format() for question in Question.query.filter_by(category=cat_id).order_by("id").all() ]
        categories = { category.id : category.type for category in Category.query.all() }
        
        ITEMS_PER_PAGE = 10
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        
        return jsonify({
            "questions" : questions[start:end],
            "total_questions": len(questions),
            "categories": categories,
            "current_category": cat_id,
            "success": True
        })


    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(success=False,error=str(e)), code
    
    
    for ex in default_exceptions:
        app.register_error_handler(ex, handle_error)   

    return app

    