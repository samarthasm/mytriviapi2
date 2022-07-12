# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- This fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/api/v1.0/questions?page=1'`

- This fetches questions as per given query parameter of page number
- Request Arguments:
  - page : positive integer
- Returns: An object with a list of questions, number of total questions, the current category, all categories.
- Sample Response:
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "Science",
    "questions": [
        {
            "answer": "Sir Isaac Newton",
            "category": 1,
            "difficulty": 1,
            "id": 5,
            "question": "The concept of gravity was discovered by which famous physicist?"
        },
        {
            "answer": "206",
            "category": 1,
            "difficulty": 2,
            "id": 9,
            "question": "How many bones are in the human body?"
        },
        {
            "answer": "1789",
            "category": 4,
            "difficulty": 4,
            "id": 2,
            "question": "What year did the French Revolution start?"
        },
        {
            "answer": "Neil Armstrong",
            "category": 4,
            "difficulty": 3,
            "id": 4,
            "question": "Who was the first person in the world to land on the moon?"
        },
        {
            "answer": "Mount Everest",
            "category": 3,
            "difficulty": 1,
            "id": 6,
            "question": "Which is the tallest mountain in the world?"
        },
        {
            "answer": "Tributaries",
            "category": 3,
            "difficulty": 3,
            "id": 10,
            "question": "What are the branches of a river called?"
        },
        {
            "answer": "Louvre",
            "category": 2,
            "difficulty": 1,
            "id": 11,
            "question": "Where can you see the Mona Lisa?"
        },
        {
            "answer": "Spain",
            "category": 2,
            "difficulty": 3,
            "id": 12,
            "question": "Which country did the famous painter Pablo Picasso belong to?"
        },
        {
            "answer": "Mysuru",
            "category": 2,
            "difficulty": 4,
            "id": 13,
            "question": "In which city is the famous painting 'Lady with the Lamp' or 'Glow of Hope' currently stored at?"
        },
        {
            "answer": "Kolar Gold Fields",
            "category": 5,
            "difficulty": 3,
            "id": 14,
            "question": "What is the full form of the famous India movie named 'KGF'?"
        }
    ],
    "success": true,
    "total_questions": 16
}
```

`DELETE '/api/v1.0/questions/20'`

- A DELETE request to delete the question with id = 4 in above example
- Request Arguments: None
- Returns an object with success property as True or False
- Sample Success Response:
```json
{
    "success": true
}
```

`POST '/api/v1.0/questions'`

- A POST request to post a question into the Trivia DB
- Request Arguments: None
- Request Body Example
```json
{
    "question": "Who won the most Grand Slam Tournaments in Men's Singles category?",
    "answer": "Rafael Nadal",
    "difficulty": 2,
    "category": 6
}
```
- Sample Response object
```json
{
    "success": true
}
```

`POST '/api/v1.0/quizzes'`
- A POST request to play quiz in the Trivia App given previous questions and category being played
- Returns a random question in the playing category (if any) which is not in the list of previous questions
- Request Arguments: None
- Request Body Example
```json
{
    "previous_questions":[6, 4],
    "quiz_category": {"type": "Geography", "id": "6"}
}

- Sample Response Object
```json
{
    "question": {
        "answer": "Mount Everest",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "Which is the tallest mountain in the world?"
    },
    "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```