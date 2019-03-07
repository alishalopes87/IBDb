"""Book_shelves"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,jsonify, abort)
from sqlalchemy.orm.attributes import flag_modified 
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy_searchable import search, parse_search_query
from flask_debugtoolbar import DebugToolbarExtension
import requests
from model_2 import *
from pyisbn import convert as convert_isbn
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
        # query = db.session.query(Book)
        # print(query)
        # query = search(query, title,sort=True)
        combined_search_vector = (Book.search_vector | db.func.coalesce(Author.search_vector, u''))

        books_query = (
        db.session.query(Book)
            .join(Author)
            .filter(
        combined_search_vector.match(parse_search_query(title)
            )
        )
    )
    
        print("Please",title)
        #do a join across tables and quiry on that join
        books = books_query.limit(1).all()
        print(books)
        # books = query.filter(Book.title.ilike('%' + title + '%')).all()
        

        for book in books:

            book = {
            'author':book.author_ol_id,
            'book_id': book.book_id,
            'title': book.title,
            'book_url': '/Book/{}'.format(book.book_id)
            }
       
            results.append(book)
            #counting subjects 
            #sort by language filter 

    # elif author:

    #     query= db.session.query(Author)
    #     query = search(query, author,sort=True)
    #     # authors = query.filter(Author.name.ilike('%' + author + '%')).all()
    #     authors = query.first()

    #     for author in authors:
    #         author ={
    #         'author_ol_id': author.author_ol_id,
    #         'name': author.name,
    #         'author_url': '/Author/{}'.format(author.author_id)
    #         }

    #         results.append(author)

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
    
    author_books = author.get_books()
   
    return render_template('author.html', author=author,author_books=author_books)
        

@app.route("/Book/<int:book_id>", methods=['GET'])
def book_detail(book_id):
    """Show info about book
    if user if logged in 
    """

    book = Book.query.get(book_id)

    author = book.get_author()
    session["book_id"] = book.book_id

    book_json = book.get_google_metadata()
    summary, cover_img, genres = book.parse_metadata(book_json)


    return render_template("book.html",
                            book=book,
                            author=author,
                            summary=summary, 
                            cover_img=cover_img, 
                            genres=genres)


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
    data = {
    "nodes": nodes,
    "links": links
    }

    user = user.convert_info()
    nodes.append(user)

    for book in users_books:   
        book_dict = book.convert_book_info()
        nodes.append(book_dict)
        print(book_dict)
        links.append({"source": user["id"], "target": book_dict["id"]})

        authors = book.books.authors_books
        for author in authors:
            author_dict = author.convert_info()
            nodes.append(author_dict)
            links.append({"source": book_id , "target": author_id})


    return jsonify(data)

@app.route('/graph')
def display_graph():

    return render_template('graph.html')

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