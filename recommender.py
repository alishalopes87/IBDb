from sqlalchemy import func
from model_2 import Authors_books, User, Book_shelf, Book, Author, Subject,  Book_subjects, connect_to_db, db
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from server import app
from sys import argv
# import pandas as pd 
def subjects():
    subjects = Subject.query.all()
    subject_names = []

    tfidf = TfidfVectorizer(stop_words='english')

    sub_subjects = subjects[:5]

    for subject in sub_subjects:
        subject_names.append(subject.subject_name)

    


    tfidf_matrix = tfidf.fit_transform(subject_names)
    tfidf_matrix.shape

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    print(cosine_sim)

def title_index():
    books = Book.query.all()
    book_titles = []

    for book in books:
        book_titles.append(book.title)
        indices = pd.Series(book_titles.index, index=book_titles).drop_duplicates()
    print(indeces)














if __name__ == "__main__":
    connect_to_db(app)
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    subjects()
    title_index()

    
  