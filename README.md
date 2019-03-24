
#IBDB
# <img src="/static/img/library.jpg">


## Table of Contents🐛

* [Tech Stack](#tech-stack)
* [Setup/Installation](#installation)
* [To-Do](#future)
* [License](#license)

## <a name="tech-stack"></a>Tech Stack

__Frontend:__ HTML5, CSS, Javascript, jQuery, Bootstrap <br/>
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy <br/>
__APIs:__ GoogleBooks, Open Library <br/>


## <a name="installation"></a>Setup/Installation ⌨️

#### Requirements:

- PostgreSQL
- Python 3.6
- Google Books and Open Library API keys
- Open library dump datasets of authors and editions 

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/alishalopes87/IBDb.git
```
Create a virtual environment🔮:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies🔗:
```
$ pip install -r requirements.txt
```
Get your own secret keys🔑 for [Google Books](https://developers.google.com/books/docs/v1/getting_started) Save them to a file `secrets.py`. Your file should look something like this:
```

APP_KEY = 'xyz'
GOOGLEBOOK_API_KEY = 'abc'
GOOGLEBOOK_API_SECRET = 'abc'


and download Open Library dump datasets Authors and Editions [Open Library](https://openlibrary.org/developers/dumps). 
```
Create database 'Library'.
```
$ createdb Library
```
Create your database tables and seed🌱 example data.
```
$ python model.py
```
Run the app from the command line.
```
$ python server.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```
$ python -i model.py
```

## <a name="future"></a>TODO✨
* Add migrations for search engine
* Add more testing! 
* Add rating system for books
