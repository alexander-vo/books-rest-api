# books-rest-api
Books REST API made by Alexander Voloshchenko. 

Books taken from Google Books API [https://www.googleapis.com/books/v1/volumes](https://www.googleapis.com/books/v1/volumes )
searched with additional query parameter `q`.

Example:

[https://www.googleapis.com/books/v1/volumes?q=Hobbit](https://www.googleapis.com/books/v1/volumes?q=Hobbit)

In code used with additional query parameters:

```json
{
  "langRestrict": "en",
  "maxResults": 40,
  "startIndex": 0
}
```

`"maxResults": 40` - max value for books per page

Example:

[https://www.googleapis.com/books/v1/volumes?q=Hobbit&langRestrict=en&maxResults=40&startIndex=0](https://www.googleapis.com/books/v1/volumes?q=Hobbit&langRestrict=en&maxResults=40&startIndex=0)

## Content

1. [Project Structure](#Project-Structure)
2. [Configuration](#Configuration)
    - [Python version](#Python-version)
    - [Packages and versions](#Packages-and-versions)
3. [How to run](#How-to-run)
4. [Database](#Database)
5. [API Calls](#API-Calls)

## Project Structure

```text
books-rest-api
├── app.py
├── books
│   ├── __init__.py
│   ├── collections.py
│   ├── db.py
│   ├── models.py
│   ├── resources.py
│   └── utils.py
├── config.py
├── Procfile
├── README.md
├── requirements.txt
├── runtime.txt
├── setup.cfg
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── test_books.json
    ├── test_db.py
    ├── test_factory.py
    └── test_rest.py

```

## Configuration

Environment variables are required:

```dotenv
ENV=<env>  # accepted values: prod | dev | test
MONGO_CLUSTER_NAME=<mongodb_cluster_name>
MONGO_USERNAME=<mongodb_user_name>
MONGO_USER_PASSWORD=<mongodb_user_password>
PROD_MONGO_DB_NAME=<mongodb_database_name_for_production>
TEST_MONGO_DB_NAME=<mongodb_database_name_for_tests>
DEV_MONGO_DB_NAME=<mongodb_database_name_for_development>
```

Accepted values for `ENV` variable: `prod`, `dev`, `test`.

Databases should contain **`books`** collection!

#### Python version 

`python 3.7`

#### Packages and versions

*All values are taken from `requirements.txt` file!*

```requirements
# Flask framework and rest extension
flask==1.1.2
flask-restful==0.3.8
# Tests and coverage
pytest==6.0.1
coverage==5.2.1
# Data models
pydantic==1.6.1
# Database connection
pymongo==3.11.0
flask-pymongo==2.3.0
# Must be installed to use mongodb atlas connection
dnspython==2.0.0
# HTTP requests lib
requests==2.24.0
# Gunicorn for deployment
gunicorn==20.0.4
```

## How to run

1) Create virtual environment \
`python3.7 -m venv env`
2) Activate virtual environment \
`source env/bin/activate`
3) Install dependencies from `requirements.txt` \
`pip install -r requirements.txt`
4) Load your environment variables described [here](#Configuration)
5) Run tests \
`pytest`
6) Run application \
`python app.py`
7) Check application home page [http://localhost:5000](http://localhost:5000). 
You should be redirected to the [http://localhost:5000/api/books](http://localhost:5000/api/books) endpoint.

## Database

MongoDB database was chosen for this application because we work mainly
with JSON data that is native to MongoDB (a document-oriented database that uses
JSON / BSON documents for storing data) and we have no relationship between documents, which is very suitable
for this database. In addition, we use a very simple scheme that can be changed very quickly at any time when we need it.
Moreover, we can easily use it from python using the `pymongo` and `flask-pymongo` packages.

Of course, we could also use PostgreSQL or SQLite (**only for development** and for
test apps like this) using SQLAlchemy, creating schemas, models, performing migrations, etc.

As the application grows, we may want to use different tables for `authors` and `categories`.
and we would use a ManyToMany relationship to the books table. In this case, I would definitely choose a SQL based database.

Books collection schema:

```mongodb
{
    '_id': String,
    'title': String,
    'authors': [String],
    'categories': [String],
    'published_date': String,
    'average_rating': Double,
    'ratings_count': Integer,
    'thumbnail': URL(String)
}
```

## API Calls

API requests documentation was made using Postman software and can 
be found [**here!!!**](https://documenter.getpostman.com/view/5375877/T1LFoqVi?version=latest)