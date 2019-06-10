from sqlalchemy import func
# from datetime import datetime
from sqlalchemy_searchable import make_searchable, search
from model_2 import Book, User, Author, Subject, Book_subjects,Authors_books, connect_to_db, db
from server import app 
from sys import argv
import json
from pprint import pprint 

def add_and_dedup_editions(book):
    if Book.query.filter(Book.title==book.title).all():
        return None
    elif len(Author.query.filter(Author.author_ol_id==book.author_ol_id).all()) == 0:
        return None
    else:
        db.session.add(book)
        return book

def add_and_dedup(subject):
    if Subject.query.filter(Subject.subject_name==subject.subject_name).all():
        return None
    else:
        db.session.add(subject)
        return subject
def get_author_name(author_ol_id):
    author = Author.query.filter(Author.author_ol_id==author_ol_id).first()
    if author:
        return author.name
    else:
        return None

def load_authors():
    counter= 0

    enc = 'iso-8859-15'
    for row in open('seed_data/ol_authors.txt'):
        counter = counter + 1
        if counter == 1000000:
            break
        

       
        row = row.strip()
        (info_type, ol_id, num, date, info_json)= row.split("\t")

        info_dict = json.loads(info_json)
        author_ol_id = info_dict['key'][9:]

        if 'name' in info_dict:
            name = info_dict['name']
            short_name = name[:100]
    

        author = Author(author_ol_id=author_ol_id, name=short_name)

        db.session.add(author)
        if counter % 100000 == 0:
            print("added 100000 authors", counter)
            db.session.commit()

                


def load_editions():
    counter = 0
    
    for row in open('seed_data/ol_editions.txt'):
        author_ol_id=None
        isbn_10=None
        isbn_13=None
        title=None
        language=None
        publishers=None
        publish_date=None
        subjects=None
        counter = counter + 1
        if counter == 10000:
            break
        

        row = row.strip()
        # print(row)
        (info_type, ol_id, num, date, info_json)= row.split("\t")
        
        info_dict = json.loads(info_json)
        # pprint(info_dict)

        if 'authors' in info_dict:
            if not info_dict['authors']:

                author_ol_id=None
            else:    
                author_ol_id = info_dict['authors'][0]['key'][9:]
                search_authors = get_author_name(author_ol_id)
        if 'publishers' in info_dict:
            if not info_dict['publishers']:
                publishers=None
            else:
                publishers = info_dict['publishers'][0]

        if 'publish_date' in info_dict:
            publish_date = info_dict['publish_date']
           
        if 'languages' in info_dict:
           
            if not info_dict['languages']:
                language=None
            else:
                language = info_dict['languages'][0]['key'][11:]
        if 'isbn_10' in info_dict:
            # print(info_dict['isbn_10'])
            if not info_dict['isbn_10']:
                isbn_10 = None

            else:
                isbn_10 = info_dict['isbn_10'][0][:10]

        if 'isbn_13' in info_dict:

            if not info_dict['isbn_13']:
                isbn_13=None

            else:
                isbn_13 = info_dict['isbn_13'][0][:13]
        
        if 'title' in info_dict:
            title = info_dict['title']
        else:
            title = None

        if search_authors == None:
            continue
        else:

            new_book = Book(isbn_10=isbn_10, isbn_13=isbn_13, author_ol_id =author_ol_id ,
                title=title, language=language, search_authors=search_authors,
                publishers=publishers, publish_date=publish_date)
            print(new_book)

            if add_and_dedup_editions(new_book) == None:
                continue
            db.session.commit()

            if counter % 100000 == 0:
                print("added 100 books", counter)

            new_author = Authors_books(author_ol_id=new_book.author_ol_id, book_id=new_book.book_id)
            db.session.add(new_author)
            db.session.commit()
            if counter % 100000 == 0:
                print("added 100000 author_books", counter)
                    

                
            if 'subjects' in info_dict:
                subject_list = info_dict['subjects']

                for subject in subject_list:
                    new_subject = Subject(subject_name=subject)
                    if add_and_dedup(new_subject) == None:
                        continue
                    db.session.commit()

                    new_subject = Book_subjects(book_id=new_book.book_id, subject_id= new_subject.subject_id)
                    db.session.add(new_subject)
                    db.session.commit()
                

                    
           


def load_works():
    counter = 0
    for row in open('seed_data/ol_works.txt'):
        counter = counter + 1
        if counter > 1:
            break

        row = row.strip()
        (info_type, ol_id, num, date, info_json)= row.split("\t")

        info_dict = json.loads(info_json)
        pprint(info_dict)


if __name__ == "__main__":
    connect_to_db(app)
    make_searchable(db.metadata)
    db.configure_mappers() 
    # In case tables haven't been created, create them
    db.create_all()
    load_authors()
    load_editions()

    

    

    

