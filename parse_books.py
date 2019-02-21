from sqlalchemy import func
# from datetime import datetime
from model_2 import Book, User, Author, Subject, connect_to_db, db
from server import app 
from sys import argv
import json
from pprint import pprint 

def add_and_dedup(subject):
    if Subject.query.filter(Subject.subject_name==subject).all():
        return None
    else:
        subject = Subject(subject_name=subject)
        db.session.add(subject)

def load_authors():
    counter= 0

    enc = 'iso-8859-15'
    for row in open('seed_data/ol_authors.txt','r', encoding=enc):
        counter= counter +1
        if counter>=100:
            break
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
    subject_table = set()
    for row in open('seed_data/ol_editions.txt'):
        counter = counter +1
        if counter >= 100:
            break

    

        row = row.strip()
        (info_type, ol_id, num, date, info_json)= row.split("\t")

        info_dict = json.loads(info_json)
        if 'isbn_10' in info_dict:
            isbn_10 = info_dict['isbn_10'][0]
        else:
            isbn_10 = None
        if 'isbn_13' in info_dict:
            isbn_13 = info_dict['isbn_13'][0]
        else:
            isbn_13 = None
        if 'title' in info_dict:
            title = info_dict['title']
        else:
            title = None

        
        if 'subjects' in info_dict:
            subject_list = info_dict['subjects']

            for subject in subject_list:
                print(subject)
                add_and_dedup(subject)

        db.session.commit()

                # subjects = Subject.query.all()
                # print(subjects)
                # # for subject_obj in subjects:
                # print(subject_obj.subject_name)
                # if subject != subject_obj.subject_name:
                #     subject = Subject(subject_name=subject)
       

                    
                        
            
            #trim each of elements 
            #strip to only numbers and letters


    # for subject_name in subject_table:
    #     print(subject_name)

    #      subject = Subject(subject_name=subject_name)

    #     db.session.add(subject)
    #     db.session.commit()
        # for subject in subject_list:
        #     subject_table.add(subject)

        # subjects = list(subject_table)

        # print(subject_table)       
            #.remove or .split
        #     rejex to write pattern
        # subjects = "".join(subject_list)
        #make for loop 
        #check if added subjet before 
        #label with id
        #make subject table
        #make a dictionary between subject name: subject id in db
        #associate table between subject and book
        #subjects reference table
        #book subjects conecting bookid to subject id
    
    
#         book = Book(isbn_10=isbn_10, isbn_13=isbn_13, title=title)


# def load_works():
#     counter = 0
#     for row in open('seed_data/ol_works.txt'):
#         counter = counter + 1
#         if counter >= 2:
#             break

#         row = row.strip()
#         print(row)
#         (info_type, ol_id, num, date, info_json)= row.split("\t")

#         info_dict = json.loads(info_json)
#         pprint(info_dict)

# load_works()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
   
load_editions()
# #     load_authors()
    

    

