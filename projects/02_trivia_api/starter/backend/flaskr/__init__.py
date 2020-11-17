import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
#paginate questions every 10 questions
def paginate_questions(request, all_questions):
    page = request.args.get('page', 1, type=int)
    start = (page -1 ) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in all_questions]
    current_questions = formatted_questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={'/': {'origins': '*'}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()

    return jsonify({
      'success':True,
      # return categories as object {'id': 'type'}
      'categories': {category.id: category.type for category in categories}
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
  @app.route('/questions')
  def get_questions():
    all_questions = Question.query.all()
    #paginate questions every 10 questions
    current_questions = paginate_questions(request, all_questions)
    categories = Category.query.all()
    
    if len (current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(all_questions),
      'categories': {category.id: category.type for category in categories},
      'current_category': ''
    })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)
      
      question.delete()
      return jsonify({
        'success':True,
        'deleted': question_id
      })

    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    try:
      added_question=Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      added_question.insert()

      return jsonify({
        'success': True,
        'question_created': added_question.id
      })
    
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def question_search():
    body = request.get_json()
    search_term = body.get('searchTerm')
    search_result = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

    if (len(search_result) == 0):
      abort(404)
    
    return jsonify({
      'success': True,
      'questions': [question.format() for question in search_result],
      'total_questions':len(search_result),
      'current_category':''
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questins_by_specific_category(category_id):
    category=Category.query.filter_by(id=category_id).one_or_none()

    if category is None:
        abort(404)

    questions_by_specific_category=Question.query.filter_by(category=category.id).all()

    return jsonify({
      'success': True,
      'questions': [question.format() for question in questions_by_specific_category],
      'total_questions': len(questions_by_specific_category),
      'current_category':''
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
  @app.route('/quizzes', methods=['POST'])
  def play_questions_quiz():
    try:
      body = request.get_json()
      previous_questions = body.get('previous_questions')
      quiz_category= body.get('quiz_category')

      #play based on select ALL category
      if (quiz_category['id'] == 0):
        questions = Question.query.all()
      #play based on select specific category
      else:
        questions = Question.query.filter_by(category=quiz_category['id']).all()

      #get random question to play quiz
      total_questions= len(questions)
      def get_random():
        #random.randrange(start, stop[, step]) Return a randomly selected element from range(start, stop, step)
        return questions[random.randrange(0, total_questions, 1)]

      random_question= get_random()
      #define flag to check if the random question is asked before so generate another random question to play quiz until finish all questions
      used_question= True
      while used_question:
        if random_question.id in previous_questions:
          random_question= get_random()
        else:
          used_question= False

      return jsonify({
            'success': True,
            'question': random_question.format()
              })
    except:
      abort(422)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'message': "resource not found ",
      'error': 404
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'message': "unprocessable",
      'error': 422
    }), 422

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'message': "method not allowed",
      'error': 405
    }), 405

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'message': "bad request",
      'error': 400
    }), 400
  
  return app
