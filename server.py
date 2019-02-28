"""Book_shelves"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,jsonify, abort)
from sqlalchemy.orm.attributes import flag_modified 
from sqlalchemy import func
from sqlalchemy_searchable import search
from flask_debugtoolbar import DebugToolbarExtension
import requests
from model_2 import Authors_books, User, Book_shelf, Book, Author, Subject,  Book_subjects, connect_to_db, db

import json


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

@app.route('/search-books.json')
def search_to_books():


    results = []

    title = request.args.get('book')
    author = request.args.get('author')

    if title:
        query = db.session.query(Book)
        query = search(query, title,sort=True)
        print(query.first().title)
        books = query.filter(Book.title.ilike('%' + title + '%')).all()
        

        for book in books:

            book = {
            'author':book.author_ol_id,
            'book_id': book.book_id,
            'title': book.title,
            'book_url': '/Book/{}'.format(book.book_id)
            }
       
            results.append(book)

    elif author:

        query= db.session.query(Author)
        query = search(query, author,sort=True)
        authors = query.filter(Author.name.ilike('%' + author + '%')).all()
        print(query.first().name)

        for author in authors:
            author ={
            'author_ol_id': author.author_ol_id,
            'name': author.name,
            'author_url': '/Author/{}'.format(author.author_id)
            }

            results.append(author)

    return jsonify(*results)

@app.route('/search-books')
def search_books_form():
    """Search form for user to search books"""

    #refresh page with new search
    return render_template('search.html')

@app.route('/')
def indenx():
    """Homepage"""
    #deleting things from bookshelf

    return render_template("login_form.html")

@app.route('/register', methods=['GET'])
def registration_form():
    """Recieve user information"""

    return render_template("registration_form.html")


@app.route('/register', methods=["POST"])
def register_process():
    """Add user information to database"""

    email = request.form["email"]
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    age = int(request.form["age"])

    new_user = User(email=email, password=password, fname=fname, 
    lname=lname, age=age)

    db.session.add(new_user)
    db.session.commit()

    flash("User {} added.".format(fname) )

    return redirect("/")

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")

@app.route('/login', methods=['POST'])
def login_process():
    """Process user login"""


    email = request.form["email"]
    password = request.form["password"]
    #dont store passwords

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/register")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect(f"/User/{user.user_id}")

@app.route('/logout')
def logout():
    """Log user out"""

    del session['user_id']
    flash('Logged out')
    return redirect('/')

@app.route("/User/<int:user_id>", methods=['GET', 'POST'])
def user_detail(user_id):
    """Show info about user."""

    user = User.query.get(user_id)
    return render_template("user.html", user=user)


@app.route("/books")
def book_list():
    """Show list of books."""

    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page=page,per_page=50)
    # books = Book.query.order_by('title').all()
    return render_template("book_list.html", books=books)

@app.route("/Author/<int:author_id>", methods=['GET'])
def author_info(author_id):
    """Show books written by author"""

    author = Author.query.get(author_id)
    print(author.author_ol_id)
    
    author_books = Authors_books.query.filter_by(author_ol_id=author.author_ol_id).all()
    print(author_books)
    return render_template('author.html', author=author,author_books=author_books)
        
    # author = Author.query.get(author_id)x
    # books = Authors_books.query.filter(Authors_books.author_ol_id
    #     ==author.author_ol_id).all()


   
    # print(books)
    # print(author.author_ol_id)
    # author = Authors_books.query.filter(Authors_books.author_ol_id==author.author_ol_id).one()
    # print('********',author,'***********')
    # auth_shelf = author.authors_books
    # print('********',auth_shelf,'***********')



@app.route("/Book/<int:book_id>", methods=['GET'])
def book_detail(book_id):
    """Show info about book
    if user if logged in 
    """

    book = Book.query.get(book_id)
    author = Author.query.filter(Author.author_ol_id==book.author_ol_id).one()

     #get summary, genres and cover image from Google Books
    url = "https://www.googleapis.com/books/v1/volumes"
    payload = {"q": "isbn:{}".format(book.isbn_10), "key": "AIzaSyBamy3iueA4AN-cfCzd45r20cmHOkNySac"}


    response = requests.get("https://www.googleapis.com/books/v1/volumes", params=payload)
    # print(response.url)
    book_json = response.json()

    cover_img = None
    if book_json["totalItems"] >= 1: # pragma: no cover
        
        cover_img = book_json["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
        
    

    session["book_id"] = book.book_id

    return render_template("book.html",
                            book=book,
                            author=author,response=response, cover_img=cover_img)

@app.route("/add_book/<int:book_id>",methods=['POST'])
def add_book_to_user_shelf(book_id):
    """Select book from database and add to users bookshelf"""
    #add logic so button will not allow you to save if not logged in
      

    user_id = session.get("user_id")

    if user_id:

        new_shelf =Book_shelf(book_id=book_id, user_id=user_id)

        db.session.add(new_shelf)
        db.session.commit()

        flash("Book added to your shelf")
        return redirect(f"/User/{user_id}")

    else:
        flash("Must be logged in to save")
        return redirect(f"/")

@app.route("/delete_book/<int:booking_id>", methods=['POST'])
def delete_book_from_user_shelf(booking_id):
    """Delete book from users shelf"""

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    if user_id:

        book_shelf = Book_shelf.query.get(booking_id)
        db.session.delete(book_shelf) 

        db.session.commit()

        flash("Book deleted from your shelf")
        return redirect(f"/User/{user.user_id}")

    else:
        flash("Must be logged in to delete")
        return redirect(f"/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')