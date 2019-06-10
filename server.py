"""Book_shelves"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,jsonify, abort)
from sqlalchemy.orm.attributes import flag_modified 
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy_searchable import search
from flask_debugtoolbar import DebugToolbarExtension
import requests
from model_2 import *
from pyisbn import convert as convert_isbn
from flask_paginate import Pagination, get_page_parameter
import json


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined



@app.route('/search-subjects.json')
def filter_by_subject():
    results = []
    subject = request.args.get('subject')
    look_for = '{}%'.format(subject)
    subjects = Subject.query.filter(Subject.subject_name.ilike(look_for)).limit(1).all()
    for subject in subjects:
        results.append(subject.subject_name)


    return jsonify(*results)


@app.route('/search-books.json', methods=["POST", "GET"])
def search_to_books():
    language=None
    results = []
    keyword = request.args.get('book')
    subject_input = request.args.get('subject')
    language = request.args.get('language')

    if keyword:
        
        query = db.session.query(Book).filter(Book.isbn_13 != None)
    
        if not subject_input:
            if language:

                #account for language
                query = search(query, keyword, sort=True)
                books = (
                    query.filter(Book.language==language)
                         .all()
                )
                # books = query.limit(10).all()
                count = query.count()
                for book in books:
                    book = book.search_results()
                    results.append(book)
            else:
              
                query = search(query, keyword, sort=True)
               
                books = query.limit(10).all()
               
                count = query.count()

                for book in books:
                   
                    book = book.search_results()
                    results.append(book)



        else:

            subject = Subject.query.filter(Subject.subject_name==subject_input).first()
            query = (
                    query
                    .join(Book_subjects)
                    .filter(Book_subjects.subject_id==subject.subject_id)
                )

            query = search(query, keyword,sort=True)
            books = query.limit(1000).all()
            count = query.count()
            for book in books:
                book = book.search_results()
                results.append(book)

    elif subject_input:

        query = db.session.query(Subject)

        query = search(query, subject_input, sort=True)
        subjects = query.limit(1000).all()
        count = query.count()
        

        for subject in subjects:
            for book in subject.books:
                book = book.search_results()
               

                results.append(book)
   

    return jsonify({"results": results, "count":count })

@app.route('/search-books')
def search_books_form():
    """Search form for user to search books"""

    user_id = session.get('user_id')
    user = User.query.get(user_id)

    book_languages = Book.query.filter(Book.language != None).limit(1000).all()

    languages = set()
    for book in book_languages:
        languages.add(book.language)

    return render_template('search.html',user=user,languages=languages)

@app.route('/')
def indenx():
    """Homepage"""

    return render_template("index.html")

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

    return render_template("index.html")

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
    cover_img = None
    summary = None
    genres = None 

    user = User.query.get(user_id)

    if user.book_shelves:
        for book_shelf in user.book_shelves:
            book_json = book_shelf.books.get_google_metadata()
            if book_json["totalItems"] >= 1:
                summary, cover_img, genres = book_shelf.books.parse_metadata(book_json)
                book_shelf.cover_img = cover_img

            elif book_json["totalItems"] < 1:

                response_ol = book_shelf.books.get_open_metadata()
                if response_ol:
                    cover_img, summary, genres = book_shelf.books.parse_ol_metadata(response_ol)


    return render_template("user.html", cover_img=cover_img, user=user)


@app.route("/books/<int:page_num>")
def book_list(page_num):
    """Show list of books."""
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    books = (
            Book
            .query
            .filter(Book.isbn_13 !=None)
            .order_by(Book.title)
            .paginate(per_page=20, page=page_num,error_out=True)
            )

    return render_template('book_list.html',page_num=page_num, user=user,books=books)
    

@app.route("/Author/<int:author_id>", methods=['GET'])
def author_info(author_id):
    """Show books written by author"""

    author = Author.query.get(author_id)
    
    author_books = author.get_books()
   
    return render_template('author.html', author=author,author_books=author_books)
        

@app.route("/Book/<int:book_id>", methods=['GET'])
def book_detail(book_id):
    """Show info about book
    if user if logged in 
    """

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    book = Book.query.get(book_id)

    author = book.get_author()
    session["book_id"] = book.book_id
    genres = []
    summary = None
    cover_img = None

    book_json = book.get_google_metadata()
    if book_json["totalItems"] >= 1:
        summary, cover_img, genres = book.parse_metadata(book_json)

    elif book_json["totalItems"] < 1:

        response_ol = book.get_open_metadata()
        if response_ol:
            cover_img, summary, genres = book.parse_ol_metadata(response_ol)

    return render_template("book.html",genres=genres,user=user,author=author,book=book,summary=summary,cover_img=cover_img)


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
@app.route('/get_graph_info.json', methods=['GET'])
def create_graph_data():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    users_books = user.book_shelves 

    nodes = []
    links = []

    user = user.convert_info()
    nodes.append(user)

    for book in users_books:   
        book_dict = book.convert_book_info()
        nodes.append(book_dict)
        links.append({"source": user["id"], "target": book_dict["id"]})

        subjects = book.books.get_subjects()
        for subject in subjects:
            subject_dict = subject.convert_info()
            nodes.append(subject_dict)
            links.append({"source": book_dict["id"], "target": subject_dict["id"]})

        author = book.books.get_author()
        author_dict = author.convert_info()
        nodes.append(author_dict)
        links.append({"source": book_dict["id"] , "target": author_dict["id"]})


    return jsonify({'nodes':nodes, 'links':links})

@app.route('/graph')
def display_graph():

    return render_template('graph.html')

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')