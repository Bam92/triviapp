from crypt import methods
import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    # utility function
    def categories():
        categories = Category.query.all()

        return {
                category.id: category.type
                for category in categories
            }

    @app.route('/categories')
    def get_categories():

        return jsonify ({
            'success': True,
            "categories": categories()
        })

    @app.route('/questions')
    # @cross_origin(supports_credentials=True)
    def get_questions():
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions = Question.query.all()

        questions_formatted = [question.format() for question in questions]

        return jsonify ({
            'success': True,
            "questions": questions_formatted[start:end],
            "totalQuestions": len(questions),
            "categories": categories(),
            "currentCategory": "History"
        })

    @app.route('/questions/<id>', methods=["DELETE"])
    def delete_question(id):

        try:
            question = Question.query.get(id)
            question.delete()
            print(question)

            return jsonify ({
                'success': True,
                'deleted': question.id,
                'total_questions': len(Question.query.all())
            })

        except: 
            abort(422)

    @app.route('/questions', methods=["POST"])
    def post_question():
        question=request.json['question']
        answer=request.json['answer']
        category=request.json['category']
        difficulty=request.json['difficulty']

        try:
            question = Question(question, answer, category, difficulty)
            question.insert()

            selection = Question.query.order_by(Question.id).all()

            return jsonify ({
                'success': True,
                'created': question.id,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)
    
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    # @app.errorhandler(404)
    # def not_found(error):
    #     return jsonify({
    #         "success": False, 
    #         "error": 404,
    #         "message": "Not found"
    #         }), 404

    # @app.errorhandler(422)
    # def unprocessable(error):
    #     return jsonify({
    #     "success": False, 
    #     "error": 422,
    #     "message": "unprocessable"
    #     }), 422

    if __name__ == "__main__":
        app.run(host='0.0.0.0')

    return app

