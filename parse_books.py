from sqlalchemy import func
# from datetime import datetime
from model import Book, User, Book_shelf, Author, connect_to_db, db
from server import app 
from sys import argv
import json
from pprint import pprint 
def load_authors():
    counter= 0

    enc = 'iso-8859-15'
    for row in open('ol_dump_authors_2019-01-31.txt','r', encoding=enc):
        
        row = row.strip()
        (info_type, ol_id, num, date, info_json)= row.split("\t")

        info_dict = json.loads(info_json)

        author_ol_id = info_dict['key'][9:]
        name = info_dict['name']

        author = Author(author_ol_id=author_ol_id,
                name=name)

        db.session.add(author)
        db.session.commit()

def load_editions():
    counter = 0
    for row in open('ol_dump_editions_2019-01-31.txt'):

    

        row = row.strip()
        (info_type, ol_id, num, date, info_json)= row.split("\t")

        info_dict = json.loads(info_json)
    
        author_ol_id = info_dict['authors'][0]['key'][9:]
        isbn_10 = info_dict['isbn_10'][0]
        # isbn_13 = info_dict['isbn_13'][0]
        # gb_identifier = info_dict['identifiers']['goodreads'][0]
        subject = info_dict['subjects']

    
        title = info_dict['title']
        
        print(subject)
        #list
            # book = Book(isbn_10=isbn_10, subjects=subjects, title=title)

            # db.session.add(book)
            # db.session.commit()

load_editions()
# def load_works():
#     counter = 0
#     for row in open('ol_dump_works_2019-01-31.txt'):
#         counter = counter + 1
#         if counter >= 10:
#             break

#         row = row.strip()
#         (info_type, ol_id, num, date, info_json)= row.split("\t")

#         info_dict = json.loads(info_json)
#         pprint(info_dict)
# load_works()

# load_works()
# if __name__ == "__main__":
#     connect_to_db(app)

#     # In case tables haven't been created, create them
#     db.create_all()

#     load_editions()
#     load_authors()

    


# load_works()