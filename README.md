# Casting Agency Specifications

## Motivation for project
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

Models:

Movies with attributes title and release date

Actors with attributes name, age and gender

Endpoints:

GET /actors and /movies

DELETE /actors/ and /movies/

POST /actors and /movies and

PATCH /actors/ and /movies/

Roles:

Casting Assistant

Can view actors and movies

Casting Director

All permissions a Casting Assistant has and…

Add or delete an actor from the database

Modify actors or movies

Executive Producer

All permissions a Casting Director has and…

Add or delete a movie from the database

Tests:

One test for success behavior of each endpoint

One test for error behavior of each endpoint

At least two tests of RBAC for each role

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```bash
pip install virtualenv
virtualenv --no-site-packages env
source env/bin/activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
When testing locally, models.py should be:
```python
# database_path = os.environ['DATABASE_URL']

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
```
When testing on heroku, models.py should be:
```python
database_path = os.environ['DATABASE_URL']

# database_filename = "database.db"
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
```

From the working folder in terminal run:
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Running the server locally

To run the server, execute:

```bash
python app.py
```

## Running the server on heroku
https://kknewudaapp.herokuapp.com

The token is in the `setup.sh`, you can test the API like this:

```bash
source setup.sh
curl -H "Authorization: Bearer ${TOKEN_EP}" https://kknewudaapp.herokuapp.com/movies | jq 
```


## API document
```
Endpoints
GET '/actors'
POST '/actors'
PATCH '/actors/<actor_id>'
DELETE '/actors/<actor_id>'
GET '/movies'
POST '/movies'
PATCH '/movies/<movie_id>'
DELETE '/movies/<movie_id>'


GET '/actors'
- Get all actors' information
- Request Arguments: None
- Returns: A list contains all the actors' info.
{
  "actors": [
    {
      "age": 31,
      "gender": "M",
      "id": 1,
      "name": "actor1"
    }
  ],
  "success": true
}

POST '/actors'
- Add a actor
- Request Arguments: name, age, gender
{"name":"actor1", "age":31, "gender":"M"}
- Returns: The actor info which we added with this request.
{
  "actors": {
    "age": 31,
    "gender": "M",
    "id": 1,
    "name": "actor1"
  },
  "success": true
}

PATCH '/actors/<actor_id>'
- Update a actor's information
- Request Arguments: name, age, gender
{"name":"actor2", "age":31, "gender":"M"}
- Returns: The actor info which we updated with this request.
{
  "actors": {
    "age": 31,
    "gender": "M",
    "id": 1,
    "name": "actor2"
  },
  "success": true
}

DELETE '/actors/<actor_id>'
- Delete a actor
- Request Arguments: actor_id
- Returns: The id of the actor which was deleted 
{
  "actors": "1",
  "success": true
}

GET '/movies'
- Get all movies' information
- Request Arguments: None
- Returns: A list contains all the movies' info.
{
  "movies": [
    {
      "id": 1,
      "release_date": "2019-11-11",
      "title": "movie1"
    }
  ],
  "success": true
}

POST '/movies'
- Add a movie
- Request Arguments: title, release_date
{"title":"movie1", "release_date": "2019-11-11"}
- Returns: The movie info which we added with this request.
{
  "movies": {
    "id": 1,
    "release_date": "2019-11-11",
    "title": "movie1"
  },
  "success": true
}

PATCH '/movies/<movie_id>'
- Update a movie's information
- Request Arguments: title, release_date
{"title":"movie2", "release_date": "2019-11-11"}
- Returns: The movie info which we updated with this request.
{
  "movies": {
    "id": 1,
    "release_date": "2019-11-11",
    "title": "movie2"
  },
  "success": true
}

DELETE '/movies/<movie_id>'
- Delete a movie
- Request Arguments: movie_id
- Returns: The id of the movie which was deleted 
{
  "movies": "1",
  "success": true
}
```

## Testing
To run the tests, run

```python
pytest test_app.py
```
