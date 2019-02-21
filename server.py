"""Book_shelves"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,jsonify, abort)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Book_shelf, Book, connect_to_db, db

import json


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

@app.route('/search-books.json')
def search_to_books():
    results = []
    books = []

    title = request.args.get('book')
    author = request.args.get('author')

    if title:
        books = Book.query.filter(Book.title.ilike('%' + title + '%')).all()

    elif author:
        books = Book.query.filter(Book.author.ilike('%' + author + '%')).all()
    else:
        abort(400)

    for book in books:
        
        book = {
        'book_id': book.book_id,
        'title': book.title,
        'author': book.author,
        'image_url': book.image_url,
        'small_image_url': book.small_image_url,
        'book_url': '/Book/{}'.format(book.book_id)
        }
       
        results.append(book)

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

    books = Book.query.order_by('title').all()
    return render_template("book_list.html", books=books)

@app.route("/Book/<int:book_id>", methods=['GET'])
def book_detail(book_id):
    """Show info about book
    if user if logged in 
    """

    book = Book.query.get(book_id)
    session["book_id"] = book.book_id

    return render_template("book.html",
                            book=book)

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

# @app.route("/delete_book<int:book_id>", methods=['POST'])
# def delete_book_from_user_shelf(book_id):
#     """Delete book from users shelf"""

#     user_id = session.get("user_id")

#     if user_id:

#         book = Book.query.get(book_id)
#         book.delete()  

#         db.session.commit()

#         flash("Book deleted from your shelf")
#         return redirect(f"User/{user_id}")

#     else:
#         flash("Must be logged in to delete")
#         return redirect(f"/")

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