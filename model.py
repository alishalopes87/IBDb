from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"

class Book(db.Model):
    """Book of website"""

    __tablename__ = "books"

    ISBN = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))

    def __repr__(self):
        """Provide helpful representation when printed"""

        return f"Book ISBN={self.ISBN} title={self.title}>"
                                         
class Book_shelf(db.Model):
    """Book_shelf of website"""

    __tablename__ = "book_shelves"

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), db.ForeignKey('users.email'))
    title = db.Column(db.String(100), db.ForeignKey('books.title'))
