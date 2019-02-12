from sqlalchemy import func
from datetime import datetime
from sys import argv


def load_data():
    variable=  """book_id,best_book_id,work_id,books_count,isbn,
            isbn13,authors,original_publication_year,original_title,title,
            language_code,average_rating,ratings_count,work_ratings_count,work_text_reviews_count,
            ratings_1,ratings_2,ratings_3,ratings_4,ratings_5,image_url,small_image_url""".split(",")
    
    enc = 'iso-8859-15'
    for row in open("raw_books.txt",'r', encoding=enc):
        #stackoverflow https://stackoverflow.com/questions/16528468/while-reading-file-on-python-i-got-a-unicodedecodeerror-what-can-i-do-to-resol?fbclid=IwAR2DFBQeizmZcKk7honBCgOMo60Jz4s654_9CA6PFLF8mv1Wfw3ADPeKGZ0

        row = row.rstrip()
        try:
            (indentifer, book_id,best_book_id,work_id,books_count,isbn,
            isbn13,authors,original_publication_year,original_title,title,
            language_code,average_rating,ratings_count,work_ratings_count,work_text_reviews_count,
            ratings_1,ratings_2,ratings_3,ratings_4,ratings_5,image_url,small_image_url) = row.split("\t")
        # (isbn, authors, original_publication_year, title, 
        # language_code, average_rating, image_url, small_image_url)= row.split("\t")

            print(title)
        except ValueError as ve:
            print("newbook")
            row_len = row.split("\t")
            count =0
            for value in row_len:
                print("\t", variable[count], value) 
                count = count + 1
        
        

load_data()