"""Models and database functions for Books project."""

from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable, search
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy import func


# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()
make_searchable(db.metadata)

class BookQuery(BaseQuery,SearchQueryMixin):
    pass

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

class Book(db.Model):
    """Book of book_shelf website"""

    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(1000),index=True) #searchable 
    isbn_10 = db.Column(db.String(100))
    isbn_13 = db.Column(db.String(100))
    author_ol_id = db.Column(db.String(1000), db.ForeignKey('authors.author_ol_id'), nullable=False)
    search_vector = db.Column(TSVectorType('title', 'isbn_10', 'isbn_13',
                            catalog='pg_catalog.simple'))
    subjects = db.relationship("Subject",
                                secondary="book_subjects",
                                backref="books")

    book_shelves = db.relationship("Book_shelf")

    authors_books = db.relationship("Authors_books")

    def __repr__(self):
        """Provide helpful representation when printed"""

        return f"title={self.title}"

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
    name= db.Column(db.String(1000))
    search_vector = db.Column(TSVectorType('name',
                            catalog='pg_catalog.simple'))

    authors_books = db.relationship("Authors_books")

class Subject(db.Model):
    """Subject of book."""

    __tablename__ = "subjects"

    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(2000), unique=True,index=True)
    search_vector = db.Column(TSVectorType('subject_name',
                            catalog='pg_catalog.simple'))
    #change to name 

    book_subjects = db.relationship("Book_subjects")

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
