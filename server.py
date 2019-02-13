"""Book_shelves"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Book_shelf, Book, connect_to_db, db


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def indenx():
    """Homepage"""

    return render_template("homepage.html")


@app.route('/register', methods=["POST"])
def register_process():
    """Add user information to database"""

    email = request.form["email"]
    password = request.form['password']

    try:
        User.query.filter(User.email == email ).one()
    
    except:
        user = User(email=email,
                    password=password)
        
        db.session.add(user)
        db.session.commit()

    return redirect("/")

@app.route('/login', methods=['POST'])
def login_process():
    """Process user login"""

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Email not recognized, please try again.")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password, try again")
        return redirect('/login')

    session['user_id']  = user.user_id

    flash('Logged in')

@app.route('/logout')
def logout():
    """Log user out"""

    del session['user_id']
    flash('Logged out')
    return redirect('/')





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