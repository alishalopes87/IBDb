"""Models and database functions for Books project."""

from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable, search
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy import func
import requests
from datetime import datetime
import os
from math import ceil

# from utils import Utils

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()
# utils = utils.Utils()
make_searchable()
GOOGLEKEY = os.environ.get("GOOGLEKEY")

class BookQuery(BaseQuery,SearchQueryMixin):
    pass

def convert_to_dict(result):
    """mutates sqlalchemy result into dictionary"""
##made this a helper function isnstead of a class method because result 
#can be both books and authors
    # for author in authors:
    result ={
        'author_ol_id': result.author_ol_id,
        'author_name': result.name,
        'author_url': '/Author/{}'.format(result.author_id),
        'book_id': result.book_id,
        'title': result.title,
        'book_url': '/Book/{}'.format(result.book_id)
        }

    return result


class User(db.Model):
    """User of book_shelf website."""
    query_class = BookQuery
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)

    book_shelves = db.relationship("Book_shelf")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"
    def convert_info(self):
        user = {
        "id": "user/{}".format(self.user_id),
        "nodeName": self.fname,
        "type": "user"

        }
        return user 

class Book(db.Model):
    """Book of book_shelf website"""

    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(3000),index=True) #searchable 
    isbn_10 = db.Column(db.String(100),index=True)
    isbn_13 = db.Column(db.String(100))
    publish_date = db.Column(db.String(1000),index=True)
    search_authors = db.Column(db.String(100),index=True)
    publishers = db.Column(db.String(1000),index=True)
    language = db.Column(db.String(100), index=True)
    author_ol_id = db.Column(db.String(1000), db.ForeignKey('authors.author_ol_id'), nullable=False)
    search_vector = db.Column(TSVectorType('title', 'search_authors',
                            catalog='pg_catalog.simple', 
                            weights={'title': 'A', 'search_authors': 'B'}))
    subjects = db.relationship("Subject",
                                secondary="book_subjects",
                                backref="books")

    book_shelves = db.relationship("Book_shelf")

    authors_books = db.relationship("Authors_books")

    def __repr__(self):
        """Provide helpful representation when printed"""

        return f"title={self.title}"

    def get_subjects(self):
        """query db for subjects of associated book"""
        return self.subjects



    def get_author(self):
        """query db for author by author_ol_id"""

        return Author.query.filter(Author.author_ol_id==self.author_ol_id).one()

    def get_isbn_10(self):
        """Get isbn from db"""

        return self.isbn_10

    def get_open_metadata(self):
        """get metadata from openlibrary"""
        isbn13 = self.isbn_13

        #use isbn-13 to get url for nearby library search
        if isbn13:
            open_library_url = "https://openlibrary.org/api/books"
            payload = {"bibkeys" : "ISBN:{}".format(isbn13), "format" : "json", "jscmd" : "data"}

            response_ol = requests.get(open_library_url, params=payload)

            return response_ol

    def parse_ol_metadata(self, response_ol):
        genres = []
        summary = None
        cover_img = None
        response_ol_json = response_ol.json()

        isbnstring = "ISBN:{}".format(self.isbn_13)
        if response_ol_json.get(isbnstring):
            if response_ol_json[isbnstring].get('cover'):
                cover_img = response_ol_json[isbnstring]["cover"]["medium"]
                
            if response_ol_json[isbnstring].get('excerpts'):
                summary = response_ol_json[isbnstring]['excerpts'][0]['text']
        genres = self.subjects

            # if 'subjects' in response_ol_json[isbnstring]: 
            #     for subject in response_ol_json[isbnstring]['subjects'][:3]:
            #         genres.append(subject['name'])

        return cover_img, summary, genres

    def get_google_metadata(self):
        url = "https://www.googleapis.com/books/v1/volumes"
        payload = {"q": "isbn:{}".format(self.get_isbn_10()), "key": GOOGLEKEY}
        response = requests.get("https://www.googleapis.com/books/v1/volumes", params=payload)
        # print(response.url)
        return response.json()

    def parse_metadata(self,book_json):
        genres = []
        summary = None
        cover_img = None
         # pragma: no cover
        if "description" in book_json["items"][0]["volumeInfo"]:
            summary = book_json["items"][0]["volumeInfo"]["description"]
        cover_img = book_json["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
        genres = self.subjects

        # if book_json["totalItems"] >= 1: # pragma: no cover
        #     if "categories" in book_json["items"][0]["volumeInfo"]:
        #         genres = book_json["items"][0]["volumeInfo"]["categories"]
        #     else:
        #         genres = None
        #     if "description" in book_json["items"][0]["volumeInfo"]:
        #         summary = book_json["items"][0]["volumeInfo"]["description"]
        #     else:
        #         summary = None
        #     if "imageLinks" in book_json:
        #         cover_img = book_json["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]


        return summary, cover_img, genres

    def search_results(self):
        author = self.get_author()
        book = {
                'author':self.author_ol_id,
                'book_id': self.book_id,
                'title': self.title,
                'book_url': '/Book/{}'.format(self.book_id),
                'author_name': author.name,
                'author_url': '/Author/{}'.format(author.author_id),
                'language': self.language
                }
        return book 



class Authors_books(db.Model):
    """Associate table between books and authors"""
    __tablename__="authors_books"

    authors_books_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    author_ol_id = db.Column(db.String(1000), db.ForeignKey('authors.author_ol_id'), nullable=False,index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)

    books = db.relationship("Book")
    authors = db.relationship("Author")
#associatre table between books and authors multiple authors 
class Author(db.Model):
    """Author table of webste"""

    __tablename__ ="authors"

    author_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    author_ol_id  = db.Column(db.String(100), unique=True)
    name= db.Column(db.String(1000), index=True)
    search_vector = db.Column(TSVectorType('name', 
                            catalog='pg_catalog.simple',
                            weights={'name': 'A'}))

    authors_books = db.relationship("Authors_books")


    def get_books(self):
        """return books associated with author by author_ol_id"""
        #self.author_ol_id


        return Authors_books.query.filter_by(author_ol_id=self.author_ol_id).all()

    def convert_info(self):
        """convert author info to dictionary"""

        author_dict = {
            "id" : "author/{}".format(self.author_id),
            "nodeName": self.name,
            "type": "author"
            }

        return author_dict
class Subject(db.Model):
    """Subject of book."""

    __tablename__ = "subjects"

    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(2000), unique=True,index=True)
    search_vector = db.Column(TSVectorType('subject_name',
                            catalog='pg_catalog.simple',
                             weights={'search_name': 'A'}))

    book_subjects = db.relationship("Book_subjects")
    #change to name 
    def convert_info(self):
        """conver subject info to dictionary"""
        subject_id= "subject/{}".format(self.subject_id)
        subject_name = self.subject_name
        subject_dict ={
            "id" :subject_id,
            "nodeName": subject_name,
            "type": "subject"
            }

        return subject_dict


class Book_subjects(db.Model):
    """Subject of a specific book."""

    __tablename__ = "book_subjects"

    book_subject_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        nullable=False)
    subject_id = db.Column(db.Integer,
                            db.ForeignKey('subjects.subject_id'),
                            nullable=False)

    books = db.relationship("Book")
    subjects = db.relationship("Subject")
                                         
class Book_shelf(db.Model):
    """Book_shelf of website"""

    __tablename__ = "book_shelves"

    #add created date 
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))

        # Define relationship to user
    users = db.relationship("User")

    # Define relationship to book
    books = db.relationship("Book")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Book_shelf booking_id={self.booking_id} 
                   User-{self.user_id} 
                   book_id={self.book_id}"""

    def convert_book_info(self):
        """Returns individual book information for 
        items in shelf and returns dictionary"""

        book_id = "book/{}".format(self.books.book_id)
        book_title = self.books.title
        subjects = self.books.subjects
        print(subjects)
        book_dict ={
            "id" :book_id,
            "nodeName": book_title,
            "type": "book",
            "subjects": []
            }

        return book_dict
class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///shelves'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
