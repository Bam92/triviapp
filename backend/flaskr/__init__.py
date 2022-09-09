from crypt import methods
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random as r

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

            return jsonify ({
                'success': True,
                'created': question.id,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)
    
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        search_term = request.json['search_term']

        questions = Question.query.filter(Question.question.ilike("%" + search_term + "%")).all()

        questions_formatted = [question.format() for question in questions]

        return jsonify ({
            "success": True,
            "questions": questions_formatted[start:end],
            "totalQuestions": len(questions),
            "categories": categories(),
            "currentCategory": "History"
        })

    @app.route('/categories/<id>/questions', methods=["GET"])
    def get_by_category(id):

        try:
            questions = Question.query.filter(Question.category == id)
            questions_formatted = [question.format() for question in questions]

            return jsonify ({
                'success': True,
                "questions": questions_formatted,
                "totalQuestions": len(questions_formatted),
                "categories": categories(),
                "currentCategory": Category.query.get(id).type
            })

        except: 
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        prev_questions = request.json['previous_questions']
        quiz_category = request.json['quiz_category']['id']
        
        # generate number: 1 to len(questions)
        max_limit = len(Question.query.all())
        question_id = r.randint(1, max_limit)

        try:
            question = Question.query.filter(Question.id == question_id).one() \
                if quiz_category == 0 \
                else Question.query.filter(Question.id == question_id, Question.category == quiz_category).one()

            question_formatted = question.format()

            return jsonify ({
                "success": True,
                "question": question_formatted,
            })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    if __name__ == "__main__":
        app.run(host='0.0.0.0')

    return app

