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
#----------------------------------------------------------------------------#
# App Setup
#----------------------------------------------------------------------------#

def create_app(test_config=None):
    # creating and configuring the app
    app = Flask(__name__)
    # To run Server, executing from backend directory:
    # Only one Time:
    # export FLASK_APP=flaskr
    # export FLASK_ENV=development
    # flask run
    setup_db(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    @app.route("/categories", methods=["GET"])
    def category():

        try:
            categories_list = Category.query.all()

            response = {
                'categories': {},
                "success": True
            }

            for category in categories_list:
                response['categories'][str(category.id)] = category.type

            return jsonify(response)

        except Exception as e:
            print(e)
            return abort(500, 'Something went wrong')

@app.route("/questions", methods=["GET"])
    def question():
        try:
            page_no = int(request.args['page'])
        except Exception as e:
            return abort(400, 'Server could not understand the made request')

        start = (page_no-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        response = {
            'questions': [],
            'total_questions': -1,
            'categories': {},
            'current_category': "",
            'success': True
        }

        all_questions = []
        filtered_questions = []

        try:
            for question in Question.query.all():
                all_questions.append(question.format())

            for category in Category.query.all():
                response['categories'][str(category.id)] = category.type
        except Exception as e:
            print(e)
            return abort(500, 'Something went wrong')

        filtered_questions = all_questions[start:end]

        if len(filtered_questions) == 0:
            return abort(404)

        response['questions'] = filtered_questions
        response['total_questions'] = len(all_questions)
        response['current_category'] = response['categories'][str(
            filtered_questions[0]['category'])]

        return jsonify(response)
    
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if question is None:
            abort(400)

        else:
            question.delete()
            return jsonify({'success': True})
    
    @app.route("/questions", methods=["POST"])
    def post():

        # Validations
        try:
            category_check = Category.query.filter(
                Category.id == int(request.json['category'])).one_or_none()

            if category_check is None:
                return abort(400)
        except:
            return abort(400)

        try:
            new_question = Question(
                question=request.json['question'],
                answer=request.json['answer'],
                difficulty=int(request.json['difficulty']),
                category=int(request.json['category'])
            )
        except:
            return abort(400)

        try:
            new_question.insert()
            return jsonify({'success': True})
        except:
            return abort(500)
    
    @app.route("/questions/search", methods=["POST"])
    def search():

        questions = Question.query.filter(Question.question.ilike(
            "%{}%".format(request.json['searchTerm']))).all()

        if len(questions) == 0:
            return abort(404)

        response = {
            'questions': [],
            'total_questions': -1,
            'current_category': "",
            'success': True
        }

        all_questions = []

        try:
            for question in questions:
                all_questions.append(question.format())

        except Exception as e:
            print(e)
            return abort(500)

        if len(all_questions) == 0:
            return jsonify()

        current_category = Category.query.filter(Category.id == all_questions[0]['category']).one()

        response['questions'] = all_questions
        response['total_questions'] = len(all_questions)
        response['current_category'] = current_category.type

        return jsonify(response)
    
    @app.route("/categories/<int:category_id>/questions")
    def category_wise_questions(category_id):

        questions = Question.query.filter(Question.category == category_id).all()

        if len(questions) == 0:
            return abort(404)

        response = {
            'questions': [],
            'total_questions': -1,
            'current_category': "",
            'success': True
        }

        all_questions = []

        try:
            for question in questions:
                all_questions.append(question.format())

        except Exception as e:
            print(e)
            return abort(500)

        if len(all_questions) == 0:
            return abort(404)

        current_category = Category.query.filter(Category.id == category_id).one()

        response['questions'] = all_questions
        response['total_questions'] = len(all_questions)
        response['current_category'] = current_category.type

        return jsonify(response)
    
    @app.route("/quizzes", methods=["POST"])
    def quiz():

        try:
            quiz_category_id = int(request.json['quiz_category']['id'])
            previous_questions = request.json['previous_questions']
        except:
            return abort(400)

        if(quiz_category_id != 0):
            available_questions_query = Question.query.filter(Question.category == quiz_category_id).filter(~Question.id.in_(previous_questions))
        if(quiz_category_id == 0):
            available_questions_query = Question.query.filter(~Question.id.in_(previous_questions))

        available_questions = available_questions_query.all()

        if len(available_questions) == 0:
            return jsonify({"question":False, "success": True})

        next_question = available_questions[randrange(len(available_questions))]

        return jsonify({"question":next_question.format(), "success": True})
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "This is a Bad Request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "That's an error, Page Not found"
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500


    

    return app

