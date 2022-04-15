"""Server for movie ratings app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


@app.route("/movies")
def show_all_movies():
    """View all movies"""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies = movies)


@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)


@app.route("/users")
def show_all_users():
    """View all users"""

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show user details"""
    
    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user = user)


@app.route("/users", methods = ["post"])
def register_user():
    """Create a new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("Email address already exists. Please try again with another email address!")
    else:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("Your account was created successfully and you can now log in.")

    return redirect("/")

@app.route("/login", methods = ["POST"])
def login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user and user.password == password:
        # Log in user by storing the user's primary key in session
        session["user_id"] = user.user_id
        flash(f"Welcome back, User {user.user_id}")
    else:
        flash("The email or password you entered was incorrect.")

    return redirect("/")




if __name__ == "__main__":
    # connect to database before app.run gets called. 
    # If not, Flask won’t be able to access your database
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
