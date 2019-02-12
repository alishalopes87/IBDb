from sqlalchemy import func
# from datetime import datetime
from model import Book, User, Book_shelf, connect_to_db, db
from server import app 
from sys import argv


def load_books():
    """Load books from raw_books.csv into databaase"""

    
    enc = 'iso-8859-15'
    for row in open("raw_books.txt",'r', encoding=enc):
        #stackoverflow https://stackoverflow.com/questions/16528468/while-reading-file-on-python-i-got-a-unicodedecodeerror-what-can-i-do-to-resol?fbclid=IwAR2DFBQeizmZcKk7honBCgOMo60Jz4s654_9CA6PFLF8mv1Wfw3ADPeKGZ0

        row = row.rstrip()
    
        (indentifer, book_id,best_book_id,work_id,books_count,isbn,
        isbn13,authors,original_publication_year,original_title,title,
        language_code,average_rating,ratings_count,work_ratings_count,work_text_reviews_count,
        ratings_1,ratings_2,ratings_3,ratings_4,ratings_5,image_url,small_image_url) = row.split("\t")
        
        book = Book(ISBN=isbn,
                    author=authors,
                    title=title,
                    average_rating=average_rating,
                    publication_year=original_publication_year)

        db.session.add(book)
        db.session.commit()

def load_users():
    """Load users from u.user into database."""

    print("Users")

    # ©Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")
        print(zipcode)
        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()
            
        

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users
    load_books()
