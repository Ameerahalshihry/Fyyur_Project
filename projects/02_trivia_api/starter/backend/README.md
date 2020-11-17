# Full Stack Trivia API Backend

The `./backend` directory contains Flask and SQLAlchemy server in app.py we define the endpoints and reference models.py for DB and SQLAlchemy setup. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: method not allowed

## Endpoints

#### GET /categories
 - General:
    - Returns a list of category objects, success value.
 - Sample:
 ```
  curl http://127.0.0.1:5000/categories
  ```
  ```
  {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
  ```

#### GET /questions
 - General:
    - Return a list of questions, number of total questions, current category, categories including pagination (every 10 questions).
 - Sample:
 ```
  curl http://127.0.0.1:5000/questions
  ```
  ```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 18
}
  ```

#### DELETE /questions/{question_id}
 - General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value.
 - Sample:
 ```
  curl -X DELETE http://127.0.0.1:5000/questions/4
  ```
  ```
 {
  "deleted": 4, 
  "success": true
}
  ```

  #### POST /questions
 - General:
    - Creates a new question using the submitted question and answer text, category, and difficulty score. Returns the id of the created question, success value.
 - Sample:
 ```
  curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Where is Jeddah city?", "answer":"Saudi Arabia", "category":"3", "difficulty":"2"}'
  ```
  ```
 {
  "question_created": 26, 
  "success": true
}
  ```

#### GET /categories/{category_id}/questions
 - General:
    - Return a list of questions based on category , number of total questions, current category, categories.
 - Sample:
 ```
  curl http://127.0.0.1:5000/categories/6/questions
  ```
  ```
{
  "current_category": "", 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
  ```

#### POST /questions/search
 - General:
    -  Return all questions for whom the search term is a substring of the question, number of these  questions, current category,and success value.
 - Sample:
 ``` 
  curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"city"}'
  ```
  ```
{
  "current_category": "", 
  "questions": [
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Saudi Arabia", 
      "category": 3, 
      "difficulty": 2, 
      "id": 26, 
      "question": "Where is Jeddah city?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
  ```

  #### POST /quizzes
 - General:
    -  Return a random questions within the given category, if provided, to play the quiz and success value.This endpoint should take category and previous question parameters.
 - Sample:
 ``` 
  curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5, 9], "quiz_category": {"type": "History", "id": "4"}}'
  ```
  ```
{
  "question": {
    "answer": "George Washington Carver", 
    "category": 4, 
    "difficulty": 2, 
    "id": 12, 
    "question": "Who invented Peanut Butter?"
  }, 
  "success": true
}
  ```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```