from sqlalchemy import func
# from datetime import datetime
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

#just add last edition 
def add_and_dedup(subject):
    if Subject.query.filter(Subject.subject_name==subject.subject_name).all():
        return None
    else:
        db.session.add(subject)
        return subject

def load_authors():
    counter= 0

    enc = 'iso-8859-15'
    for row in open('seed_data/ol_authors.txt'):
        counter = counter + 1


       
        row = row.strip()
        (info_type, ol_id, num, date, info_json)= row.split("\t")

        info_dict = json.loads(info_json)
        # pprint(info_dict)
        author_ol_id = info_dict['key'][9:]

        if 'name' in info_dict:
            name = info_dict['name']
            short_name = name[:100]
    

        author = Author(author_ol_id=author_ol_id, name=short_name)

        db.session.add(author)
        if counter % 100000 == 0:
            print("added 100000 authors", counter)
            db.session.commit()

                

# load_authors()

def load_editions():
    counter = 0
    
    for row in open('seed_data/ol_editions.txt'):
        author_ol_id=None
        isbn_10=None
        isbn_13=None
        title=None
        counter = counter + 1

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
            # print(author_ol_id)
        
           
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

        new_book = Book(isbn_10=isbn_10, isbn_13=isbn_13, author_ol_id =author_ol_id ,title=title)
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

                if counter % 100000 == 0:
                    print("added 1000 subjects", counter)
                    

                new_subject = Book_subjects(book_id=new_book.book_id, subject_id= new_subject.subject_id)
                db.session.add(new_subject)
                if counter % 100000 == 0:
                    print("added 100000 Book_subjects", counter)
            db.session.commit()
# def load_associates():
    

# load_editions()              
#                     #vagrant disk space?   
#         # db.session.commit()
       

                    
                        
            
# #             #trim each of elements 
# #             #strip to only numbers and letters



#         # print(subject_table)       
#             #.remove or .split
#         #     rejex to write pattern
#         # subjects = "".join(subject_list)
#         #make for loop 
#         #check if added subjet before 
#         #label with id
#         #make subject table
#         #make a dictionary between subject name: subject id in db
#         #associate table between subject and book
#         #subjects reference table
#         #book subjects conecting bookid to subject id
    
    
# #         book = Book(isbn_10=isbn_10, isbn_13=isbn_13, title=title)


# # def load_works():
# #     counter = 0
# #     for row in open('seed_data/ol_works.txt'):
# #         counter = counter + 1
# #         if counter > 1:
# #             break

# #         row = row.strip()
# #         (info_type, ol_id, num, date, info_json)= row.split("\t")

# #         info_dict = json.loads(info_json)
# #         pprint(info_dict)

# # # load_works()

if __name__ == "__main__":
    connect_to_db(app)
    db.configure_mappers() 
    # In case tables haven't been created, create them
    db.create_all()
    # load_authors()
    load_editions()

    # Import different types of data
   
    

    

    

